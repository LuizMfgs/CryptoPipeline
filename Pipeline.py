from Extract import extract
from transform import transform
from load import load
from datetime import datetime
from Quality import quality_report, validate
import logging

logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s- %(levelname)s - %(message)s"
)

def main():

    start_time = datetime.now()

    print("\n" + "=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)

    logging.info("Starting ETL Pipeline")

    try:

        # ==========================
        # EXTRACT
        # ==========================

        df = extract()

        print(f"Extracted {len(df)} records")
        logging.info(
            f"Extracted {len(df)} records"
        )

        # ==========================
        # TRANSFORM
        # ==========================

        transformed_df = transform(df)

        print(
            f"Transformed {len(transformed_df)} records"
        )

        logging.info(
            f"Transformed {len(transformed_df)} records"
        )
        # ==========================
        # Quality
        # ==========================
        validate(
            transformed_df
        )

        quality_report (transformed_df)

        logging.info(
            "Data Quality Checks Passed"
        )



        # ==========================
        # LOAD
        # ==========================

        load(transformed_df)

        logging.info(
            "Data loaded successfully"
        )

        # ==========================
        # FINISH
        # ==========================

        end_time = datetime.now()

        duration = (
            end_time - start_time
        ).total_seconds()

        print(
            f"Pipeline completed in {duration:.2f} seconds"
        )

        logging.info(
            f"Pipeline completed successfully in {duration:.2f} seconds"
        )

    except Exception as error:

        print(
            f"Pipeline failed: {error}"
        )

        logging.error(
            f"Pipeline failed: {error}",
            exc_info=True
        )


if __name__ == "__main__":
    main()