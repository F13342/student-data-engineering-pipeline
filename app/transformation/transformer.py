def performance_level(gpa, score):
    if gpa >= 3.5 and score >= 85:
        return "Excellent"
    if gpa >= 3.0 and score >= 70:
        return "Good"
    if gpa >= 2.0 and score >= 50:
        return "Satisfactory"
    return "Needs Improvement"


def attendance_status(attendance):
    if attendance >= 90:
        return "Excellent"
    if attendance >= 75:
        return "Acceptable"
    return "Low"


def transform(rows):
    output = []
    for row in rows:
        item = dict(row)
        item["performance_level"] = performance_level(float(item["gpa"]), float(item["score"]))
        item["attendance_status"] = attendance_status(float(item["attendance"]))
        output.append(item)
    return output
