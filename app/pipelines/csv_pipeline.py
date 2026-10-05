from pathlib import Path

from app.sources.csv_source import extract_csv
from app.transformation.cleaner import clean_student_row
from app.validation.quality import validate_source_rows
from app.transformation.pipeline_result import PipelineResult
from app.utils.logger import get_logger


def run_csv_pipeline(file_path: Path) -> PipelineResult:
    """
    Run the CSV-specific data pipeline.

    Steps:
        1. Extract data from CSV.
        2. Validate source records.
        3. Clean valid records.
        4. Return prepared records and rejected records.
    """
    logger = get_logger()
    logger.info("CSV pipeline started")

    # 1. Extract
    raw_rows = extract_csv(file_path)
    logger.info("CSV extracted: %d records", len(raw_rows))

    # 2. Source validation
    valid_rows, rejected_rows = validate_source_rows(raw_rows, "CSV")
    logger.info(
        "CSV validation completed: valid=%d rejected=%d",
        len(valid_rows),
        len(rejected_rows),
    )

    # 3. Clean
    cleaned_rows = [
        clean_student_row(row)
        for row in valid_rows
    ]

    logger.info("CSV transformation completed: %d records", len(cleaned_rows))
    logger.info("CSV pipeline completed")

    return PipelineResult(
        valid=cleaned_rows,
        rejected=rejected_rows,
    )