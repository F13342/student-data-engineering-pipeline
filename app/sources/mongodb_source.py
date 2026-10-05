from typing import Any

from pymongo.collection import Collection


def extract_mongodb(
    collection: Collection,
    query: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Extract documents from a MongoDB collection."""
    documents = collection.find(
        query or {},
        {"_id": 0},
    )

    return list(documents)
