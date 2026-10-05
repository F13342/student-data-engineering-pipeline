def extract_postgresql(connection):
    query = """
        SELECT
            e.student_id,
            e.course_code,
            c.course_name,
            c.credit_hours,
            e.semester
        FROM enrollments e
        JOIN courses c
            ON c.course_code = e.course_code
        ORDER BY e.student_id, e.course_code
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = [
        "student_id",
        "course_code",
        "course_name",
        "credit_hours",
        "semester",
    ]

    return [dict(zip(columns, row)) for row in rows]