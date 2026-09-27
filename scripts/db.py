"""
Database helper functions for the Scholarship System.
"""

import mysql.connector
from mysql.connector import Error
from pathlib import Path

# Database config — CHANGE PASSWORD to your MySQL password
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "2004",
    "database": "scholarship_db",
}


def get_connection():
    """Return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


def save_prediction(student, prediction, recommendations):
    """
    If a student with the same name already exists, update their record.
    Otherwise insert a new student. Old predictions are replaced.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Check if student already exists (by name)
        cursor.execute(
            "SELECT id FROM students WHERE name = %s LIMIT 1",
            (student["name"],)
        )
        existing = cursor.fetchone()

        if existing:
            # --- UPDATE existing student ---
            student_id = existing["id"]

            cursor.execute("""
                UPDATE students
                SET age=%s, gender=%s, category=%s, disability=%s,
                    education=%s, marks=%s, attendance=%s, income=%s
                WHERE id=%s
            """, (
                student["age"],
                student["gender"],
                student["category"],
                student["disability"],
                student["education"],
                student["marks"],
                student["attendance"],
                student["income"],
                student_id,
            ))

            # Delete old predictions for this student
            cursor.execute(
                "DELETE FROM predictions WHERE student_id = %s",
                (student_id,)
            )

        else:
            # --- INSERT new student ---
            cursor.execute("""
                INSERT INTO students
                    (name, age, gender, category, disability, education, marks, attendance, income)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                student["name"],
                student["age"],
                student["gender"],
                student["category"],
                student["disability"],
                student["education"],
                student["marks"],
                student["attendance"],
                student["income"],
            ))
            student_id = cursor.lastrowid

        # 2. Insert new prediction
        cursor.execute("""
            INSERT INTO predictions (student_id, eligible, score)
            VALUES (%s, %s, %s)
        """, (
            student_id,
            1 if prediction["eligible"] else 0,
            prediction["score"],
        ))
        prediction_id = cursor.lastrowid

        # 3. Insert recommendations
        for rec in recommendations:
            cursor.execute("""
                INSERT INTO recommendations
                    (prediction_id, scholarship_name, provider, amount, portal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                prediction_id,
                rec["name"],
                rec["provider"],
                rec["amount"],
                rec["portal"],
            ))

        conn.commit()
        cursor.close()
        conn.close()
        return student_id

    except Error as e:
        print(f"Database error: {e}")
        return None

def get_all_predictions(limit=50):
    """Return recent predictions joined with student info."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id AS prediction_id,
                s.id AS student_id,
                s.name,
                s.age, s.gender, s.category, s.education,
                s.marks, s.attendance, s.income,
                p.eligible, p.score, p.created_at
            FROM predictions p
            JOIN students s ON s.id = p.student_id
            ORDER BY p.created_at DESC
            LIMIT %s
        """, (limit,))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    except Error as e:
        print(f"Database error: {e}")
        return []


def get_stats():
    """Return aggregate stats for the admin panel."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM predictions")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS c FROM predictions WHERE eligible = 1")
        eligible = cursor.fetchone()["c"]

        cursor.execute("SELECT AVG(score) AS avg_score FROM predictions")
        avg_score = cursor.fetchone()["avg_score"] or 0

        cursor.close()
        conn.close()

        return {
            "total": total,
            "eligible": eligible,
            "not_eligible": total - eligible,
            "avg_score": round(float(avg_score), 2),
        }

    except Error as e:
        print(f"Database error: {e}")
        return {"total": 0, "eligible": 0, "not_eligible": 0, "avg_score": 0}


def delete_prediction(prediction_id):
    """Delete a prediction and its recommendations (cascade)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE id = %s", (prediction_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Database error: {e}")
        return False


def clear_all_history():
    """Delete ALL students, predictions, and recommendations."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recommendations")
        cursor.execute("DELETE FROM predictions")
        cursor.execute("DELETE FROM students")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Database error: {e}")
        return False


def search_predictions(name_query="", category="", eligible_filter=""):
    """Search predictions with optional filters."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                p.id AS prediction_id,
                s.id AS student_id,
                s.name,
                s.age, s.gender, s.category, s.education,
                s.marks, s.attendance, s.income,
                p.eligible, p.score, p.created_at
            FROM predictions p
            JOIN students s ON s.id = p.student_id
            WHERE 1=1
        """
        params = []

        if name_query:
            query += " AND s.name LIKE %s"
            params.append(f"%{name_query}%")

        if category:
            query += " AND s.category = %s"
            params.append(category)

        if eligible_filter in ("0", "1"):
            query += " AND p.eligible = %s"
            params.append(int(eligible_filter))

        query += " ORDER BY p.created_at DESC LIMIT 200"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    except Error as e:
        print(f"Database error: {e}")
        return []