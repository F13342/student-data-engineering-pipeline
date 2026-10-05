import sqlite3
from pathlib import Path


COLUMNS = [
    "student_id",
    "student_name",
    "age",
    "major",
    "city",
    "gpa",
    "attendance",
    "score",
    "status",
    "course_code",
    "course_name",
    "credit_hours",
    "semester",
    "performance_level",
    "attendance_status",
]


def export_to_sqlite(
    database_path: Path,
    rows: list[dict],
) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("DROP TABLE IF EXISTS students")

        connection.execute(
            """
            CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                student_name TEXT NOT NULL,
                age INTEGER,
                major TEXT,
                city TEXT,
                gpa REAL,
                attendance REAL,
                score REAL,
                status TEXT,
                course_code TEXT,
                course_name TEXT,
                credit_hours INTEGER,
                semester TEXT,
                performance_level TEXT,
                attendance_status TEXT
            )
            """
        )

        placeholders = ", ".join(["?"] * len(COLUMNS))

        values = [
            tuple(row.get(column) for column in COLUMNS)
            for row in rows
        ]

        connection.executemany(
            f"""
            INSERT INTO students ({", ".join(COLUMNS)})
            VALUES ({placeholders})
            """,
            values,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()