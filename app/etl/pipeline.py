from app.sources.csv_source import extract_csv
from app.sources.api_source import extract_api
from app.sources.database_source import extract_database
from app.transformation.cleaner import clean_student_row, clean_api_row
from app.transformation.integration import integrate
from app.transformation.transformer import transform
from app.validation.quality import validate_and_split, validate_source_rows
from app.output.csv_writer import write_csv
from app.utils.paths import RAW_DIR, PROCESSED_DIR, REJECTED_DIR
from app.utils.logger import get_logger
from app.transformation.pipeline_result import PipelineResult


def run_pipeline(connection, api_url):
    logger = get_logger()
    logger.info("Pipeline started")

    # 1) Extract
    csv_raw = extract_csv(RAW_DIR / "students.csv")
    api_raw = extract_api(api_url)
    db_raw = extract_database(connection)
    logger.info("Extracted CSV=%d API=%d SQLite=%d", len(csv_raw), len(api_raw), len(db_raw))

    # 2) Validate source records
    csv_rows, rej_csv = validate_source_rows(csv_raw, "CSV")
    api_rows, rej_api = validate_source_rows(api_raw, "API")
    db_rows, rej_db = validate_source_rows(db_raw, "SQLite")

    # 3) Clean
    csv_rows = [clean_student_row(r) for r in csv_rows]
    api_rows = [clean_api_row(r) for r in api_rows]

    # 4) Integrate
    integrated, rej_integration = integrate(csv_rows, api_rows, db_rows)

    # 5) Transform
    transformed = transform(integrated)

    # 6) Final Validation
    valid, rej_validation = validate_and_split(transformed)

    rejected = rej_csv + rej_api + rej_db + rej_integration + rej_validation
    final_path = write_csv(PROCESSED_DIR / "final_dataset.csv", valid)
    rejected_path = write_csv(REJECTED_DIR / "rejected_records.csv", rejected)
    logger.info("Final validation: valid=%d rejected=%d", len(valid), len(rejected))
    logger.info("Loaded %s and %s", final_path, rejected_path)
    logger.info("Pipeline completed")
    return PipelineResult(valid=valid, rejected=rejected)
