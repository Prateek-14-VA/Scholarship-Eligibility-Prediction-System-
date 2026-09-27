"""
Scholarship Recommendation Engine.
Matches a student profile against Indian scholarship schemes.
"""

import pandas as pd
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
SCHOLARSHIPS_FILE = DATA_DIR / "scholarships.csv"

# Fallback amount for "Scheme-specific" entries
DEFAULT_AMOUNT = 25000


# Load scholarships database once
def load_scholarships():
    return pd.read_csv(SCHOLARSHIPS_FILE)


# Get eligible scholarships for a student
def recommend_scholarships(student):
    """
    student = {
        "age", "gender", "category", "disability",
        "education", "marks", "attendance", "income"
    }
    Returns a list of matching scholarships.
    """
    df = load_scholarships()
    matches = []

    for _, scheme in df.iterrows():
        # Education filter
        if scheme["education"] != "Any" and scheme["education"] != student["education"]:
            continue

        # Category filter
        if scheme["category"] != "Any" and scheme["category"] != student["category"]:
            continue

        # Gender filter
        if scheme["gender"] != "Any" and scheme["gender"] != student["gender"]:
            continue

        # Disability filter
        if scheme["disability"] != "Any" and scheme["disability"] != student["disability"]:
            continue

        # Income check
        if student["income"] > scheme["income_limit"]:
            continue

        # Marks check
        if student["marks"] < scheme["min_marks"]:
            continue

        # Parse amount
        try:
            amount_val = int(scheme["amount"])
        except (ValueError, TypeError):
            amount_val = DEFAULT_AMOUNT

        matches.append({
            "name": scheme["name"],
            "provider": scheme["provider"],
            "amount": amount_val,
            "amount_display": scheme["amount"],
            "portal": scheme["portal"],
        })

    # Remove duplicates by name
    seen = set()
    unique_matches = []
    for m in matches:
        if m["name"] not in seen:
            seen.add(m["name"])
            unique_matches.append(m)

    return unique_matches


# Sum of awards
def total_award(scholarships):
    return sum(s["amount"] for s in scholarships)


# Test when run directly
if __name__ == "__main__":
    test_student = {
        "age": 24,
        "gender": "Female",
        "category": "SC",
        "disability": "No",
        "education": "Professional",
        "marks": 75.0,
        "attendance": 85.0,
        "income": 200000,
    }

    results = recommend_scholarships(test_student)

    print("=" * 70)
    print("  SCHOLARSHIP RECOMMENDATION TEST")
    print("=" * 70)
    print(f"  Student: {test_student['category']}, {test_student['gender']}, "
          f"{test_student['education']}")
    print(f"           Marks={test_student['marks']}, "
          f"Income=Rs. {test_student['income']:,}")
    print()

    if not results:
        print("  No matching scholarships found.")
    else:
        for i, s in enumerate(results, 1):
            print(f"  {i}. {s['name']}")
            print(f"     Provider: {s['provider']}")
            print(f"     Amount:   {s['amount_display']}")
            print(f"     Portal:   {s['portal']}")
            print()

        print(f"  Total estimated award: Rs. {total_award(results):,}")
    print("=" * 70)