from pymongo import UpdateOne
from pymongo.collection import Collection


def load_final_records(
    collection: Collection,
    rows: list[dict],
) -> int:
    """Load final validated records into MongoDB using upsert."""
    collection.create_index("student_id", unique=True)

    if not rows:
        return 0

    operations = [
        UpdateOne(
            {"student_id": row["student_id"]},
            {"$set": row},
            upsert=True,
        )
        for row in rows
    ]

    result = collection.bulk_write(operations)
    return result.upserted_count + result.modified_count