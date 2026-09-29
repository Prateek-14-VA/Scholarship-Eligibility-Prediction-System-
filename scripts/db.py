"""
Database helper functions for the Scholarship System.
Auto-detects PostgreSQL (Render / cloud) or MySQL (local dev).
"""

import os
from pathlib import Path

# ---- Detect which DB to use ----
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import psycopg2
    import psycopg2.extras

    USE_POSTGRES = True

    def get_connection():
        return psycopg2.connect(DATABASE_URL)

    def _cursor_dict(conn):
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

else:
    import mysql.connector
    from mysql.connector import Error as MySQLError

    USE_POSTGRES = False

    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "2004",
        "database": "scholarship_db",
    }

    def get_connection():
        return mysql.connector.connect(**DB_CONFIG)

    def _cursor_dict(conn):
        return conn.cursor(dictionary=True)


def save_prediction(student, prediction, recommendations):
    """Save or update student + prediction + recommendations."""
    try:
        conn = get_connection()
        cursor = _cursor_dict(conn)

        cursor.execute(
            "SELECT id FROM students WHERE name = %s LIMIT 1",
            (student["name"],)
        )
        existing = cursor.fetchone()

        if existing:
            student_id = existing["id"]
            cursor.execute("""
                UPDATE students
                SET age=%s, gender=%s, category=%s, disability=%s,
                    education=%s, marks=%s, attendance=%s, income=%s
                WHERE id=%s
            """, (
                student["age"], student["gender"], student["category"],
                student["disability"], student["education"],
                student["marks"], student["attendance"],
                student["income"], student_id,
            ))
            cursor.execute("DELETE FROM predictions WHERE student_id = %s", (student_id,))
        else:
            cursor.execute("""
                INSERT INTO students
                    (name, age, gender, category, disability, education, marks, attendance, income)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                student["name"], student["age"], student["gender"],
                student["category"], student["disability"],
                student["education"], student["marks"],
                student["attendance"], student["income"],
            ))
            if USE_POSTGRES:
                cursor.execute("SELECT lastval() AS id")
                student_id = cursor.fetchone()["id"]
            else:
                student_id = cursor.lastrowid

                        # PostgreSQL uses TRUE/FALSE, MySQL uses 1/0
        if USE_POSTGRES:
            eligible_val = bool(prediction["eligible"])
        else:
            eligible_val = 1 if prediction["eligible"] else 0

        cursor.execute("""
            INSERT INTO predictions (student_id, eligible, score)
            VALUES (%s, %s, %s)
        """, (
            student_id,
            eligible_val,
            prediction["score"],
        ))
        if USE_POSTGRES:
            cursor.execute("SELECT lastval() AS id")
            prediction_id = cursor.fetchone()["id"]
        else:
            prediction_id = cursor.lastrowid

        for rec in recommendations:
            cursor.execute("""
                INSERT INTO recommendations
                    (prediction_id, scholarship_name, provider, amount, portal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                prediction_id, rec["name"], rec["provider"],
                rec["amount"], rec["portal"],
            ))

        conn.commit()
        cursor.close()
        conn.close()
        return student_id

    except Exception as e:
        print(f"Database error in save_prediction: {e}")
        return None


def get_all_predictions(limit=50):
    """Return recent predictions joined with student info."""
    try:
        conn = get_connection()
        cursor = _cursor_dict(conn)
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
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Database error in get_all_predictions: {e}")
        return []


def get_stats():
    """Return aggregate stats."""
    try:
        conn = get_connection()
        cursor = _cursor_dict(conn)

        cursor.execute("SELECT COUNT(*) AS total FROM predictions")
        total = cursor.fetchone()["total"]

        if USE_POSTGRES:
            cursor.execute("SELECT COUNT(*) AS c FROM predictions WHERE eligible = TRUE")
        else:
            cursor.execute("SELECT COUNT(*) AS c FROM predictions WHERE eligible = 1")
        eligible = cursor.fetchone()["c"]

        cursor.execute("SELECT AVG(score) AS avg_score FROM predictions")
        avg_score = cursor.fetchone()["avg_score"] or 0

        cursor.close()
        conn.close()

        return {
            "total": int(total),
            "eligible": int(eligible),
            "not_eligible": int(total - eligible),
            "avg_score": round(float(avg_score), 2),
        }
    except Exception as e:
        print(f"Database error in get_stats: {e}")
        return {"total": 0, "eligible": 0, "not_eligible": 0, "avg_score": 0}


def delete_prediction(prediction_id):
    """Delete a prediction."""
    try:
        conn = get_connection()
        cursor = _cursor_dict(conn)
        cursor.execute("DELETE FROM predictions WHERE id = %s", (prediction_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error in delete_prediction: {e}")
        return False


def clear_all_history():
    """Delete all data."""
    try:
        conn = get_connection()
        cursor = _cursor_dict(conn)
        cursor.execute("DELETE FROM recommendations")
        cursor.execute("DELETE FROM predictions")
        cursor.execute("DELETE FROM students")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error in clear_all_history: {e}")
        return False


def search_predictions(name_query="", category="", eligible_filter=""):
    """Search predictions with filters."""
    try:
        conn = get_connection()
        cursor = _cursor_dict(conn)

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
            if USE_POSTGRES:
                params.append(eligible_filter == "1")
            else:
                params.append(int(eligible_filter))

        query += " ORDER BY p.created_at DESC LIMIT 200"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Database error in search_predictions: {e}")
        return []