from app.pipelines.api_pipeline import run_api_pipeline
from app.pipelines.csv_pipeline import run_csv_pipeline
from app.pipelines.mongodb_pipeline import run_mongodb_pipeline
from app.pipelines.postgresql_pipeline import run_postgresql_pipeline
from app.pipelines.web_scraping_pipeline import run_web_scraping_pipeline
from app.transformation.integration import integrate_all
from app.transformation.pipeline_result import PipelineResult
from app.transformation.transformer import transform
from app.utils.logger import get_logger
from app.validation.quality import validate_and_split


def run_integration_pipeline(
    csv_path,
    api_url,
    web_url,
    postgresql_connection,
    mongodb_collection,
) -> PipelineResult:
    logger = get_logger()
    logger.info("Integration pipeline started")

    csv_result = run_csv_pipeline(csv_path)
    api_result = run_api_pipeline(api_url)
    web_result = run_web_scraping_pipeline(web_url)
    postgres_result = run_postgresql_pipeline(postgresql_connection)
    mongo_result = run_mongodb_pipeline(mongodb_collection)

    integrated, integration_rejected = integrate_all(
        csv_result.valid,
        api_result.valid,
        web_result.valid,
        postgres_result.valid,
        mongo_result.valid,
    )

    logger.info(
        "Integration completed: valid=%d rejected=%d",
        len(integrated),
        len(integration_rejected),
    )

    transformed = transform(integrated)

    valid, validation_rejected = validate_and_split(transformed)

    rejected = (
        csv_result.rejected
        + api_result.rejected
        + web_result.rejected
        + postgres_result.rejected
        + mongo_result.rejected
        + integration_rejected
        + validation_rejected
    )

    logger.info(
        "Final validation: valid=%d rejected=%d",
        len(valid),
        len(rejected),
    )

    logger.info("Integration pipeline completed")

    return PipelineResult(
        valid=valid,
        rejected=rejected,
    )