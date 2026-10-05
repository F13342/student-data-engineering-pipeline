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
        if student_id not in csv_index or student_id not in api_index or student_id not in db_index:
            missing = [name for name, index in (("CSV", csv_index), ("API", api_index), ("SQLite", db_index)) if student_id not in index]
            rejected.append({"student_id": student_id, "reason": "Missing source record: " + ", ".join(missing)})
            continue
        rows.append({**csv_index[student_id], **api_index[student_id], **db_index[student_id]})
    return rows, rejected
