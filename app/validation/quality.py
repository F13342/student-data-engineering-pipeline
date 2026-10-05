def _number(value, field):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"invalid {field}")


def validate_record(row):
    required = ["student_id", "student_name", "age", "major", "city", "gpa", "attendance", "score", "course_code", "course_name"]
    for field in required:
        if row.get(field) in (None, ""):
            return f"missing {field}"

    if not str(row["student_id"]).strip():
        return "invalid student_id"
    try:
        age = int(row["age"])
    except (TypeError, ValueError):
        return "invalid age"
    if not 16 <= age <= 80:
        return "invalid age: must be 16-80"

    try:
        gpa = _number(row["gpa"], "GPA")
    except ValueError as exc:
        return str(exc)
    if not 0 <= gpa <= 4:
        return "invalid GPA: must be 0-4"

    try:
        attendance = _number(row["attendance"], "attendance")
    except ValueError as exc:
        return str(exc)
    if not 0 <= attendance <= 100:
        return "invalid attendance: must be 0-100"

    try:
        score = _number(row["score"], "score")
    except ValueError as exc:
        return str(exc)
    if not 0 <= score <= 100:
        return "invalid score: must be 0-100"

    return None


def validate_and_split(rows):
    valid, rejected = [], []
    seen = set()
    for row in rows:
        student_id = row.get("student_id", "")
        if student_id in seen:
            rejected.append({**row, "reason": "duplicate student_id"})
            continue
        seen.add(student_id)
        reason = validate_record(row)
        if reason:
            rejected.append({**row, "reason": reason})
        else:
            valid.append(row)
    return valid, rejected


def validate_source_record(row, source):
    if source in {"CSV", "Web Scraping"}:
        required = ["student_id", "student_name", "age", "major", "city"]
    elif source == "API":
        required = ["student_id", "gpa", "attendance", "score"]
    elif source in {"SQLite", "MongoDB", "PostgreSQL"}:
      required = ["student_id", "course_code", "course_name"]
    else:
     raise ValueError(f"Unsupported source: {source}")

    for field in required:
        if row.get(field) in (None, ""):
            return f"missing {field}"

    if source in {"CSV", "API", "Web Scraping"}:
        try:
            if source == "CSV" and not 16 <= int(row["age"]) <= 80:
                return "invalid age: must be 16-80"
        except (TypeError, ValueError):
            return "invalid age"

    if source == "API":
        try:
            gpa = float(row["gpa"])
        except (TypeError, ValueError):
            return "invalid GPA"
        if not 0 <= gpa <= 4:
            return "invalid GPA: must be 0-4"
        try:
            attendance = float(row["attendance"])
        except (TypeError, ValueError):
            return "invalid attendance"
        if not 0 <= attendance <= 100:
            return "invalid attendance: must be 0-100"
        try:
            score = float(row["score"])
        except (TypeError, ValueError):
            return "invalid score"
        if not 0 <= score <= 100:
            return "invalid score: must be 0-100"

    return None


def validate_source_rows(rows, source):
    valid, rejected = [], []
    seen = set()
    for row in rows:
        sid = row.get("student_id", "")
        reason = validate_source_record(row, source)
        if sid in seen:
            rejected.append({**row, "reason": f"duplicate record in {source}"})
        elif reason:
            rejected.append({**row, "reason": reason})
        else:
            seen.add(sid)
            valid.append(row)
    return valid, rejected
