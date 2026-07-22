import requests
import pandas as pd
import time
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


#CONFIGURAÇÕES BÁSICAS#

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

VS_CURRENCY = "usd"
ORDER = "market_cap_desc"

REQUEST_DELAY = 2
REQUEST_TIMEOUT = 30

MAX_RETRIES = 3
BACKOFF_FACTOR = 2

PER_PAGE = 100
TOTAL_PAGES = 5

#LOGGING#

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

#SESSION CON ENTRY#

retry_strategy = Retry(
    total=MAX_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    status_forcelist=[
    429,
    500,
    502,
    503,
    504
],
    allowed_methods=["GET"],
    respect_retry_after_header=True)

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

#Extraction#
def extract(total_pages=TOTAL_PAGES):
    all_data = []
    logger.info("starting extraction...")
    for page in range (1,total_pages + 1):
        logger.info(
            f"Extracting page {page}/{total_pages}"
        )
        params = {
        "vs_currency": VS_CURRENCY,
        "order": ORDER,
        "per_page": PER_PAGE,
        "page": page
        }
        try:

            response = session.get(
                    BASE_URL,
                    params=params,
                    timeout=REQUEST_TIMEOUT
                )
     
            response.raise_for_status()

            page_data = response.json()

            if not page_data:

                    logger.info("No more data available.")
                    break

                

            logger.info(
                    f"Page {page}: "
                    f"{len(page_data)} records"
                )
            all_data.extend(page_data)

            time.sleep(REQUEST_DELAY)

            

        except requests.exceptions.RequestException as error:

                logger.error(
                    f"Page {page}: {error}"
                )
                continue
    df = pd.DataFrame(all_data)
    if df.empty:
        logger.error(
        "No data returned from API."
    )
    logger.info(
    f"Extraction finished: {len(df)} total records.")
    return df

#TESTE#
if __name__ == "__main__":

    dataframe = extract()

    print("\nFirst five rows:\n")

    print(dataframe.head())

    print("\nColumns:\n")

    print(dataframe.columns.tolist())

    print(f"\nTotal records:{len(dataframe)}")