"""
Prediction pipeline for scholarship eligibility.
Handles raw student input, encoding, scaling, and prediction.
"""

import joblib
import pandas as pd
from pathlib import Path

# Paths (absolute, so it works from any folder)
PROJECT_ROOT = Path(__file__).parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_FILE = MODEL_DIR / "best_model.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"
TRAIN_FILE = PROJECT_ROOT / "data" / "train.csv"

# Load once at import time
_model = joblib.load(MODEL_FILE)
_scaler = joblib.load(SCALER_FILE)
_train_df = pd.read_csv(TRAIN_FILE)
FEATURE_COLUMNS = [c for c in _train_df.columns if c != "eligible"]


# Build a one-row feature vector from raw input
def build_features(student):
    """
    student = {
        "age": int,
        "gender": "Male"|"Female"|"Other",
        "category": "General"|"OBC"|"SC"|"ST"|"EWS"|"Minority",
        "disability": "Yes"|"No",
        "education": "UG"|"PG"|"Technical"|"Professional",
        "marks": float,
        "attendance": float,
        "income": int
    }
    """
    row = {col: 0 for col in FEATURE_COLUMNS}

    # Numeric features
    row["age"] = student["age"]
    row["marks"] = student["marks"]
    row["attendance"] = student["attendance"]
    row["income"] = student["income"]
    row["disability"] = 1 if student["disability"] == "Yes" else 0

    # One-hot encoded features
    g = f"gender_{student['gender']}"
    c = f"category_{student['category']}"
    e = f"education_{student['education']}"

    if g in row:
        row[g] = 1
    if c in row:
        row[c] = 1
    if e in row:
        row[e] = 1

    return pd.DataFrame([row])[FEATURE_COLUMNS]


# Main prediction function
def predict_student(student):
    """
    Returns:
        {
            "eligible": bool,
            "label": "Eligible" or "Not Eligible",
            "score": float (0-100),
            "confidence": float (0-1)
        }
    """
    X = build_features(student)
    X_scaled = _scaler.transform(X)

    pred = int(_model.predict(X_scaled)[0])
    prob = float(_model.predict_proba(X_scaled)[0][1])

    return {
        "eligible": bool(pred == 1),
        "label": "Eligible" if pred == 1 else "Not Eligible",
        "score": round(prob * 100, 2),
        "confidence": round(prob, 4),
    }


# Quick test when running this file directly
if __name__ == "__main__":
    test_student = {
        "age": 22,
        "gender": "Female",
        "category": "SC",
        "disability": "No",
        "education": "PG",
        "marks": 85.0,
        "attendance": 90.0,
        "income": 200000,
    }

    result = predict_student(test_student)
    print("=" * 55)
    print("  PREDICTION PIPELINE TEST")
    print("=" * 55)
    for k, v in result.items():
        print(f"  {k:<12}: {v}")
    print("=" * 55)
    