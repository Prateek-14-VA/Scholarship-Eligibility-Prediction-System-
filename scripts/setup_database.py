"""
Creates the MySQL database and tables for the
Scholarship Eligibility Prediction System.
"""

import mysql.connector
from mysql.connector import Error

# Database config — CHANGE the password to your MySQL password
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "2004",   
}

DB_NAME = "scholarship_db"


def create_database():
    """Create the database if it doesn't exist."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database '{DB_NAME}' ready.")
    cursor.close()
    conn.close()


def create_tables():
    """Create all tables."""
    conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
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
    print("Table 'students' ready.")

    # Predictions table
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
    print("Table 'predictions' ready.")

    # Recommendations table
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
    print("Table 'recommendations' ready.")

    cursor.close()
    conn.close()


def main():
    print("=" * 55)
    print("  SETTING UP MYSQL DATABASE")
    print("=" * 55)
    create_database()
    create_tables()
    print()
    print("=" * 55)
    print("  DATABASE SETUP COMPLETE")
    print("=" * 55)


if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Is MySQL running?")
        print("  2. Is the password in DB_CONFIG correct?")
        print("  3. Is MySQL port 3306 free?")