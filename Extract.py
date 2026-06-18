import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"

def extract ():

    params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1
        }
    response = requests.get(
        url,
        params=params,
        timeout=30
                            )
    response.raise_for_status()
    return pd.DataFrame(response.json())
if __name__ == "__main__":

    df = extract()

    print(df.head())

    print(f"\nTotal records: {len(df)}")