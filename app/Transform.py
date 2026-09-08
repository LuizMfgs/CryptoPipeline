import logging
from datetime import datetime, timezone
import pandas as pd
from app.Extract import extract

logger = logging.getLogger(__name__)

# REQUIRED COLUMNS

REQUIRED_COLUMNS = [
    "id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "market_cap_rank",
    "total_volume",
    "price_change_percentage_24h",
    "ath_change_percentage",
]


# VALIDATION

def validate_columns(df: pd.DataFrame) -> None:
    """
    Validate whether all required columns
    are present in the extracted dataset.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


# SELECT COLUMNS

def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select only the columns required by
    the transformation pipeline.
    """

    return df[REQUIRED_COLUMNS].copy()


# STANDARDIZE COLUMN NAMES

def standardize_column_names(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize external API column names
    according to the internal data model.

    CoinGecko:
        id

    Internal model:
        coin_id
    """

    return df.rename(
        columns={
            "id": "coin_id",
        }
    ).copy()


# CLEAN DATA

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the extracted data.
    """

    logger.info("Starting data cleaning...")

    # Remove records without critical values

    before = len(df)

    df = df.dropna(
        subset=[
            "current_price",
            "market_cap",
        ]
    ).copy()

    removed = before - len(df)

    if removed > 0:
        logger.warning(
            "Removed %s records with missing "
            "critical values.",
            removed,
        )

    # Standardize symbol

    df["symbol"] = (
        df["symbol"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Convert numeric columns

    numeric_columns = [
        "current_price",
        "market_cap",
        "market_cap_rank",
        "total_volume",
        "price_change_percentage_24h",
        "ath_change_percentage",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Fill optional values

    df["price_change_percentage_24h"] = (
        df["price_change_percentage_24h"]
        .fillna(0)
    )

    df["ath_change_percentage"] = (
        df["ath_change_percentage"]
        .fillna(0)
    )

    return df


# METRICS

def calculate_metrics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate derived metrics used by
    the analytics layer.
    """

    logger.info("Calculating derived metrics...")

    # Liquidity Ratio

    df["liquidity_ratio"] = (
        (
            df["total_volume"]
            / df["market_cap"]
        ) * 100
    ).round(2)

    # Replace invalid/infinite values

    df["liquidity_ratio"] = (
        df["liquidity_ratio"]
        .replace(
            [float("inf"), float("-inf")],
            0,
        )
        .fillna(0)
    )

    return df


# REMOVE DUPLICATES

def remove_duplicates(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove duplicated cryptocurrencies inside
    the current extraction only.

    Historical snapshots are NOT removed here.
    """

    before = len(df)

    df = df.drop_duplicates(
        subset=["coin_id"],
        keep="last",
    ).copy()

    removed = before - len(df)

    if removed > 0:
        logger.warning(
            "Removed %s duplicated records "
            "from current extraction.",
            removed,
        )

    return df


# ETL TIMESTAMP

def add_etl_timestamp(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add the timestamp associated with this
    ETL execution.
    """

    df["etl_timestamp"] = datetime.now(
        timezone.utc
    )

    return df


# MAIN TRANSFORMATION

def transform(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transform raw CoinGecko data into a
    clean dataset ready for PostgreSQL.
    """

    logger.info("Starting transformation...")

    # Empty dataset

    if df.empty:
        logger.warning(
            "Received empty DataFrame."
        )
        return df

    # 1. Validate API columns

    validate_columns(df)

    # 2. Select required API columns

    df = select_columns(df)

    # 3. Convert API naming to internal naming

    df = standardize_column_names(df)

    # 4. Clean data

    df = clean_data(df)

    # 5. Remove duplicates from current extraction

    df = remove_duplicates(df)

    # 6. Calculate derived metrics

    df = calculate_metrics(df)

    # 7. Add ETL execution timestamp

    df = add_etl_timestamp(df)

    logger.info(
        "Transformation finished: %s records.",
        len(df),
    )

    return df


# TEST

if __name__ == "__main__":

    print("=" * 50)
    print("EXTRACT PHASE")
    print("=" * 50)

    df = extract()

    print(
        f"Records extracted: {len(df)}"
    )

    print("\nOriginal columns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows from API:")
    print(df.head())

    print("\n" + "=" * 50)
    print("TRANSFORM PHASE")
    print("=" * 50)

    transformed_df = transform(df)

    print(
        f"Records after transform: "
        f"{len(transformed_df)}"
    )

    print("\nColumns after transform:")
    print(
        transformed_df.columns.tolist()
    )

    print(
        "\nTop 20 Cryptocurrencies "
        "by Market Cap Rank:"
    )

    print(
        transformed_df[
            [
                "market_cap_rank",
                "coin_id",
                "name",
                "symbol",
                "current_price",
                "market_cap",
                "price_change_percentage_24h",
                "ath_change_percentage",
                "liquidity_ratio",
                "etl_timestamp",
            ]
        ]
        .sort_values("market_cap_rank")
        .head(20)
    )

    print("\nDataset information:")
    transformed_df.info()

    print("\nDescriptive statistics:")

    print(
        transformed_df[
            [
                "current_price",
                "market_cap",
                "price_change_percentage_24h",
                "ath_change_percentage",
                "liquidity_ratio",
            ]
        ].describe()
    )
