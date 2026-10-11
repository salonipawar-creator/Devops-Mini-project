import json
import logging
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s colorimetry-service %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "config" / "color_reference.json").read_text())
REFERENCES = CONFIG["references"]

app = FastAPI(title="Colorimetry Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def decode_image(content: bytes) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image.")
    return image


def rgb_to_lab(rgb: tuple[int, int, int]) -> dict:
    patch = np.uint8([[[rgb[2], rgb[1], rgb[0]]]])
    lab = cv2.cvtColor(patch, cv2.COLOR_BGR2LAB)[0][0]
    return {"l": round(float(lab[0]) * 100 / 255, 2), "a": round(float(lab[1]) - 128, 2), "b": round(float(lab[2]) - 128, 2)}


def rgb_to_hsv(rgb: tuple[int, int, int]) -> dict:
    patch = np.uint8([[[rgb[2], rgb[1], rgb[0]]]])
    hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)[0][0]
    return {"h": int(hsv[0]) * 2, "s": int(hsv[1]), "v": int(hsv[2])}


def delta_e(lab_a: dict, lab_b: dict) -> float:
    return float(np.sqrt((lab_a["l"] - lab_b["l"]) ** 2 + (lab_a["a"] - lab_b["a"]) ** 2 + (lab_a["b"] - lab_b["b"]) ** 2))


def representative_rgb(image: np.ndarray, pad: dict) -> tuple[int, int, int]:
    x, y, w, h = pad["x"], pad["y"], pad["width"], pad["height"]
    x0 = max(0, x + int(w * 0.22))
    y0 = max(0, y + int(h * 0.22))
    x1 = min(image.shape[1], x + int(w * 0.78))
    y1 = min(image.shape[0], y + int(h * 0.78))
    crop = image[y0:y1, x0:x1]
    if crop.size == 0:
        raise HTTPException(status_code=422, detail=f"Pad crop is outside image bounds for {pad.get('parameter')}.")
    # Median is used because strip pad edges, glare, and background pixels can bias a mean or single-pixel sample.
    b, g, r = np.median(crop.reshape(-1, 3), axis=0)
    return int(round(r)), int(round(g)), int(round(b))


def classify(parameter: str, lab: dict) -> tuple[str, float]:
    refs = REFERENCES.get(parameter)
    if not refs:
        raise HTTPException(status_code=422, detail=f"No reference colors configured for {parameter}.")
    distances = []
    for ref in refs:
        ref_lab = rgb_to_lab(tuple(ref["rgb"]))
        distances.append((delta_e(lab, ref_lab), ref["category"]))
    distance, category = min(distances, key=lambda item: item[0])
    return category, round(distance, 2)


def analyze_pad(image: np.ndarray, pad: dict) -> dict:
    parameter = pad["parameter"]
    logger.info("extracting color for %s", parameter)
    rgb = representative_rgb(image, pad)
    hsv = rgb_to_hsv(rgb)
    lab = rgb_to_lab(rgb)
    match, distance = classify(parameter, lab)
    return {
        "parameter": parameter,
        "rgb": {"r": rgb[0], "g": rgb[1], "b": rgb[2]},
        "hsv": hsv,
        "lab": lab,
        "hex": f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}",
        "reference_match": match,
        "color_distance": distance,
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "colorimetry-service"}


@app.post("/analyze-colors")
async def analyze_colors(file: UploadFile = File(...), pads_json: str = Form(...)):
    logger.info("request received")
    image = decode_image(await file.read())
    try:
        pads = json.loads(pads_json)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="pads_json must be valid JSON.") from exc
    results = [analyze_pad(image, pad) for pad in pads]
    return {"measurements": results, "method": "median central crop with RGB, HSV, Lab and Delta-E comparison"}
