import sqlite3
from app.utils.paths import DB_FILE

def get_connection():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database(conn):
    conn.executescript((DB_FILE.parent / "schema.sql").read_text(encoding="utf-8"))
    conn.execute("DELETE FROM courses")
    conn.execute("DELETE FROM enrollments")
    conn.executemany("INSERT INTO courses(course_code, course_name, credit_hours) VALUES (?, ?, ?)", [("CS101","Programming",3),("CS102","Data Engineering",3),("IS101","Information Systems",3)])
    conn.executemany("INSERT INTO enrollments(student_id, course_code, semester) VALUES (?, ?, ?)", [("S001","CS101","2026-1"),("S002","CS101","2026-1"),("S003","IS101","2026-1"),("S004","CS102","2026-1"),("S005","CS101","2026-1")])
    conn.commit()
