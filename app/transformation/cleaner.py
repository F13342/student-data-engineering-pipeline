def clean_text(value):
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def clean_city(value):
    value = clean_text(value).lower().replace("’", "\'")
    if value in {"sanaa", "sana’a", "sana\'a"}:
        return "Sanaa"
    return value.title()


def clean_student_row(row):
    cleaned = dict(row)
    for key in ("student_id", "student_name", "major"):
        cleaned[key] = clean_text(cleaned.get(key))
    cleaned["city"] = clean_city(cleaned.get("city"))
    return cleaned


def clean_api_row(row):
    cleaned = dict(row)
    cleaned["student_id"] = clean_text(cleaned.get("student_id"))
    if cleaned.get("status") is not None:
        cleaned["status"] = clean_text(cleaned["status"]).lower()
    return cleaned
