import pandas as pd
import logging
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import os
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE = "data/crypto.db"
TABLE_NAME = "cryptocurrencies"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def recreate_table_if_schema_changed(df, table_name="cryptocurrencies"):
    """
    Recria a tabela apenas se o esquema do DataFrame
    for diferente do esquema existente no PostgreSQL.
    """

    inspector = inspect(engine)

    if not inspector.has_table(table_name):
        logger.info("Table does not exist. It will be created.")
        return

    db_columns = [
        column["name"]
        for column in inspector.get_columns(table_name)
    ]

    df_columns = list(df.columns)

    if db_columns != df_columns:

        logger.warning("Schema changed.")
        logger.warning("Dropping old table...")

        with engine.begin() as connection:
            connection.exec_driver_sql(
                f"DROP TABLE {table_name}"
            )

        logger.info("Table removed successfully.")

    else:

        logger.info("Schema unchanged.")


def load(df, table_name="cryptocurrencies"):

    recreate_table_if_schema_changed(df, table_name)

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    logger.info(
        f"{len(df)} records loaded successfully."
    )


if __name__ == "__main__":

    from app.Extract import extract
    from app.Transform import transform

    print("=" * 50)
    print("LOADING TEST")
    print("=" * 50)

    raw_df = extract()

    transformed_df = transform(raw_df)

    load(transformed_df)

    print("Load completed successfully.")