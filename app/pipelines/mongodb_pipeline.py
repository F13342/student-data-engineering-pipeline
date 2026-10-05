from pymongo.collection import Collection

from app.sources.mongodb_source import extract_mongodb
from app.transformation.cleaner import clean_mongodb_row
from app.transformation.pipeline_result import PipelineResult
from app.utils.logger import get_logger
from app.validation.quality import validate_source_rows


def run_mongodb_pipeline(collection: Collection) -> PipelineResult:
    """
    Run the MongoDB-specific source pipeline.

    Steps:
        1. Extract documents from MongoDB.
        2. Validate source records.
        3. Clean valid records.
        4. Return prepared and rejected records.
    """
    logger = get_logger()
    logger.info("MongoDB pipeline started")

    # 1. Extract
    raw_rows = extract_mongodb(collection)
    logger.info("MongoDB extracted: %d records", len(raw_rows))

    # 2. Source validation
    valid_rows, rejected_rows = validate_source_rows(
        raw_rows,
        "MongoDB",
    )

    logger.info(
        "MongoDB validation completed: valid=%d rejected=%d",
        len(valid_rows),
        len(rejected_rows),
    )

    # 3. Clean
    cleaned_rows = [
        clean_mongodb_row(row)
        for row in valid_rows
    ]

    logger.info(
        "MongoDB transformation completed: %d records",
        len(cleaned_rows),
    )

    logger.info("MongoDB pipeline completed")

    return PipelineResult(
        valid=cleaned_rows,
        rejected=rejected_rows,
    )