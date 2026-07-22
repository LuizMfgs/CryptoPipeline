import pandas as pd
from app.Extract import extract
from datetime import datetime
import pandas as pd

def transform(df):
    
    colunas = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "total_volume",
        "price_change_percentage_24h",
        "ath_change_percentage"
                ]
    df = df[colunas].copy()
    df = df.dropna(

            subset=[
            "current_price",
            "market_cap"
        ]
    )
 # Preenche valores ausentes
    df["price_change_percentage_24h"] = (
        df["price_change_percentage_24h"]
        .fillna(0)
    )

    df["ath_change_percentage"] = (
        df["ath_change_percentage"]
        .fillna(0)
    )

    # Liquidity Ratio (%)
    df["liquidity_ratio"] = (
        (
            df["total_volume"] /
            df["market_cap"]
        ) * 100
    ).round(2)

    # Timestamp da execução
    df["etl_timestamp"] = datetime.now()

    return df


if __name__ == "__main__":

    print("=" * 50)
    print("EXTRACT PHASE")
    print("=" * 50)

    df = extract()

    print(f"Records extracted: {len(df)}")

    print("\nOriginal columns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows from API:")
    print(df.head())

    print("\n" + "=" * 50)
    print("TRANSFORM PHASE")
    print("=" * 50)

    transformed_df = transform(df)

    print(f"Records after transform: {len(transformed_df)}")

    print("\nColumns after transform:")
    print(transformed_df.columns.tolist())

    print("\nTop 20 Cryptocurrencies by Market Cap Rank:")

    print(
        transformed_df[
            [
                "market_cap_rank",
                "name",
                "symbol",
                "current_price",
                "market_cap",
                "price_change_percentage_24h",
                "ath_change_percentage",
                "liquidity_ratio"
            ]
        ]
        .sort_values("market_cap_rank")
        .head(20)
    )

    print("\nDataset information:")
    print(transformed_df.info())

    print("\nDescriptive statistics:")
    print(
        transformed_df[
            [
                "current_price",
                "market_cap",
                "price_change_percentage_24h",
                "ath_change_percentage",
                "liquidity_ratio"
            ]
        ].describe()
    )