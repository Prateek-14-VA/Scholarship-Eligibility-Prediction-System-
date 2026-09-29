"""
Flask web application for Scholarship Eligibility Prediction System.
"""
import os
import sys
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, Response

# Add scripts folder to import path
SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from predictor import predict_student
from recommend import recommend_scholarships, total_award
from db import (
    save_prediction, get_all_predictions, get_stats,
    delete_prediction, clear_all_history, search_predictions
)

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
    """Show prediction history with optional search/filter."""
    name_query = request.args.get("name", "").strip()
    category = request.args.get("category", "").strip()
    eligible = request.args.get("eligible", "").strip()

    if name_query or category or eligible:
        predictions = search_predictions(name_query, category, eligible)
    else:
        predictions = get_all_predictions(limit=200)

    return render_template(
        "history.html",
        predictions=predictions,
        name_query=name_query,
        category_filter=category,
        eligible_filter=eligible,
    )


@app.route("/delete/<int:prediction_id>", methods=["POST"])
def delete_record(prediction_id):
    """Delete a single prediction."""
    delete_prediction(prediction_id)
    return redirect(url_for("history"))


@app.route("/clear_history", methods=["POST"])
def clear_history():
    """Delete all history."""
    clear_all_history()
    return redirect(url_for("history"))


@app.route("/export_csv")
def export_csv():
    """Download history as CSV."""
    predictions = get_all_predictions(limit=1000)

    lines = ["Date,Name,Age,Gender,Category,Education,Marks,Attendance,Income,Eligible,Score"]
    for p in predictions:
        date_str = p["created_at"].strftime("%Y-%m-%d %H:%M") if p["created_at"] else ""
        lines.append(
            f'{date_str},{p["name"]},{p["age"]},{p["gender"]},{p["category"]},'
            f'{p["education"]},{p["marks"]},{p["attendance"]},{p["income"]},'
            f'{"Yes" if p["eligible"] else "No"},{p["score"]}'
        )

    csv_content = "\n".join(lines)
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=history.csv"}
    )

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)