"""
Flask web application for Scholarship Eligibility Prediction System.
"""

import sys
import json
from pathlib import Path
from flask import Flask, render_template, request

# Add scripts folder to import path
SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from predictor import predict_student
from recommend import recommend_scholarships, total_award
from db import save_prediction, get_all_predictions, get_stats

app = Flask(__name__)


@app.route("/")
def home():
    """Show the student input form."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Handle form submission, save to DB, and show results."""
    student = {
        "name": request.form["name"].strip(),
        "age": int(request.form["age"]),
        "gender": request.form["gender"],
        "category": request.form["category"],
        "disability": request.form["disability"],
        "education": request.form["education"],
        "marks": float(request.form["marks"]),
        "attendance": float(request.form["attendance"]),
        "income": int(request.form["income"]),
    }
    prediction = predict_student(student)
    recommendations = recommend_scholarships(student)
    total = total_award(recommendations)

    # Save to database
    save_prediction(student, prediction, recommendations)

    return render_template(
        "result.html",
        student=student,
        prediction=prediction,
        recommendations=recommendations,
        total=total,
    )


@app.route("/dashboard")
def dashboard():
    """Analytics dashboard with charts."""
    from dashboard_data import get_all_dashboard_data
    data = get_all_dashboard_data()
    return render_template(
        "dashboard.html",
        summary=data["summary"],
        chart_data=json.dumps(data)
    )

@app.route("/history")
def history():
    """Show recent prediction history."""
    predictions = get_all_predictions(limit=100)
    return render_template("history.html", predictions=predictions)


@app.route("/admin")
def admin():
    """Admin stats panel."""
    stats = get_stats()
    return render_template("admin.html", stats=stats)

@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")

@app.route("/scholarships")
def scholarships():
    """List all available scholarships."""
    import pandas as pd
    from pathlib import Path
    df = pd.read_csv(Path(__file__).parent / "data" / "scholarships.csv")
    return render_template("scholarships.html", scholarships=df.to_dict("records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)