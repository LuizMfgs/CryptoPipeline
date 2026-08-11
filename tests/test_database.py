from datetime import datetime, timezone

import pandas as pd
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database.Database import engine, get_session
from app.database.Models import Cryptocurrency
from app.database.Repository import CryptoRepository


def _row(coin_id="test-database-pytest", **overrides):
    row = {
        "coin_id": coin_id,
        "symbol": "td",
        "name": "Test Database",
        "current_price": 100.0,
        "market_cap": 1_000_000,
        "market_cap_rank": 1,
        "total_volume": 50_000,
        "price_change_percentage_24h": 1.0,
        "ath_change_percentage": -10.0,
        "liquidity_ratio": 0.05,
        "etl_timestamp": datetime.now(timezone.utc),
    }
    row.update(overrides)
    return row


def test_database_connection():
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar() == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("current_price", -1.0),
        ("market_cap", -1),
        ("market_cap_rank", 0),
        ("total_volume", -1),
        ("liquidity_ratio", -0.01),
    ],
)
def test_invalid_values_are_rejected(field, value):
    row = _row(
        coin_id=f"test-constraint-{field}",
        **{field: value},
    )

    with pytest.raises(IntegrityError):
        CryptoRepository.insert_snapshots(pd.DataFrame([row]))


def test_transaction_rolls_back_on_invalid_record():
    valid_id = "rollback-valid-pytest"
    invalid_id = "rollback-invalid-pytest"

    valid = _row(valid_id)
    invalid = _row(
        invalid_id,
        current_price=-100.0,
    )

    try:
        with pytest.raises(IntegrityError):
            CryptoRepository.insert_snapshots(
                pd.DataFrame([valid, invalid])
            )

        with get_session() as session:
            assert (
                session.query(Cryptocurrency)
                .filter(
                    Cryptocurrency.coin_id.in_(
                        [valid_id, invalid_id]
                    )
                )
                .count()
                == 0
            )
    finally:
        with get_session() as session:
            session.query(Cryptocurrency).filter(
                Cryptocurrency.coin_id.in_([valid_id, invalid_id])
            ).delete(synchronize_session=False)
