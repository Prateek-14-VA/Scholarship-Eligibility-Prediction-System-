"""
End-to-end test: predict eligibility + recommend scholarships.
"""

import sys
from pathlib import Path

# Add current folder to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from predictor import predict_student
from recommend import recommend_scholarships, total_award


def process_student(student, name="Student"):
    prediction = predict_student(student)
    recommendations = recommend_scholarships(student)

    print("=" * 70)
    print(f"  {name}")
    print("=" * 70)
    print(f"  Profile:  Age={student['age']}, {student['category']}, "
          f"{student['gender']}, {student['education']}")
    print(f"            Marks={student['marks']}, "
          f"Attendance={student['attendance']}%, "
          f"Income=Rs. {student['income']:,}")
    print()
    print(f"  Eligibility:  {prediction['label']}")
    print(f"  Score:        {prediction['score']}%")
    print()
    print(f"  Recommended Scholarships ({len(recommendations)}):")

    if recommendations:
        for i, s in enumerate(recommendations, 1):
            print(f"    {i}. {s['name']}")
            print(f"       Provider: {s['provider']}  |  Amount: {s['amount_display']}")
        print()
        print(f"  Total estimated award: Rs. {total_award(recommendations):,}")
    else:
        print("    None")
    print()


# Priya Sharma from your synopsis
priya = {
    "age": 24, "gender": "Female", "category": "SC",
    "disability": "No", "education": "Professional",
    "marks": 75.0, "attendance": 85.0, "income": 200000,
}

# Rahul — general, high income
rahul = {
    "age": 22, "gender": "Male", "category": "General",
    "disability": "No", "education": "UG",
    "marks": 68.0, "attendance": 78.0, "income": 500000,
}

# Anita — OBC female, good profile
anita = {
    "age": 21, "gender": "Female", "category": "OBC",
    "disability": "No", "education": "UG",
    "marks": 82.0, "attendance": 90.0, "income": 180000,
}

# Suresh — disabled student
suresh = {
    "age": 23, "gender": "Male", "category": "SC",
    "disability": "Yes", "education": "Technical",
    "marks": 60.0, "attendance": 70.0, "income": 150000,
}


if __name__ == "__main__":
    for name, student in [("PRIYA", priya), ("RAHUL", rahul),
                          ("ANITA", anita), ("SURESH", suresh)]:
        process_student(student, name)