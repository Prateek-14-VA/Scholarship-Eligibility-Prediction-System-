"""
Dashboard data generator.
Computes statistics and chart data from the student dataset.
"""

import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "students.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


def get_summary(df):
    total = len(df)
    eligible = (df["eligible"] == "Yes").sum()
    not_eligible = (df["eligible"] == "No").sum()
    return {
        "total": int(total),
        "eligible": int(eligible),
        "not_eligible": int(not_eligible),
        "eligible_pct": round(eligible / total * 100, 1),
    }


def get_category_data(df):
    grouped = df.groupby(["category", "eligible"]).size().unstack(fill_value=0)
    categories = grouped.index.tolist()
    yes_counts = grouped["Yes"].tolist() if "Yes" in grouped.columns else [0] * len(categories)
    no_counts = grouped["No"].tolist() if "No" in grouped.columns else [0] * len(categories)
    return {
        "categories": categories,
        "eligible": [int(x) for x in yes_counts],
        "not_eligible": [int(x) for x in no_counts],
    }


def get_education_data(df):
    grouped = df.groupby(["education", "eligible"]).size().unstack(fill_value=0)
    levels = grouped.index.tolist()
    yes_counts = grouped["Yes"].tolist() if "Yes" in grouped.columns else [0] * len(levels)
    no_counts = grouped["No"].tolist() if "No" in grouped.columns else [0] * len(levels)
    return {
        "levels": levels,
        "eligible": [int(x) for x in yes_counts],
        "not_eligible": [int(x) for x in no_counts],
    }


def get_gender_data(df):
    grouped = df.groupby(["gender", "eligible"]).size().unstack(fill_value=0)
    genders = grouped.index.tolist()
    yes_counts = grouped["Yes"].tolist() if "Yes" in grouped.columns else [0] * len(genders)
    no_counts = grouped["No"].tolist() if "No" in grouped.columns else [0] * len(genders)
    return {
        "genders": genders,
        "eligible": [int(x) for x in yes_counts],
        "not_eligible": [int(x) for x in no_counts],
    }


def get_marks_histogram(df):
    bins = [0, 40, 50, 60, 70, 80, 90, 100]
    labels = ["<40", "40-49", "50-59", "60-69", "70-79", "80-89", "90-100"]
    df = df.copy()
    df["marks_bin"] = pd.cut(df["marks"], bins=bins, labels=labels, right=False)

    grouped = df.groupby(["marks_bin", "eligible"], observed=True).size().unstack(fill_value=0)

    eligible_list = []
    not_eligible_list = []
    for label in labels:
        if label in grouped.index:
            eligible_list.append(int(grouped.loc[label, "Yes"]) if "Yes" in grouped.columns else 0)
            not_eligible_list.append(int(grouped.loc[label, "No"]) if "No" in grouped.columns else 0)
        else:
            eligible_list.append(0)
            not_eligible_list.append(0)

    return {
        "labels": labels,
        "eligible": eligible_list,
        "not_eligible": not_eligible_list,
    }


def get_income_brackets(df):
    bins = [0, 100000, 250000, 500000, 800000, 1500000]
    labels = ["<1L", "1L-2.5L", "2.5L-5L", "5L-8L", ">8L"]
    df = df.copy()
    df["income_bin"] = pd.cut(df["income"], bins=bins, labels=labels, right=False)

    grouped = df.groupby(["income_bin", "eligible"], observed=True).size().unstack(fill_value=0)

    eligible_list = []
    not_eligible_list = []
    for label in labels:
        if label in grouped.index:
            eligible_list.append(int(grouped.loc[label, "Yes"]) if "Yes" in grouped.columns else 0)
            not_eligible_list.append(int(grouped.loc[label, "No"]) if "No" in grouped.columns else 0)
        else:
            eligible_list.append(0)
            not_eligible_list.append(0)

    return {
        "labels": labels,
        "eligible": eligible_list,
        "not_eligible": not_eligible_list,
    }


def get_all_dashboard_data():
    df = load_data()
    return {
        "summary": get_summary(df),
        "category": get_category_data(df),
        "education": get_education_data(df),
        "gender": get_gender_data(df),
        "marks": get_marks_histogram(df),
        "income": get_income_brackets(df),
    }


if __name__ == "__main__":
    data = get_all_dashboard_data()
    print(json.dumps(data, indent=2))