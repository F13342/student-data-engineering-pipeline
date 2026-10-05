from app.sources.api_source import extract_api
from app.transformation.cleaner import clean_api_row
from app.transformation.pipeline_result import PipelineResult
from app.utils.logger import get_logger
from app.validation.quality import validate_source_rows


def run_api_pipeline(url: str) -> PipelineResult:
    logger = get_logger()
    logger.info("API pipeline started")

    raw_rows = extract_api(url)

    valid_rows, rejected_rows = validate_source_rows(
        raw_rows,
        "API",
    )

    cleaned_rows = [
        clean_api_row(row)
        for row in valid_rows
    ]

    logger.info(
        "API pipeline completed: valid=%d rejected=%d",
        len(cleaned_rows),
        len(rejected_rows),
    )

    return PipelineResult(
        valid=cleaned_rows,
        rejected=rejected_rows,
    )