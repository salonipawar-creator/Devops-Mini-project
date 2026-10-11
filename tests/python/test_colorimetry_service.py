from pathlib import Path
import importlib.util

import cv2
import numpy as np

SERVICE_PATH = Path(__file__).resolve().parents[2] / "services" / "colorimetry-service" / "main.py"
spec = importlib.util.spec_from_file_location("colorimetry_service_main", SERVICE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
classify = module.classify
representative_rgb = module.representative_rgb
rgb_to_hsv = module.rgb_to_hsv
rgb_to_lab = module.rgb_to_lab
analyze_pad = module.analyze_pad
health = module.health


def test_health():
    assert health()["service"] == "colorimetry-service"


def test_color_conversions_and_reference_match():
    rgb = (248, 203, 104)
    hsv = rgb_to_hsv(rgb)
    lab = rgb_to_lab(rgb)
    assert hsv["v"] == 248
    assert "l" in lab and "a" in lab and "b" in lab
    category, distance = classify("glucose", lab)
    assert category == "negative"
    assert distance < 1


def test_representative_rgb_uses_central_crop():
    image = np.full((100, 100, 3), (0, 0, 0), dtype=np.uint8)
    image[30:70, 30:70] = (90, 170, 180)
    rgb = representative_rgb(image, {"parameter": "glucose", "x": 20, "y": 20, "width": 60, "height": 60})
    assert rgb == (180, 170, 90)


def test_analyze_pad():
    image = np.full((120, 120, 3), 255, dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (80, 80), (104, 203, 248), -1)
    result = analyze_pad(image, {"parameter": "glucose", "x": 20, "y": 20, "width": 60, "height": 60})
    assert result["reference_match"] == "negative"
