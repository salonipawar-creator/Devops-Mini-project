from pathlib import Path
import importlib.util
import subprocess
import sys

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]


def ensure_model():
    subprocess.run([sys.executable, str(ROOT / "ml" / "train.py")], check=True)


ensure_model()
SERVICE_PATH = ROOT / "services" / "ai-service" / "main.py"
spec = importlib.util.spec_from_file_location("ai_service_main", SERVICE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
app = module.app
Measurement = module.Measurement
health = module.health
predict = module.predict


def test_health():
    data = health()
    assert data["service"] == "ai-service"
    assert data["model_loaded"] is True


def test_prediction():
    payload = Measurement(
        parameter="glucose",
        rgb={"r": 248, "g": 203, "b": 104},
        hsv={"h": 42, "s": 148, "v": 248},
        lab={"l": 83.0, "a": 7.0, "b": 55.0},
        color_distance=0.2,
        reference_match="negative",
    )
    response = predict([payload])
    assert response["predictions"][0]["parameter"] == "glucose"


def test_invalid_input():
    with pytest.raises(ValidationError):
        Measurement(parameter="glucose")
