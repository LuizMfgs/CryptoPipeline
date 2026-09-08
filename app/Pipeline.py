import logging
from datetime import datetime

from app.Extract import extract
from app.Transform import transform
from app.Load import load_data, remove_old_data

from app.data_quality.Checks import run_quality_checks
from app.data_quality.Report import (
    build_quality_report,
    log_quality_report,
    print_quality_report,
)

from app.database.Repository import ETLRepository
from config.settings import settings


logger = logging.getLogger(__name__)


def main():

    start_time = datetime.now()

    rows_extracted = 0
    rows_loaded = 0

    print("\n" + "=" * 60)
    print("STARTING ETL PIPELINE")
    print("=" * 60)

    logger.info("Starting ETL pipeline.")

    try:

        # EXTRACT

        logger.info("Starting extraction.")

        df = extract()

        rows_extracted = len(df)

        print(
            f"\nExtracted: {rows_extracted} records"
        )

        logger.info(
            "Extraction completed: %s records.",
            rows_extracted,
        )

        # TRANSFORM

        logger.info("Starting transformation.")

        transformed_df = transform(df)

        transformed_rows = len(transformed_df)

        print(
            f"Transformed: {transformed_rows} records"
        )

        logger.info(
            "Transformation completed: %s records.",
            transformed_rows,
        )

        # DATA QUALITY

        logger.info(
            "Starting data quality validation."
        )

        quality_results = run_quality_checks(
            transformed_df
        )

        quality_report_result = build_quality_report(
            transformed_df,
            quality_results,
        )

        log_quality_report(
            quality_report_result,
            quality_results,
        )

        print_quality_report(
            quality_report_result,
            quality_results,
        )

        # QUALITY GATE

        if not quality_results["passed"]:

            logger.error(
                "Data quality validation failed. "
                "Pipeline aborted before load."
            )

            raise ValueError(
                "Data quality validation failed."
            )

        logger.info(
            "Data quality validation passed."
        )

        # LOAD

        logger.info(
            "Starting database load."
        )

        rows_loaded = load_data(
            transformed_df
        )

        logger.info(
            "Database load completed: %s records.",
            rows_loaded,
        )

        print(
            f"\nLoaded: {rows_loaded} records"
        )

        # RETENTION

        logger.info(
            "Starting data retention cleanup."
        )

        removed_rows = remove_old_data(
            days=settings.DATA_RETENTION_DAYS
        )

        logger.info(
            "Retention cleanup completed: "
            "%s records removed.",
            removed_rows,
        )

        print(
            f"Old records removed: {removed_rows}"
        )

        # SUCCESS

        end_time = datetime.now()

        duration = (
            end_time - start_time
        ).total_seconds()

        ETLRepository.save_execution(

            start_time=start_time,

            end_time=end_time,

            duration=duration,

            rows_extracted=rows_extracted,

            rows_loaded=rows_loaded,

            status="SUCCESS",

            error_message=None,
        )

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print(
            f"Execution time: "
            f"{duration:.2f} seconds"
        )

        logger.info(
            "ETL pipeline completed successfully "
            "in %.2f seconds.",
            duration,
        )

    # FAILURE

    except Exception as error:

        end_time = datetime.now()

        duration = (
            end_time - start_time
        ).total_seconds()

        logger.error(
            "ETL pipeline failed after %.2f seconds: %s",
            duration,
            error,
            exc_info=True,
        )

        # Save failed execution

        try:

            ETLRepository.save_execution(

                start_time=start_time,

                end_time=end_time,

                duration=duration,

                rows_extracted=rows_extracted,

                rows_loaded=rows_loaded,

                status="FAILED",

                error_message=str(error),
            )

        except Exception as execution_error:

            logger.critical(
                "Failed to save ETL execution history: %s",
                execution_error,
                exc_info=True,
            )

        # Console output

        print("\n" + "=" * 60)
        print("PIPELINE FAILED")
        print("=" * 60)

        print(
            f"Error: {error}"
        )

        print(
            f"Execution time: "
            f"{duration:.2f} seconds"
        )

        # Important for:
        # Docker
        # CI/CD
        # schedulers
        raise


if __name__ == "__main__":
    main()
