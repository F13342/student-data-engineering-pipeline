import sqlite3


def extract_database(connection: sqlite3.Connection):
    query = """
    SELECT e.student_id, e.course_code, c.course_name, c.credit_hours, e.semester
    FROM enrollments e
    JOIN courses c ON c.course_code = e.course_code
    ORDER BY e.student_id, e.course_code
    """
    return [dict(row) for row in connection.execute(query).fetchall()]
