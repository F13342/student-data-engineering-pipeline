from app.sources.postgresql_source import extract_postgresql
from app.transformation.cleaner import clean_mongodb_row
from app.transformation.pipeline_result import PipelineResult
from app.utils.logger import get_logger
from app.validation.quality import validate_source_rows


def run_postgresql_pipeline(connection) -> PipelineResult:
    logger = get_logger()
    logger.info("PostgreSQL pipeline started")

    raw_rows = extract_postgresql(connection)

    valid_rows, rejected_rows = validate_source_rows(
        raw_rows,
        "PostgreSQL",
    )

    cleaned_rows = [
        clean_mongodb_row(row)
        for row in valid_rows
    ]

    logger.info(
        "PostgreSQL pipeline completed: valid=%d rejected=%d",
        len(cleaned_rows),
        len(rejected_rows),
    )

    return PipelineResult(
        valid=cleaned_rows,
        rejected=rejected_rows,
    )