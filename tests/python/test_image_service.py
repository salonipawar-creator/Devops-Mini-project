from pathlib import Path
import importlib.util

import cv2
import numpy as np

SERVICE_PATH = Path(__file__).resolve().parents[2] / "services" / "image-service" / "main.py"
spec = importlib.util.spec_from_file_location("image_service_main", SERVICE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
quality_report = module.quality_report
decode_image = module.decode_image
detect_strip = module.detect_strip
pads_from_layout = module.pads_from_layout
health = module.health


def synthetic_image():
    image = np.full((900, 520, 3), 245, dtype=np.uint8)
    cv2.rectangle(image, (215, 50), (305, 850), (225, 225, 225), -1)
    colors = [(104, 203, 248), (95, 220, 231), (64, 151, 237), (153, 185, 239), (78, 203, 238),
              (178, 206, 232), (202, 213, 245), (112, 139, 59), (137, 196, 232), (139, 177, 239)]
    for idx, color in enumerate(colors):
        y = 90 + idx * 75
        cv2.rectangle(image, (230, y), (290, y + 60), color, -1)
    return image


def test_health():
    assert health()["service"] == "image-service"


def test_quality_report_good_image():
    report = quality_report(synthetic_image())
    assert report["quality"] == "good"


def test_detect_strip_and_pads():
    strip_box = detect_strip(synthetic_image())
    pads = pads_from_layout(strip_box)
    assert len(pads) == 10
    assert pads[0]["parameter"] == "glucose"


def test_decode_valid_image():
    ok, encoded = cv2.imencode(".png", synthetic_image())
    assert ok
    image = decode_image(encoded.tobytes())
    assert image.shape[0] == 900


def test_invalid_image():
    try:
        decode_image(b"not image")
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
