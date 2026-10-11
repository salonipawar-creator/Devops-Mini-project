import logging
import os
from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s result-service %(message)s")
logger = logging.getLogger(__name__)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
DB_NAME = os.getenv("MONGO_DB", "urine_strip_demo")
USE_MEMORY = os.getenv("USE_MEMORY_STORE", "false").lower() == "true"

app = FastAPI(title="Result Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
memory_store: list[dict] = []
mongo_client = None


class Analysis(BaseModel):
    image_metadata: dict = Field(default_factory=dict)
    detected_pads: list[dict]
    measurements: list[dict]
    ml_predictions: list[dict] = Field(default_factory=list)
    final_results: list[dict]
    disclaimer: str


def serialize(document: dict) -> dict:
    doc = dict(document)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


def collection():
    global mongo_client
    if USE_MEMORY:
        return None
    if mongo_client is None:
        mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2500)
    mongo_client.admin.command("ping")
    return mongo_client[DB_NAME]["analyses"]


@app.get("/health")
def health():
    if USE_MEMORY:
        return {"status": "healthy", "service": "result-service", "database": "memory"}
    try:
        collection()
        return {"status": "healthy", "service": "result-service", "database": "mongodb"}
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="MongoDB unavailable.")


@app.post("/results")
def save_result(analysis: Analysis):
    logger.info("saving analysis")
    document = analysis.model_dump()
    document["created_at"] = datetime.now(timezone.utc).isoformat()
    if USE_MEMORY:
        document["id"] = str(uuid4())
        memory_store.append(document)
        return document
    try:
        inserted = collection().insert_one(document)
        document["_id"] = inserted.inserted_id
        return serialize(document)
    except PyMongoError as exc:
        logger.exception("database operation failed")
        raise HTTPException(status_code=503, detail="Database unavailable.") from exc


@app.get("/results")
def list_results():
    logger.info("listing analyses")
    if USE_MEMORY:
        return {"results": list(reversed(memory_store))}
    try:
        docs = collection().find().sort("created_at", -1).limit(25)
        return {"results": [serialize(doc) for doc in docs]}
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable.") from exc


@app.get("/results/{analysis_id}")
def get_result(analysis_id: str):
    if USE_MEMORY:
        for doc in memory_store:
            if doc["id"] == analysis_id:
                return doc
        raise HTTPException(status_code=404, detail="Analysis not found.")
    try:
        doc = collection().find_one({"_id": ObjectId(analysis_id)})
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid analysis id.") from exc
    if not doc:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return serialize(doc)
