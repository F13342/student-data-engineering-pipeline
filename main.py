from pathlib import Path
from threading import Thread

from app.database.mongodb import (
    get_mongodb_client,
    get_mongodb_database,
)
from app.database.postgresql import get_postgresql_connection
from app.output.csv_export import export_to_csv
from app.output.mongodb_loader import load_final_records
from app.output.sqlite_export import export_to_sqlite
from app.pipelines.integration_pipeline import run_integration_pipeline
from app.utils.logger import get_logger
from mock_api.server import create_server


CSV_FILE = Path("data/raw/students.csv")
API_URL = "http://127.0.0.1:8765/students"
WEB_URL = "http://127.0.0.1:8765/web-students"

SQLITE_EXPORT = Path(
    "data/exports/final_dataset.db"
)

CSV_EXPORT = Path(
    "data/exports/final_dataset.csv"
)


def main():
    logger = get_logger()

    server = create_server()
    thread = Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    postgres = get_postgresql_connection()
    mongo_client = get_mongodb_client()

    try:
        mongo_db = get_mongodb_database(mongo_client)

        result = run_integration_pipeline(
            csv_path=CSV_FILE,
            api_url=API_URL,
            web_url=WEB_URL,
            postgresql_connection=postgres,
            mongodb_collection=mongo_db["student_courses"],
        )

        print(f"Final valid: {len(result.valid)}")
        print(f"Total rejected: {len(result.rejected)}")

        final_collection = mongo_db["students"]

        loaded = load_final_records(
            final_collection,
            result.valid,
        )

        export_to_sqlite(
            SQLITE_EXPORT,
            result.valid,
        )

        export_to_csv(
            CSV_EXPORT,
            result.valid,
        )

        logger.info(
            "Final MongoDB load completed: %d records",
            loaded,
        )

        print(f"MongoDB collection: students")
        print(f"SQLite export: {SQLITE_EXPORT}")
        print(f"CSV export: {CSV_EXPORT}")

    finally:
        postgres.close()
        mongo_client.close()
        server.shutdown()


if __name__ == "__main__":
    main()