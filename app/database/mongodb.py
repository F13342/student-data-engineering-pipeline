import os

from pymongo import MongoClient
from pymongo.database import Database


DEFAULT_MONGODB_URI = "mongodb://localhost:27017/"
DEFAULT_DATABASE_NAME = "student_data_engineering"


def get_mongodb_client() -> MongoClient:
    """
    Create a MongoDB client using an environment variable when available.
    """
    uri = os.getenv("MONGODB_URI", DEFAULT_MONGODB_URI)

    return MongoClient(
        uri,
        serverSelectionTimeoutMS=3000,
    )


def get_mongodb_database(client: MongoClient) -> Database:
    """
    Return the application MongoDB database.
    """
    database_name = os.getenv(
        "MONGODB_DATABASE",
        DEFAULT_DATABASE_NAME,
    )

    return client[database_name]


def check_mongodb_connection(client: MongoClient) -> None:
    """
    Verify that MongoDB is reachable.
    """
    client.admin.command("ping")