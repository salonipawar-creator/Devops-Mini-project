import importlib
import importlib.util
import os
from pathlib import Path

os.environ["USE_MEMORY_STORE"] = "true"
SERVICE_PATH = Path(__file__).resolve().parents[2] / "services" / "result-service" / "main.py"
spec = importlib.util.spec_from_file_location("result_service_main", SERVICE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Analysis = module.Analysis


def sample_payload():
    return {
        "image_metadata": {"filename": "demo.png"},
        "detected_pads": [{"parameter": "glucose", "x": 1, "y": 2, "width": 3, "height": 4}],
        "measurements": [{"parameter": "glucose", "reference_match": "negative"}],
        "ml_predictions": [{"parameter": "glucose", "prediction": "negative", "confidence": 0.9}],
        "final_results": [{"parameter": "glucose", "estimated_result": "negative", "confidence": 0.9}],
        "disclaimer": "Academic demonstration only."
    }


def test_health_memory():
    assert module.health()["database"] == "memory"


def test_save_and_retrieve_result():
    saved = module.save_result(Analysis(**sample_payload()))
    analysis_id = saved["id"]
    listed = module.list_results()["results"]
    assert listed[0]["id"] == analysis_id
    fetched = module.get_result(analysis_id)
    assert fetched["image_metadata"]["filename"] == "demo.png"
