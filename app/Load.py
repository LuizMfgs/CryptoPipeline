import logging
import pandas as pd
from app.database.Repository import CryptoRepository

logger = logging.getLogger(__name__)

def load_data(df: pd.DataFrame) -> int:
    """
    Load transformed cryptocurrency data
    into PostgreSQL.

    Args:
        df: Transformed cryptocurrency DataFrame.

    Returns:
        Number of records inserted.
    """

    if df.empty:
        logger.warning(
            "Load skipped: received empty DataFrame."
        )

        return 0

    logger.info(
        "Starting load: %s records.",
        len(df)
    )

    try:

        rows = CryptoRepository.insert_snapshots(df)

        logger.info(
            "Load completed successfully: "
            "%s records inserted.",
            rows
        )

        return rows

    except Exception:
        logger.exception(
            "Failed to load cryptocurrency data."
        )

        raise


def remove_old_data(days: int) -> int:
    """
    Remove historical records older than
    the specified number of days.

    Args:
        days: Number of days to preserve.

    Returns:
        Number of records removed.
    """

    if days <= 0:
        raise ValueError(
            "days must be greater than zero."
        )

    logger.info(
        "Starting historical data cleanup. "
        "Retention: %s days.",
        days
    )

    try:

        removed = (
            CryptoRepository.remove_old_data(days)
        )

        logger.info(
            "Historical cleanup completed: "
            "%s records removed.",
            removed
        )

        return removed

    except Exception:
        logger.exception(
            "Failed to remove old records."
        )

        raise