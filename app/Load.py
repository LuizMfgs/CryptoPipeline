import logging

from app.Database.Repository import CryptoRepository


logger = logging.getLogger(__name__)


def load_data(df):

    rows = CryptoRepository.save_dataframe(df)

    logger.info("%s records inserted.", rows)

    print(f"{rows} records inserted successfully.")

    return rows


def remove_old_data(days):

    removed = CryptoRepository.remove_old_data(days)

    logger.info("%s old records removed.", removed)

    print(f"{removed} old records removed.")

    return removed