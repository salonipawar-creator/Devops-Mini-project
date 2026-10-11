import json
from pathlib import Path

import cv2
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config" / "color_reference.json").read_text())
MODEL_PATH = ROOT / "ml" / "saved_model" / "urine_demo_rf.joblib"
DATASET_PATH = ROOT / "ml" / "dataset" / "demo_dataset.csv"


def rgb_to_features(rgb):
    r, g, b = [int(v) for v in rgb]
    hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
    lab = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2LAB)[0][0]
    return [r, g, b, int(hsv[0]) * 2, int(hsv[1]), int(hsv[2]), float(lab[0]) * 100 / 255, float(lab[1]) - 128, float(lab[2]) - 128]


def build_demo_dataset():
    rng = np.random.default_rng(42)
    rows = ["parameter,category,r,g,b,h,s,v,l,a,lab_b"]
    x, y = [], []
    for parameter, refs in CONFIG["references"].items():
        for ref in refs:
            base = np.array(ref["rgb"], dtype=int)
            for _ in range(22):
                rgb = np.clip(base + rng.normal(0, 7, 3), 0, 255).astype(int)
                features = rgb_to_features(rgb)
                label = f"{parameter}:{ref['category']}"
                x.append(features)
                y.append(label)
                rows.append(",".join([parameter, ref["category"], *[str(round(v, 4)) for v in features]]))
    DATASET_PATH.write_text("\n".join(rows))
    return np.array(x), np.array(y)


def main():
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    x, y = build_demo_dataset()
    model = Pipeline([
        ("scale", StandardScaler()),
        ("forest", RandomForestClassifier(n_estimators=120, random_state=7, class_weight="balanced")),
    ])
    model.fit(x, y)
    joblib.dump({"model": model, "feature_order": ["r", "g", "b", "h", "s", "v", "l", "a", "lab_b"]}, MODEL_PATH)
    print(f"Saved demo model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
