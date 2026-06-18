import pandas as pd
from Extract import extract
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
        "roi"
                ]
    df = df[colunas].copy()
    df = df.dropna(

            subset=[
            "current_price",
            "market_cap"
        ]
    )
# Preenche valores ausentes da variação 24h
    df["price_change_percentage_24h"] = (
    df["price_change_percentage_24h"]
    .fillna(0)
        )


    # Extrair apenas o campo "times" do ROI
    df["roi_times"] = df["roi"].apply(
        lambda x: x.get("times")
        if isinstance(x, dict)
        else None
    )

    df = df.drop(columns=["roi"])

    df["volume_marketcap_ratio"] = (
        df["total_volume"] /
        df["market_cap"]
    )

    # Volatilidade absoluta
    df["volatility"] = (
        df["price_change_percentage_24h"]
        .abs()
    )
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
                "volatility"
            ]
        ] .sort_values("market_cap_rank")
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
                "volatility"
            ]
        ].describe()
    )