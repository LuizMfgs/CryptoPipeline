from datetime import datetime
import logging

from app.Extract import extract
from app.Transform import transform
from app.Load import load_data, remove_old_data
from app.Quality import quality_report, validate
from app.Database.Repository import ETLRepository
from config.settings import RETENTION_DAYS


logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    start_time = datetime.now()

    print("\n" + "=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)

    logging.info("Starting ETL Pipeline")

    rows_extracted = 0
    rows_loaded = 0

    try:

        # =====================
        # EXTRACT
        # =====================

        df = extract()

        rows_extracted = len(df)

        print(f"Extracted {rows_extracted} records")
        logging.info(f"Extracted {rows_extracted} records")

        # =====================
        # TRANSFORM
        # =====================

        transformed_df = transform(df)

        print(f"Transformed {len(transformed_df)} records")
        logging.info(f"Transformed {len(transformed_df)} records")

        # =====================
        # QUALITY
        # =====================

        if not validate(transformed_df):

            logging.error("Data Quality Checks Failed")

            print(
                "Pipeline stopped because the data did not pass the quality checks."
            )

            return

        logging.info("Data Quality Checks Passed")

        quality_report(transformed_df)

        # =====================
        # LOAD
        # =====================

        load_data(transformed_df)

        rows_loaded = len(transformed_df)

        logging.info("Data loaded successfully")

        # =====================
        # RETENTION
        # =====================

        remove_old_data(days=RETENTION_DAYS)

        logging.info("Old records removed successfully")

        # =====================
        # FINISH
        # =====================

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

            status="SUCCESS"

        )

        print("\n" + "=" * 50)
        print("PIPELINE COMPLETED")
        print("=" * 50)
        print(f"Execution Time: {duration:.2f} seconds")

        logging.info(
            f"Pipeline completed successfully in {duration:.2f} seconds"
        )

    except Exception as error:

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

            status="FAILED",

            error_message=str(error)

        )

        print(f"\nPipeline failed: {error}")

        logging.error(
            f"Pipeline failed: {error}",
            exc_info=True
        )


if __name__ == "__main__":
    main()