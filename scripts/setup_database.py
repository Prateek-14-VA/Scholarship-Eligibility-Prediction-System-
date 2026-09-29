"""
Setup database schema for both MySQL (local) and PostgreSQL (Render).
"""

import os

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import psycopg2
    DB_TYPE = "PostgreSQL"
else:
    import mysql.connector
    DB_TYPE = "MySQL"


def create_tables():
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
    else:
        conn = mysql.connector.connect(
            host="localhost", user="root",
            password="2004", database="scholarship_db"
        )
        cursor = conn.cursor()

    if DATABASE_URL:
        # PostgreSQL syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                category VARCHAR(20) NOT NULL,
                disability VARCHAR(5) NOT NULL,
                education VARCHAR(20) NOT NULL,
                marks FLOAT NOT NULL,
                attendance FLOAT NOT NULL,
                income INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                eligible BOOLEAN NOT NULL,
                score FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id SERIAL PRIMARY KEY,
                prediction_id INT NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
                scholarship_name VARCHAR(255) NOT NULL,
                provider VARCHAR(100) NOT NULL,
                amount INT NOT NULL,
                portal VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        # MySQL syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                category VARCHAR(20) NOT NULL,
                disability VARCHAR(5) NOT NULL,
                education VARCHAR(20) NOT NULL,
                marks FLOAT NOT NULL,
                attendance FLOAT NOT NULL,
                income INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                eligible TINYINT(1) NOT NULL,
                score FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                prediction_id INT NOT NULL,
                scholarship_name VARCHAR(255) NOT NULL,
                provider VARCHAR(100) NOT NULL,
                amount INT NOT NULL,
                portal VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE
            )
        """)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Tables created successfully in {DB_TYPE}")


if __name__ == "__main__":
    print(f"Setting up database: {DB_TYPE}")
    create_tables()