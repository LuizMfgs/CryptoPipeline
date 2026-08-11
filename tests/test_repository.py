from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest
from sqlalchemy.exc import IntegrityError

from app.database.Database import get_session
from app.database.Models import Cryptocurrency
from app.database.Repository import CryptoRepository


def _row(coin_id, timestamp=None, **overrides):
    row = {
        "coin_id": coin_id,
        "symbol": "tr",
        "name": "Test Repository",
        "current_price": 100.0,
        "market_cap": 1_000_000,
        "market_cap_rank": 1,
        "total_volume": 50_000,
        "price_change_percentage_24h": 1.0,
        "ath_change_percentage": -10.0,
        "liquidity_ratio": 0.05,
        "etl_timestamp": timestamp or datetime.now(timezone.utc),
    }
    row.update(overrides)
    return row


def _delete_coin(coin_id):
    with get_session() as session:
        session.query(Cryptocurrency).filter(
            Cryptocurrency.coin_id == coin_id
        ).delete(synchronize_session=False)


def test_insert_empty_dataframe():
    assert CryptoRepository.insert_snapshots(pd.DataFrame()) == 0


def test_duplicate_snapshot_is_rejected():
    coin_id = "test-duplicate-pytest"
    row = _row(coin_id)

    try:
        assert CryptoRepository.insert_snapshots(pd.DataFrame([row])) == 1

        with pytest.raises(IntegrityError):
            CryptoRepository.insert_snapshots(pd.DataFrame([row]))

        with get_session() as session:
            assert (
                session.query(Cryptocurrency)
                .filter(Cryptocurrency.coin_id == coin_id)
                .count()
                == 1
            )
    finally:
        _delete_coin(coin_id)


def test_multiple_snapshots_are_preserved():
    coin_id = "test-history-pytest"
    base_time = datetime.now(timezone.utc)

    rows = [
        _row(
            coin_id,
            timestamp=base_time + timedelta(minutes=i),
            current_price=100.0 + i,
        )
        for i in range(3)
    ]

    try:
        assert CryptoRepository.insert_snapshots(
            pd.DataFrame(rows)
        ) == 3

        with get_session() as session:
            assert (
                session.query(Cryptocurrency)
                .filter(Cryptocurrency.coin_id == coin_id)
                .count()
                == 3
            )
    finally:
        _delete_coin(coin_id)


def test_batch_insert_rolls_back_on_invalid_record():
    ids = [
        "rollback-batch-valid-1",
        "rollback-batch-invalid",
        "rollback-batch-valid-2",
    ]

    rows = [
        _row(ids[0]),
        _row(ids[1], current_price=-100.0),
        _row(ids[2], current_price=200.0),
    ]

    try:
        with pytest.raises(IntegrityError):
            CryptoRepository.insert_snapshots(pd.DataFrame(rows))

        with get_session() as session:
            assert (
                session.query(Cryptocurrency)
                .filter(Cryptocurrency.coin_id.in_(ids))
                .count()
                == 0
            )
    finally:
        with get_session() as session:
            session.query(Cryptocurrency).filter(
                Cryptocurrency.coin_id.in_(ids)
            ).delete(synchronize_session=False)
