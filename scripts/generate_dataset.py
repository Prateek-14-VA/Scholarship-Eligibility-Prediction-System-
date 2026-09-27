"""
Scholarship Eligibility Prediction System
Builds a synthetic student dataset with eligibility labels
based on Indian scholarship scheme rules.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Settings
SEED = 2024
SAMPLE_SIZE = 2000
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "students.csv"

rng = np.random.default_rng(SEED)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Pick category values based on India-like proportions
def pick_categories(n):
    labels = ["General", "OBC", "SC", "ST", "EWS", "Minority"]
    weights = [0.30, 0.27, 0.16, 0.08, 0.10, 0.09]
    return rng.choice(labels, size=n, p=weights)


# Pick gender values
def pick_gender(n):
    return rng.choice(["Male", "Female", "Other"], size=n, p=[0.48, 0.50, 0.02])


# Pick disability status (5% yes)
def pick_disability(n):
    return rng.choice(["Yes", "No"], size=n, p=[0.05, 0.95])


# Pick education level
def pick_education(n):
    return rng.choice(
        ["UG", "PG", "Technical", "Professional"],
        size=n,
        p=[0.40, 0.25, 0.20, 0.15],
    )


# Build the raw student table
def build_raw_table(n):
    ages = rng.integers(17, 31, size=n)

    # Marks around 72 with std 12, clipped between 35 and 100
    marks = np.clip(rng.normal(72, 12, n), 35, 100).round(2)

    # Attendance around 82 with std 10, clipped between 40 and 100
    attendance = np.clip(rng.normal(82, 10, n), 40, 100).round(2)

    # Income as log-normal, clipped between 30K and 15L
    income = np.clip(rng.lognormal(12.5, 0.7, n), 30_000, 1_500_000).astype(int)

    return pd.DataFrame(
        {
            "student_id": [f"STU{i:05d}" for i in range(1, n + 1)],
            "age": ages,
            "gender": pick_gender(n),
            "category": pick_categories(n),
            "disability": pick_disability(n),
            "education": pick_education(n),
            "marks": marks,
            "attendance": attendance,
            "income": income,
        }
    )


# Income caps for eligibility
RESERVED = {"SC", "ST", "OBC", "Minority", "EWS"}
GENERAL_INCOME_CAP = 250_000
RESERVED_INCOME_CAP = 450_000
DISABILITY_INCOME_CAP = 400_000
GIRL_CHILD_INCOME_CAP = 300_000

# Age and score limits
MIN_AGE = 17
MAX_AGE = 30
MIN_ATTENDANCE = 60
MIN_MARKS = 65
MIN_MARKS_DISABILITY = 55


# Decide Yes or No for one student row
def decide_eligibility(row):
    if row["age"] > MAX_AGE or row["age"] < MIN_AGE:
        return "No"

    if row["attendance"] < MIN_ATTENDANCE:
        return "No"

    # Disability path (relaxed marks)
    if row["disability"] == "Yes":
        if row["marks"] >= MIN_MARKS_DISABILITY and row["income"] <= DISABILITY_INCOME_CAP:
            return "Yes"
        return "No"

    # Basic marks check
    if row["marks"] < MIN_MARKS:
        return "No"

    # Choose income cap based on category and gender
    if row["category"] in RESERVED:
        cap = RESERVED_INCOME_CAP
    else:
        cap = GENERAL_INCOME_CAP

    if row["gender"] == "Female":
        cap = max(cap, GIRL_CHILD_INCOME_CAP)

    return "Yes" if row["income"] <= cap else "No"


# Add noise and missing values to look realistic
def add_noise(df, flip_rate=0.04, missing_rate=0.02):
    n = len(df)

    # Flip some labels
    flip_idx = rng.random(n) < flip_rate
    df.loc[flip_idx, "eligible"] = df.loc[flip_idx, "eligible"].map(
        {"Yes": "No", "No": "Yes"}
    )

    # Blank some marks and attendance
    mask_marks = rng.random(n) < missing_rate
    mask_attendance = rng.random(n) < missing_rate
    df.loc[mask_marks, "marks"] = np.nan
    df.loc[mask_attendance, "attendance"] = np.nan

    return df


# Print summary after saving
def print_report(df, path):
    yes = (df["eligible"] == "Yes").sum()
    no = (df["eligible"] == "No").sum()
    total = len(df)

    print("=" * 60)
    print("  DATASET BUILD COMPLETE")
    print("=" * 60)
    print(f"  Saved to:       {path}")
    print(f"  Records:        {total}")
    print(f"  Columns:        {len(df.columns)}")
    print()
    print("  Label balance:")
    print(f"    Eligible:     {yes:>5}  ({yes / total * 100:5.1f}%)")
    print(f"    Not Eligible: {no:>5}  ({no / total * 100:5.1f}%)")
    print()
    print("  Missing values:")
    for col, count in df.isnull().sum().items():
        if count:
            print(f"    {col:<12} {count}")
    print()
    print("  First 5 rows:")
    print(df.head().to_string(index=False))
    print("=" * 60)


# Main entry
def main():
    print("Building student dataset...")
    df = build_raw_table(SAMPLE_SIZE)

    print("Applying eligibility rules...")
    df["eligible"] = df.apply(decide_eligibility, axis=1)

    print("Adding noise...")
    df = add_noise(df)

    df.to_csv(OUTPUT_FILE, index=False)
    print_report(df, OUTPUT_FILE)


if __name__ == "__main__":
    main()