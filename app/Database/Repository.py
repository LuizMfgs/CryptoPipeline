import pandas as pd
from sqlalchemy import text
from app.Database.Database import engine
from app.Database.Models import ETLExecution
from app.Database.Database import SessionLocal

TABLE_NAME = "cryptocurrencies"

class CryptoRepository:

    # ==========================================
    # INSERTS
    # ==========================================

    @staticmethod
    def save_dataframe(df):

        df.to_sql(
            TABLE_NAME,
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )

    # ==========================================
    # SELECTS
    # ==========================================
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
    def get_top_marketcap(limit=10):

        query = f"""
        SELECT *
        FROM cryptocurrencies
        WHERE etl_timestamp = (
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        )
        ORDER BY market_cap DESC
        LIMIT {limit}
        """

        return pd.read_sql(query, engine)


    @staticmethod
    def get_top_volume(limit=10):

        query = f"""
        SELECT *
        FROM cryptocurrencies
        WHERE etl_timestamp = (
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        )
        ORDER BY total_volume DESC
        LIMIT {limit}
        """

        return pd.read_sql(query, engine)


    @staticmethod
    def get_top_liquidity(limit=10):

        query = f"""
        SELECT *
        FROM cryptocurrencies
        WHERE etl_timestamp = (
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        )
        ORDER BY liquidity_ratio DESC
        LIMIT {limit}
        """

        return pd.read_sql(query, engine)


    @staticmethod
    def save_execution(
        start_time,
        end_time,
        duration,
        rows_extracted,
        rows_loaded,
        status,
        error_message=None
        ):

        with SessionLocal() as session:

            execution = ETLExecution(

            start_time=start_time,

            end_time=end_time,

            duration_seconds=duration,

            rows_extracted=rows_extracted,

            rows_loaded=rows_loaded,

            status=status,

            error_message=error_message

        )

        session.add(execution)

        session.commit()

    @staticmethod
    def get_last_execution():

        with SessionLocal() as session:

            return (

            session.query(ETLExecution)

            .order_by(ETLExecution.id.desc())

            .first()

        )
    @staticmethod
    def get_execution_history(limit=20):

        with SessionLocal() as session:

                return (

            session.query(ETLExecution)

            .order_by(ETLExecution.id.desc())

            .limit(limit)

            .all()

        )
    
    @staticmethod
    def get_top_gainers(limit=10):

        query = f"""
        SELECT *
        FROM cryptocurrencies
        WHERE etl_timestamp = (
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        )
        ORDER BY price_change_percentage_24h DESC
        LIMIT {limit}
        """

        return pd.read_sql(query, engine)


    @staticmethod
    def get_coin_history(symbol):

        query = """
        SELECT
            etl_timestamp,
            current_price,
            market_cap,
            total_volume,
            liquidity_ratio
        FROM cryptocurrencies
        WHERE symbol = %(symbol)s
        ORDER BY etl_timestamp
        """

        return pd.read_sql(
            query,
            engine,
            params={"symbol": symbol}
        )


    @staticmethod
    def get_database_size():

        query = """
        SELECT pg_size_pretty(
        pg_database_size(current_database())
        ) AS database_size;
        """

        return pd.read_sql(query, engine)



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
        ORDER BY etl_timestamp DESC,
                 market_cap_rank
        """

        return pd.read_sql(query, engine)

    @staticmethod
    def get_last_update():

        query = text("""
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        """)

        with engine.begin() as conn:

            return conn.execute(query).scalar()

    @staticmethod
    def count_records():

        query = text("""
            SELECT COUNT(*)
            FROM cryptocurrencies
        """)

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

    # ==========================================
    # DELETE
    # ==========================================

    @staticmethod
    def remove_old_data(days=7):

        query = text("""
            DELETE
            FROM cryptocurrencies
            WHERE etl_timestamp <
                  NOW() - (:days * INTERVAL '1 day')
        """)

        with engine.begin() as conn:

            conn.execute(
                query,
                {"days": days}
            )

    # ==========================================
    # ADMIN
    # ==========================================

    @staticmethod
    def reset_table():

        query = text("""
            TRUNCATE TABLE cryptocurrencies
            RESTART IDENTITY
        """)

        with engine.begin() as conn:

            conn.execute(query)