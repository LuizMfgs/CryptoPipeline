import pandas as pd

from app.Load import load_data
from app.Transform import transform
from app.database.Database import get_session
from app.database.Models import Cryptocurrency


def _raw(coin_id):
    return {
        "id": coin_id,
        "symbol": "tl",
        "name": "Test Load",
        "current_price": 100.0,
        "market_cap": 1_000_000,
        "market_cap_rank": 1,
        "total_volume": 100_000,
        "price_change_percentage_24h": 2.0,
        "ath_change_percentage": -10.0,
    }


def test_load_empty_dataframe():
    assert load_data(pd.DataFrame()) == 0


def test_transform_to_load():
    coin_id = "test-transform-load"

    try:
        transformed = transform(
            pd.DataFrame([_raw(coin_id)])
        )

        assert load_data(transformed) == 1

        with get_session() as session:
            record = (
                session.query(Cryptocurrency)
                .filter(Cryptocurrency.coin_id == coin_id)
                .first()
            )

            assert record is not None
            assert record.name == "Test Load"
    finally:
        with get_session() as session:
            session.query(Cryptocurrency).filter(
                Cryptocurrency.coin_id == coin_id
            ).delete(synchronize_session=False)
