import logging
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s ai-service %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "ml" / "saved_model" / "urine_demo_rf.joblib"

app = FastAPI(title="AI/ML Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
model_bundle = None


class Measurement(BaseModel):
    parameter: str
    rgb: dict
    hsv: dict
    lab: dict
    color_distance: float = Field(ge=0)
    reference_match: str


def load_model():
    global model_bundle
    if model_bundle is None:
        if not MODEL_PATH.exists():
            raise HTTPException(status_code=503, detail="Demo ML model is not trained. Run python ml/train.py first.")
        model_bundle = joblib.load(MODEL_PATH)
    return model_bundle


def features(measurement: Measurement):
    return [[
        measurement.rgb["r"], measurement.rgb["g"], measurement.rgb["b"],
        measurement.hsv["h"], measurement.hsv["s"], measurement.hsv["v"],
        measurement.lab["l"], measurement.lab["a"], measurement.lab["b"],
    ]]


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-service", "model_loaded": MODEL_PATH.exists()}


@app.post("/predict")
def predict(measurements: list[Measurement]):
    logger.info("prediction request for %s pads", len(measurements))
    bundle = load_model()
    model = bundle["model"]
    predictions = []
    for measurement in measurements:
        probabilities = model.predict_proba(features(measurement))[0]
        classes = model.classes_
        ranked = sorted(zip(probabilities, classes), reverse=True)
        best_probability, best_label = next(
            ((prob, label) for prob, label in ranked if label.startswith(f"{measurement.parameter}:")),
            (ranked[0][0], ranked[0][1]),
        )
        predicted_parameter, category = best_label.split(":", 1)
        if predicted_parameter != measurement.parameter:
            category = measurement.reference_match
            best_probability = 0.0
        predictions.append({
            "parameter": measurement.parameter,
            "prediction": category,
            "confidence": round(float(best_probability), 3),
            "explanation": "Random Forest trained on synthetic demonstration colors; reference matching remains primary.",
        })
    return {"predictions": predictions}
