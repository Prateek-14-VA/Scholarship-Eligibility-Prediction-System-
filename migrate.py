"""
One-time migration script: adds 'course' column to Render PostgreSQL.
"""
import psycopg2

# ⚠️ REPLACE this with the FULL External Database URL from Render
# It should look like: postgresql://scholarship_user:PASSWORD@dpg-xxxxx.oregon-postgres.render.com/scholarship_db_26ew
DATABASE_URL = "postgresql://scholarship_user:79CLmbCyKzzr84SFB3EUqHb6CAThjeTH@dpg-datk6anlot8c73ft4jrg-a.oregon-postgres.render.com/scholarship_db_26ew"

print("Connecting to database...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN course VARCHAR(50) NOT NULL DEFAULT 'Not Specified'
    """)
    conn.commit()
    print("✅ Column 'course' added successfully!")
except Exception as e:
    print(f"⚠️ Error (column may already exist): {e}")
    conn.rollback()

# Verify
cursor.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'students'
    ORDER BY ordinal_position
""")
cols = [row[0] for row in cursor.fetchall()]
print("Columns in 'students' table:", cols)

cursor.close()
conn.close()