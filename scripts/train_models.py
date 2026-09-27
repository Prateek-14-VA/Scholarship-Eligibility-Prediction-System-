"""
Train and evaluate multiple classification models
for scholarship eligibility prediction.
Uses feature scaling for better convergence.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)

# Paths
DATA_DIR = Path("data")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_FILE = DATA_DIR / "train.csv"
TEST_FILE = DATA_DIR / "test.csv"
RESULTS_FILE = DATA_DIR / "model_results.csv"
BEST_MODEL_FILE = MODEL_DIR / "best_model.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"


# Load train and test sets
def load_data():
    train_df = pd.read_csv(TRAIN_FILE)
    test_df = pd.read_csv(TEST_FILE)

    X_train = train_df.drop(columns=["eligible"])
    y_train = train_df["eligible"]

    X_test = test_df.drop(columns=["eligible"])
    y_test = test_df["eligible"]

    print(f"Train: {X_train.shape}, Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test


# Scale numeric features
def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save scaler for use during prediction
    joblib.dump(scaler, SCALER_FILE)

    return X_train_scaled, X_test_scaled, scaler


# Build the four models
def get_models():
    return {
        "Logistic Regression": LogisticRegression(max_iter=5000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=15, random_state=42
        ),
        "SVM": SVC(kernel="rbf", C=1.0, gamma="scale",
                   probability=True, random_state=42)
    }


# Evaluate one model
def evaluate_model(name, model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"\n{'-' * 55}")
    print(f"  {name}")
    print(f"{'-' * 55}")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1 Score:  {f1:.4f}")

    cm = confusion_matrix(y_test, y_pred)
    print(f"  Confusion Matrix:")
    print(f"                 Predicted No  Predicted Yes")
    print(f"  Actual No      {cm[0][0]:>6}       {cm[0][1]:>6}")
    print(f"  Actual Yes     {cm[1][0]:>6}       {cm[1][1]:>6}")

    return {
        "Model": name,
        "Accuracy": round(acc, 4),
        "Precision": round(prec, 4),
        "Recall": round(rec, 4),
        "F1": round(f1, 4)
    }


# Main pipeline
def main():
    print("=" * 55)
    print("  MODEL TRAINING AND EVALUATION")
    print("=" * 55)

    X_train, X_test, y_train, y_test = load_data()

    print("\nScaling features...")
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    print(f"Scaler saved: {SCALER_FILE}")

    models = get_models()
    results = []
    trained_models = {}

    for name, model in models.items():
        row = evaluate_model(name, model, X_train_scaled, y_train,
                             X_test_scaled, y_test)
        results.append(row)
        trained_models[name] = model

    # Summary
    results_df = pd.DataFrame(results).sort_values("F1", ascending=False)
    results_df.to_csv(RESULTS_FILE, index=False)

    print("\n" + "=" * 55)
    print("  MODEL COMPARISON (sorted by F1)")
    print("=" * 55)
    print(results_df.to_string(index=False))

    # Save all models
    for name, model in trained_models.items():
        safe_name = name.lower().replace(" ", "_")
        joblib.dump(model, MODEL_DIR / f"{safe_name}.pkl")

    # Save best model
    best_name = results_df.iloc[0]["Model"]
    best_model = trained_models[best_name]
    joblib.dump(best_model, BEST_MODEL_FILE)

    print(f"\nBest model: {best_name}")
    print(f"Saved as:   {BEST_MODEL_FILE}")
    print(f"Results:    {RESULTS_FILE}")
    print("=" * 55)


if __name__ == "__main__":
    main()