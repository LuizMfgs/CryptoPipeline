from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    BigInteger,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
    Index
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cryptocurrency(Base):

    __tablename__ = "cryptocurrencies"

    __table_args__ = (

    UniqueConstraint(
        "coin_id",
        "etl_timestamp",
        name="uq_coin_snapshot"
    ),

    CheckConstraint(
        "current_price >= 0",
        name="ck_current_price"
    ),

    CheckConstraint(
        "market_cap >= 0",
        name="ck_market_cap"
    ),

    CheckConstraint(
        "market_cap_rank >= 1",
        name="ck_market_cap_rank"
    ),

    CheckConstraint(
        "total_volume >= 0",
        name="ck_total_volume"
    ),

    CheckConstraint(
        "liquidity_ratio >= 0",
        name="ck_liquidity_ratio"
    ),

    Index("idx_coin_id", "coin_id"),

    Index("idx_symbol", "symbol"),

    Index("idx_market_cap", "market_cap"),

    Index("idx_market_rank", "market_cap_rank"),

    Index("idx_etl_timestamp", "etl_timestamp"),

    Index("idx_symbol_timestamp", "symbol", "etl_timestamp"),

)

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    coin_id = Column(
    String(100),
    nullable=False
    )

    symbol = Column(
        String(20),
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    current_price = Column(
        Float,
        nullable=False
    )

    market_cap = Column(
        BigInteger,
        nullable=False
    )

    market_cap_rank = Column(
        Integer
    )

    total_volume = Column(
        BigInteger
    )

    price_change_percentage_24h = Column(
        Float
    )

    ath_change_percentage = Column(
        Float
    )

    liquidity_ratio = Column(
        Float
    )
    etl_timestamp = Column(
        DateTime(timezone=True),
        nullable=False  
    )
class ETLExecution(Base):

    __tablename__ = "etl_execution"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    start_time = Column(
        DateTime,
        nullable=False
    )

    end_time = Column(
        DateTime,
        nullable=False
    )

    duration_seconds = Column(
        Float,
        nullable=False
    )

    rows_extracted = Column(
        Integer,
        nullable=False
    )

    rows_loaded = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False
    )

    error_message = Column(
        String(1000)
    )