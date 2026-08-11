from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests

from app.Extract import create_session, extract
from config.settings import settings


class FakeResponse:
    def __init__(self, payload, error=None):
        self._payload = payload
        self._error = error

    def raise_for_status(self):
        if self._error:
            raise self._error

    def json(self):
        return self._payload


def _coin(coin_id):
    return {
        "id": coin_id,
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 100000,
        "market_cap": 2_000_000_000,
        "market_cap_rank": 1,
        "total_volume": 100_000_000,
        "price_change_percentage_24h": 2.5,
        "ath_change_percentage": -10.0,
    }


@pytest.mark.parametrize("pages", [0, -1, -7])
def test_extract_rejects_invalid_total_pages(pages):
    with pytest.raises(
        ValueError,
        match="total_pages must be greater than zero.",
    ):
        extract(pages)


def test_create_session_configures_retry():
    session = create_session()

    try:
        adapter = session.get_adapter("https://")
        retry = adapter.max_retries

        assert retry.total == settings.MAX_RETRIES
        assert retry.backoff_factor == settings.BACKOFF_FACTOR
        assert set(retry.status_forcelist) == set(
            settings.RETRY_STATUS_CODES
        )
        assert "GET" in retry.allowed_methods
    finally:
        session.close()


def test_extract_valid_response():
    session = MagicMock()
    session.get.return_value = FakeResponse(
        [_coin("bitcoin")]
    )

    with patch("app.Extract.create_session", return_value=session):
        result = extract(1)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["id"] == "bitcoin"
    session.get.assert_called_once()


def test_extract_paginates_and_combines_pages():
    session = MagicMock()
    session.get.side_effect = [
        FakeResponse([_coin("bitcoin")]),
        FakeResponse([_coin("ethereum")]),
    ]

    with patch("app.Extract.create_session", return_value=session):
        result = extract(2)

    assert len(result) == 2
    assert result["id"].tolist() == ["bitcoin", "ethereum"]
    assert session.get.call_count == 2


def test_extract_stops_on_empty_page():
    session = MagicMock()
    session.get.side_effect = [
        FakeResponse([_coin("bitcoin")]),
        FakeResponse([]),
    ]

    with patch("app.Extract.create_session", return_value=session):
        result = extract(3)

    assert len(result) == 1
    assert session.get.call_count == 2


def test_extract_ignores_unexpected_response_format():
    session = MagicMock()
    session.get.return_value = FakeResponse(
        {"error": "unexpected"}
    )

    with patch("app.Extract.create_session", return_value=session):
        result = extract(1)

    assert result.empty


def test_extract_continues_after_request_error():
    session = MagicMock()
    session.get.side_effect = [
        requests.exceptions.Timeout("timeout"),
        FakeResponse([_coin("ethereum")]),
    ]

    with patch("app.Extract.create_session", return_value=session):
        result = extract(2)

    assert len(result) == 1
    assert result.iloc[0]["id"] == "ethereum"
    assert session.get.call_count == 2
