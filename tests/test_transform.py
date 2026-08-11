import pandas as pd
import pytest

from app.Transform import transform


def _raw(coin_id="bitcoin", **overrides):
    row = {
        "id": coin_id,
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 100000.0,
        "market_cap": 1_000_000,
        "market_cap_rank": 1,
        "total_volume": 100_000,
        "price_change_percentage_24h": 2.5,
        "ath_change_percentage": -10.0,
    }
    row.update(overrides)
    return row


def test_transform_valid_data():
    result = transform(pd.DataFrame([_raw()]))

    assert not result.empty
    assert len(result) == 1
    assert {"coin_id", "liquidity_ratio", "etl_timestamp"} <= set(
        result.columns
    )
    assert result.iloc[0]["coin_id"] == "bitcoin"


def test_transform_removes_duplicates():
    result = transform(
        pd.DataFrame([_raw(), _raw()])
    )

    assert len(result) == 1
    assert result.iloc[0]["coin_id"] == "bitcoin"


def test_transform_rejects_missing_required_columns():
    with pytest.raises(Exception):
        transform(
            pd.DataFrame(
                [{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}]
            )
        )


def test_liquidity_ratio_is_calculated_correctly():
    result = transform(
        pd.DataFrame(
            [
                _raw(
                    market_cap=1_000_000,
                    total_volume=100_000,
                )
            ]
        )
    )

    assert result.iloc[0]["liquidity_ratio"] == pytest.approx(10.0)


def test_etl_timestamp_is_utc():
    result = transform(pd.DataFrame([_raw()]))

    timestamp = result.iloc[0]["etl_timestamp"]

    assert timestamp is not None
    assert timestamp.tzinfo is not None
    assert timestamp.utcoffset().total_seconds() == 0
