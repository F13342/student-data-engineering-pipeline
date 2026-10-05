from app.sources.web_scraping_source import extract_web_students
from app.transformation.cleaner import clean_web_row
from app.transformation.pipeline_result import PipelineResult
from app.utils.logger import get_logger
from app.validation.quality import validate_source_rows


def run_web_scraping_pipeline(url: str) -> PipelineResult:
    logger = get_logger()
    logger.info("Web scraping pipeline started")

    raw_rows = extract_web_students(url)

    valid_rows, rejected_rows = validate_source_rows(
        raw_rows,
        "Web Scraping",
    )

    cleaned_rows = [
        clean_web_row(row)
        for row in valid_rows
    ]

    logger.info(
        "Web scraping completed: valid=%d rejected=%d",
        len(cleaned_rows),
        len(rejected_rows),
    )

    return PipelineResult(
        valid=cleaned_rows,
        rejected=rejected_rows,
    )