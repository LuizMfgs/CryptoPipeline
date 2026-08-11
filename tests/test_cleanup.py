from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from app.Load import remove_old_data
from app.database.Database import get_session
from app.database.Models import Cryptocurrency
from app.database.Repository import CryptoRepository


def _row(coin_id, timestamp):
    return {
        "coin_id": coin_id,
        "symbol": "tc",
        "name": "Test Cleanup",
        "current_price": 100.0,
        "market_cap": 1_000_000,
        "market_cap_rank": 1,
        "total_volume": 50_000,
        "price_change_percentage_24h": 1.0,
        "ath_change_percentage": -10.0,
        "liquidity_ratio": 0.05,
        "etl_timestamp": timestamp,
    }


@pytest.mark.parametrize("days", [0, -1, -7])
def test_remove_old_data_rejects_invalid_days(days):
    with pytest.raises(
        ValueError,
        match="days must be greater than zero.",
    ):
        remove_old_data(days)


def test_remove_old_data_removes_only_old_snapshots():
    coin_id = "test-cleanup-pytest"
    old_timestamp = datetime.now(timezone.utc) - timedelta(days=30)
    recent_timestamp = datetime.now(timezone.utc)

    rows = [
        _row(coin_id, old_timestamp),
        _row(coin_id, recent_timestamp),
    ]

    try:
        assert CryptoRepository.insert_snapshots(
            pd.DataFrame(rows)
        ) == 2

        assert remove_old_data(days=7) == 1

        with get_session() as session:
            remaining = (
                session.query(Cryptocurrency)
                .filter(Cryptocurrency.coin_id == coin_id)
                .all()
            )

            assert len(remaining) == 1

            # PostgreSQL column is timestamp without time zone.
            stored_timestamp = remaining[0].etl_timestamp

            assert stored_timestamp.replace(tzinfo=None) == (
                recent_timestamp
                .astimezone()
                .replace(tzinfo=None)
                )
    finally:
        with get_session() as session:
            session.query(Cryptocurrency).filter(
                Cryptocurrency.coin_id == coin_id
            ).delete(synchronize_session=False)
