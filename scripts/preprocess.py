"""
Preprocessing for Scholarship Eligibility Dataset.
Handles missing values, encodes categories, splits data,
and saves processed files for training.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split

# Paths
DATA_DIR = Path("data")
INPUT_FILE = DATA_DIR / "students.csv"
TRAIN_FILE = DATA_DIR / "train.csv"
TEST_FILE = DATA_DIR / "test.csv"


# Load the dataset
def load_data():
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} records from {INPUT_FILE}")
    return df


# Handle missing values
def fill_missing(df):
    print("\nMissing values before:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    # Fill marks with median
    df["marks"] = df["marks"].fillna(df["marks"].median())

    # Fill attendance with median
    df["attendance"] = df["attendance"].fillna(df["attendance"].median())

    print("\nMissing values after:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    if df.isnull().sum().sum() == 0:
        print("None - all cleaned!")

    return df


# Encode categorical columns to numbers
def encode_categoricals(df):
    # Binary mapping for disability
    df["disability"] = df["disability"].map({"Yes": 1, "No": 0})

    # Binary mapping for target
    df["eligible"] = df["eligible"].map({"Yes": 1, "No": 0})

    # One-hot encode multi-value columns
    df = pd.get_dummies(
        df,
        columns=["gender", "category", "education"],
        drop_first=False
    )

    print(f"\nEncoded columns: {len(df.columns)}")
    return df


# Drop columns not useful for training
def drop_unused(df):
    # student_id is just an identifier, not a feature
    if "student_id" in df.columns:
        df = df.drop(columns=["student_id"])
    return df


# Split into train and test
def split_data(df):
    X = df.drop(columns=["eligible"])
    y = df["eligible"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTrain size: {len(X_train)}")
    print(f"Test size:  {len(X_test)}")
    print(f"Train eligible ratio: {y_train.mean():.3f}")
    print(f"Test eligible ratio:  {y_test.mean():.3f}")

    return X_train, X_test, y_train, y_test


# Save train and test as CSVs
def save_splits(X_train, X_test, y_train, y_test):
    train_df = X_train.copy()
    train_df["eligible"] = y_train.values
    train_df.to_csv(TRAIN_FILE, index=False)

    test_df = X_test.copy()
    test_df["eligible"] = y_test.values
    test_df.to_csv(TEST_FILE, index=False)

    print(f"\nSaved: {TRAIN_FILE}")
    print(f"Saved: {TEST_FILE}")


# Main pipeline
def main():
    print("=" * 60)
    print("  PREPROCESSING PIPELINE")
    print("=" * 60)

    df = load_data()
    df = fill_missing(df)
    df = drop_unused(df)
    df = encode_categoricals(df)

    X_train, X_test, y_train, y_test = split_data(df)
    save_splits(X_train, X_test, y_train, y_test)

    print("\n" + "=" * 60)
    print("  PREPROCESSING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()