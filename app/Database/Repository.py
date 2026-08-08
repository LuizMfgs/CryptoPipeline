import logging
from datetime import datetime, timedelta, timezone

import pandas as pd

from sqlalchemy import text

from app.database.Database import engine, get_session
from app.database.Models import Cryptocurrency, ETLExecution


logger = logging.getLogger(__name__)


class CryptoRepository:

    # INSERT

    @staticmethod
    def insert_snapshots(df: pd.DataFrame) -> int:
        """
        Insert cryptocurrency snapshots into PostgreSQL.

        Historical snapshots are preserved.
        """

        if df.empty:
            logger.warning(
                "No data to insert."
            )
            return 0

        records = df.to_dict(
            orient="records"
        )

        with get_session() as session:

            coins = [
                Cryptocurrency(
                    coin_id=row["coin_id"],
                    symbol=row["symbol"],
                    name=row["name"],
                    current_price=row["current_price"],
                    market_cap=row["market_cap"],
                    market_cap_rank=row["market_cap_rank"],
                    total_volume=row["total_volume"],
                    price_change_percentage_24h=(
                        row["price_change_percentage_24h"]
                    ),
                    ath_change_percentage=(
                        row["ath_change_percentage"]
                    ),
                    liquidity_ratio=(
                        row["liquidity_ratio"]
                    ),
                    etl_timestamp=(
                        row["etl_timestamp"]
                    ),
                )
                for row in records
            ]

            session.add_all(coins)

            logger.info(
                "%s cryptocurrency snapshots "
                "inserted.",
                len(coins)
            )

            return len(coins)

    # LATEST SNAPSHOT

    @staticmethod
    def get_latest_snapshot() -> pd.DataFrame:

        query = text("""
            SELECT *
            FROM cryptocurrencies
            WHERE etl_timestamp = (
                SELECT MAX(etl_timestamp)
                FROM cryptocurrencies
            )
            ORDER BY market_cap_rank
        """)

        return pd.read_sql(
            query,
            engine
        )

    # TOP MARKET CAP

    @staticmethod
    def get_top_marketcap(
        limit: int = 10
    ) -> pd.DataFrame:

        query = text("""
            SELECT *
            FROM cryptocurrencies
            WHERE etl_timestamp = (
                SELECT MAX(etl_timestamp)
                FROM cryptocurrencies
            )
            ORDER BY market_cap DESC
            LIMIT :limit
        """)

        return pd.read_sql(
            query,
            engine,
            params={"limit": limit}
        )

    # TOP VOLUME

    @staticmethod
    def get_top_volume(
        limit: int = 10
    ) -> pd.DataFrame:

        query = text("""
            SELECT *
            FROM cryptocurrencies
            WHERE etl_timestamp = (
                SELECT MAX(etl_timestamp)
                FROM cryptocurrencies
            )
            ORDER BY total_volume DESC
            LIMIT :limit
        """)

        return pd.read_sql(
            query,
            engine,
            params={"limit": limit}
        )

    # TOP LIQUIDITY

    @staticmethod
    def get_top_liquidity(
        limit: int = 10
    ) -> pd.DataFrame:

        query = text("""
            SELECT *
            FROM cryptocurrencies
            WHERE etl_timestamp = (
                SELECT MAX(etl_timestamp)
                FROM cryptocurrencies
            )
            ORDER BY liquidity_ratio DESC
            LIMIT :limit
        """)

        return pd.read_sql(
            query,
            engine,
            params={"limit": limit}
        )

    # TOP GAINERS

    @staticmethod
    def get_top_gainers(
        limit: int = 10
    ) -> pd.DataFrame:

        query = text("""
            SELECT *
            FROM cryptocurrencies
            WHERE etl_timestamp = (
                SELECT MAX(etl_timestamp)
                FROM cryptocurrencies
            )
            ORDER BY price_change_percentage_24h DESC
            LIMIT :limit
        """)

        return pd.read_sql(
            query,
            engine,
            params={"limit": limit}
        )

    # COIN HISTORY

    @staticmethod
    def get_coin_history(
        symbol: str
    ) -> pd.DataFrame:

        query = text("""
            SELECT
                etl_timestamp,
                current_price,
                market_cap,
                total_volume,
                liquidity_ratio
            FROM cryptocurrencies
            WHERE symbol = :symbol
            ORDER BY etl_timestamp
        """)

        return pd.read_sql(
            query,
            engine,
            params={
                "symbol": symbol.lower()
            }
        )

    # FULL HISTORY

    @staticmethod
    def get_history() -> pd.DataFrame:

        query = text("""
            SELECT *
            FROM cryptocurrencies
            ORDER BY
                etl_timestamp DESC,
                market_cap_rank
        """)

        return pd.read_sql(
            query,
            engine
        )

    # LAST UPDATE

    @staticmethod
    def get_last_update():

        query = text("""
            SELECT MAX(etl_timestamp)
            FROM cryptocurrencies
        """)

        with engine.connect() as connection:

            return connection.execute(
                query
            ).scalar()

    # COUNT RECORDS

    @staticmethod
    def count_records() -> int:

        query = text("""
            SELECT COUNT(*)
            FROM cryptocurrencies
        """)

        with engine.connect() as connection:

            return connection.execute(
                query
            ).scalar()


    # COUNT SNAPSHOTS

    @staticmethod
    def count_snapshots() -> int:

        query = text("""
            SELECT COUNT(
                DISTINCT etl_timestamp
            )
            FROM cryptocurrencies
        """)

        with engine.connect() as connection:

            return connection.execute(
                query
            ).scalar()

    # DATABASE SIZE

    @staticmethod
    def get_database_size() -> pd.DataFrame:

        query = text("""
            SELECT pg_size_pretty(
                pg_database_size(
                    current_database()
                )
            ) AS database_size
        """)

        return pd.read_sql(
            query,
            engine
        )

    # ETL EXECUTION

    @staticmethod
    def save_execution(
        start_time,
        end_time,
        duration,
        rows_extracted,
        rows_loaded,
        status,
        error_message=None,
    ) -> None:

        with get_session() as session:

            execution = ETLExecution(
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                rows_extracted=rows_extracted,
                rows_loaded=rows_loaded,
                status=status,
                error_message=error_message,
            )

            session.add(execution)

        logger.info(
            "ETL execution saved. Status: %s",
            status
        )

    # LAST EXECUTION

    @staticmethod
    def get_last_execution():

        with get_session() as session:

            return (
                session.query(ETLExecution)
                .order_by(
                    ETLExecution.id.desc()
                )
                .first()
            )

    # EXECUTION HISTORY

    @staticmethod
    def get_execution_history(
        limit: int = 20
    ):

        with get_session() as session:

            return (
                session.query(ETLExecution)
                .order_by(
                    ETLExecution.id.desc()
                )
                .limit(limit)
                .all()
            )

    # REMOVE OLD DATA

    @staticmethod
    def remove_old_data(
        days: int = 7
    ) -> int:

        if days <= 0:
            raise ValueError(
                "days must be greater than zero."
            )

        cutoff_date = (
            datetime.now(timezone.utc)
            - timedelta(days=days)
        )

        with get_session() as session:

            deleted = (
                session.query(Cryptocurrency)
                .filter(
                    Cryptocurrency.etl_timestamp
                    < cutoff_date
                )
                .delete(
                    synchronize_session=False
                )
            )

        logger.info(
            "Removed %s records older than %s days.",
            deleted,
            days
        )

        return deleted


    # RESET TABLE

    @staticmethod
    def reset_table() -> None:

        with engine.begin() as connection:

            connection.execute(
                text("""
                    TRUNCATE TABLE cryptocurrencies
                    RESTART IDENTITY CASCADE
                """)
            )

        logger.warning(
            "Cryptocurrency table was reset."
        )