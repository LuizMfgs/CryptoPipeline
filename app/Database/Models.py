from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    BigInteger,
    DateTime
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cryptocurrency(Base):

    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True, autoincrement=True)

    coin_id = Column(String(100), nullable=False)

    symbol = Column(String(20), nullable=False)

    name = Column(String(100), nullable=False)

    current_price = Column(Float, nullable=False)

    market_cap = Column(BigInteger, nullable=False)

    market_cap_rank = Column(Integer)

    total_volume = Column(BigInteger)

    price_change_percentage_24h = Column(Float)

    ath_change_percentage = Column(Float)

    liquidity_ratio = Column(Float)

    etl_timestamp = Column(DateTime, nullable=False)