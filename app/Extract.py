import logging
import time
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import settings


logger = logging.getLogger(__name__)

# HTTP SESSION

def create_session() -> requests.Session:
    """
    Creates and configures an HTTP session with
    retry support for temporary API failures.
    """

    retry_strategy = Retry(
        total=settings.MAX_RETRIES,
        backoff_factor=settings.BACKOFF_FACTOR,
        status_forcelist=settings.RETRY_STATUS_CODES,
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy
    )

    session = requests.Session()

    session.mount(
        "http://",
        adapter
    )

    session.mount(
        "https://",
        adapter
    )

    return session

# EXTRACTION

def extract(
    total_pages: int | None = None
) -> pd.DataFrame:
    """
    Extract cryptocurrency market data
    from the CoinGecko API.

    Args:
        total_pages:
            Number of API pages to extract.
            Uses settings.TOTAL_PAGES when None.

    Returns:
        DataFrame containing extracted cryptocurrency data.
    """

    if total_pages is None:
        total_pages = settings.TOTAL_PAGES

    if total_pages <= 0:
        raise ValueError(
            "total_pages must be greater than zero."
        )

    all_data = []

    logger.info(
        "Starting cryptocurrency extraction."
    )

    logger.info(
        "Pages configured: %s | Records per page: %s",
        total_pages,
        settings.PER_PAGE,
    )

    session = create_session()

    try:

        for page in range(
            1,
            total_pages + 1
        ):

            logger.info(
                "Extracting page %s/%s.",
                page,
                total_pages,
            )

            params = {
                "vs_currency": settings.VS_CURRENCY,
                "order": settings.ORDER,
                "per_page": settings.PER_PAGE,
                "page": page,
            }

            try:

                response = session.get(
                    settings.COINGECKO_MARKETS_URL,
                    params=params,
                    timeout=settings.REQUEST_TIMEOUT,
                )

                response.raise_for_status()

                page_data = response.json()

                if not isinstance(
                    page_data,
                    list
                ):

                    logger.error(
                        "Unexpected API response "
                        "format on page %s.",
                        page,
                    )

                    continue

                if not page_data:

                    logger.info(
                        "No more data available "
                        "after page %s.",
                        page,
                    )

                    break

                all_data.extend(
                    page_data
                )

                logger.info(
                    "Page %s extracted successfully: "
                    "%s records.",
                    page,
                    len(page_data),
                )

                # Avoid unnecessary delay
                # after the final request.
                if page < total_pages:

                    time.sleep(
                        settings.REQUEST_DELAY
                    )

            except requests.exceptions.RequestException as error:

                logger.error(
                    "Failed to extract page %s: %s",
                    page,
                    error,
                )

                continue

    finally:

        session.close()

    dataframe = pd.DataFrame(
        all_data
    )

    if dataframe.empty:

        logger.warning(
            "Extraction finished with "
            "no records returned."
        )

        return dataframe

    logger.info(
        "Extraction finished successfully: "
        "%s total records.",
        len(dataframe),
    )

    return dataframe


# TEST

if __name__ == "__main__":

    dataframe = extract()

    print(
        "\nFirst five rows:\n"
    )

    print(
        dataframe.head()
    )

    print(
        "\nColumns:\n"
    )

    print(
        dataframe.columns.tolist()
    )

    print(
        f"\nTotal records: "
        f"{len(dataframe)}"
    )