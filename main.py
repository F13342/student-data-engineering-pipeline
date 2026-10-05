from threading import Thread

from app.database.connection import get_connection, initialize_database
from app.etl.pipeline import run_pipeline
from app.utils.paths import PROCESSED_DIR, REJECTED_DIR, LOG_FILE
from mock_api.server import create_server


def main():
    server = create_server()
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    conn = get_connection()
    try:
        initialize_database(conn)
        result = run_pipeline(conn, "http://127.0.0.1:8765/students")
        print(f"Valid records: {len(result.valid)}")
        print(f"Rejected records: {len(result.rejected)}")
        print(f"Final dataset: {PROCESSED_DIR / 'final_dataset.csv'}")
        print(f"Rejected records: {REJECTED_DIR / 'rejected_records.csv'}")
        print(f"Log: {LOG_FILE}")
    finally:
        conn.close(); server.shutdown()

if __name__ == "__main__":
    main()
