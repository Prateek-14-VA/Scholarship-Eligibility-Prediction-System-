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
    """Handle form submission with validation, save to DB, show results."""
    try:
        name = request.form.get("name", "").strip()
        age = int(request.form.get("age", 0))
        gender = request.form.get("gender", "")
        category = request.form.get("category", "")
        disability = request.form.get("disability", "")
        education = request.form.get("education", "")
        marks = float(request.form.get("marks", 0))
        attendance = float(request.form.get("attendance", 0))
        income = int(request.form.get("income", 0))

        # Validation rules
        errors = []
        if not name or len(name) < 2:
            errors.append("Name must be at least 2 characters.")
        if age < 15 or age > 60:
            errors.append("Age must be between 15 and 60.")
        if marks < 0 or marks > 100:
            errors.append("Marks must be between 0 and 100.")
        if attendance < 0 or attendance > 100:
            errors.append("Attendance must be between 0 and 100.")
        if income < 0:
            errors.append("Income must be a positive number.")

        if errors:
            return render_template("index.html", errors=errors), 400

        student = {
            "name": name,
            "age": age,
            "gender": gender,
            "category": category,
            "disability": disability,
            "education": education,
            "marks": marks,
            "attendance": attendance,
            "income": income,
        }

        prediction = predict_student(student)
        recommendations = recommend_scholarships(student)
        total = total_award(recommendations)

        save_prediction(student, prediction, recommendations)

        return render_template(
            "result.html",
            student=student,
            prediction=prediction,
            recommendations=recommendations,
            total=total,
        )

    except ValueError:
        return render_template(
            "index.html",
            errors=["Invalid input: please check all fields."]
        ), 400
    except Exception as e:
        print(f"Error in predict: {e}")
        return render_template("500.html"), 500


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

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    """Custom 500 page."""
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)