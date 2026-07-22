from app.Extract import extract
from app.Transform import transform
from app.Load import load_data, remove_old_data
from datetime import datetime
from app.Quality import quality_report, validate
import logging

# LOGGING

logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# MAIN PIPELINE

def main():

    start_time = datetime.now()

    print("\n" + "=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)

    logging.info("Starting ETL Pipeline")

    try:

        # EXTRACT

        df = extract()

        print(f"Extracted {len(df)} records")
        logging.info(f"Extracted {len(df)} records")

        # TRANSFORM
     
        transformed_df = transform(df)

        print(f"Transformed {len(transformed_df)} records")
        logging.info(f"Transformed {len(transformed_df)} records")
       
        # DATA QUALITY
       
        if validate(transformed_df):

            logging.info("Data Quality Checks Passed")

            quality_report(transformed_df)

        else:

            logging.error("Data Quality Checks Failed")

            print(
                "Pipeline stopped because the data did not pass the quality checks."
            )

            return
        
        # LOAD
       
        load_data(transformed_df)

        logging.info("Data loaded successfully")

        #Remove dados antigos

        remove_old_data(days=7)

        logging.info("Old records removed successfully")

        load_data(transformed_df)

        remove_old_data()

        # FINISH

        end_time = datetime.now()

        duration = (
            end_time - start_time
        ).total_seconds()

        print("\n" + "=" * 50)
        print("PIPELINE COMPLETED")
        print("=" * 50)
        print(f"Execution Time: {duration:.2f} seconds")

        logging.info(
            f"Pipeline completed successfully in {duration:.2f} seconds"
        )

    except Exception as error:

        print(f"\nPipeline failed: {error}")

        logging.error(
            f"Pipeline failed: {error}",
            exc_info=True
        )


# ENTRY

if __name__ == "__main__":
    main()