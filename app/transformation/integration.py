def index_unique(rows, key):
    result = {}
    for row in rows:
        result[row[key]] = row
    return result


def integrate(csv_rows, api_rows, db_rows):
    csv_index = index_unique(csv_rows, "student_id")
    api_index = index_unique(api_rows, "student_id")
    db_index = index_unique(db_rows, "student_id")

    rows = []
    rejected = []

    all_ids = sorted(set(csv_index) | set(api_index) | set(db_index))

    for student_id in all_ids:
        if (
            student_id not in csv_index
            or student_id not in api_index
            or student_id not in db_index
        ):
            missing = [
                name
                for name, index in (
                    ("CSV", csv_index),
                    ("API", api_index),
                    ("SQLite", db_index),
                )
                if student_id not in index
            ]

            rejected.append(
                {
                    "student_id": student_id,
                    "reason": "Missing source record: " + ", ".join(missing),
                }
            )
            continue

        rows.append(
            {
                **csv_index[student_id],
                **api_index[student_id],
                **db_index[student_id],
            }
        )

    return rows, rejected


def integrate_all(
    csv_rows,
    api_rows,
    web_rows,
    postgresql_rows,
    mongodb_rows,
):
    """
    Integrate all source-specific datasets.

    PostgreSQL and MongoDB both provide course information.
    Their course information must agree before the record is accepted.
    """
    csv_index = index_unique(csv_rows, "student_id")
    api_index = index_unique(api_rows, "student_id")
    web_index = index_unique(web_rows, "student_id")
    postgres_index = index_unique(postgresql_rows, "student_id")
    mongo_index = index_unique(mongodb_rows, "student_id")

    rows = []
    rejected = []

    all_ids = sorted(
        set(csv_index)
        | set(api_index)
        | set(web_index)
        | set(postgres_index)
        | set(mongo_index)
    )

    for student_id in all_ids:
        indexes = (
            ("CSV", csv_index),
            ("API", api_index),
            ("Web Scraping", web_index),
            ("PostgreSQL", postgres_index),
            ("MongoDB", mongo_index),
        )

        missing = [
            name
            for name, index in indexes
            if student_id not in index
        ]

        if missing:
            rejected.append(
                {
                    "student_id": student_id,
                    "reason": "Missing source record: " + ", ".join(missing),
                }
            )
            continue

        csv_row = csv_index[student_id]
        web_row = web_index[student_id]
        postgres_row = postgres_index[student_id]
        mongo_row = mongo_index[student_id]

        if (
            postgres_row.get("course_code")
            != mongo_row.get("course_code")
        ):
            rejected.append(
                {
                    "student_id": student_id,
                    "reason": "PostgreSQL/MongoDB course mismatch",
                }
            )
            continue

        if (
            postgres_row.get("course_name")
            != mongo_row.get("course_name")
        ):
            rejected.append(
                {
                    "student_id": student_id,
                    "reason": "PostgreSQL/MongoDB course name mismatch",
                }
            )
            continue

        rows.append(
            {
                **csv_row,
                **web_row,
                **api_index[student_id],
                **postgres_row,
            }
        )

    return rows, rejected