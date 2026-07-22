import pandas as pd

from sqlalchemy import text

from app.Database.Database import engine


TABLE_NAME = "cryptocurrencies"


class CryptoRepository:

    @staticmethod
    def save_dataframe(df):

        df.to_sql(
            TABLE_NAME,
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )

    @staticmethod
    def get_latest_snapshot():

        query = """
        SELECT *
        FROM cryptocurrencies
        WHERE etl_timestamp = (
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        )
        ORDER BY market_cap_rank
        """

        return pd.read_sql(query, engine)

    @staticmethod
    def get_history():

        query = """
        SELECT *
        FROM cryptocurrencies
        ORDER BY etl_timestamp DESC, market_cap_rank
        """

        return pd.read_sql(query, engine)

    @staticmethod
    def remove_old_data(days=7):

        query = text("""
            DELETE FROM cryptocurrencies
            WHERE etl_timestamp < NOW() - (:days * INTERVAL '1 day')
        """)

        with engine.begin() as conn:

            conn.execute(
                query,
                {"days": days}
            )

    @staticmethod
    def count_records():

        query = text(
            "SELECT COUNT(*) FROM cryptocurrencies"
        )

        with engine.begin() as conn:

            return conn.execute(query).scalar()

    @staticmethod
    def count_snapshots():

        query = text("""
            SELECT COUNT(DISTINCT etl_timestamp)
            FROM cryptocurrencies
        """)

        with engine.begin() as conn:

            return conn.execute(query).scalar()

    @staticmethod
    def get_last_update():

        query = text("""
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        """)

        with engine.begin() as conn:

            return conn.execute(query).scalar()

    @staticmethod
    def reset_table():

        query = text("""
            TRUNCATE TABLE cryptocurrencies
            RESTART IDENTITY
        """)

        with engine.begin() as conn:

            conn.execute(query)