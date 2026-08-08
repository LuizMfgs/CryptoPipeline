import pandas as pd


REQUIRED_COLUMNS = [
    "coin_id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "market_cap_rank",
    "total_volume",
    "price_change_percentage_24h",
    "ath_change_percentage",
    "liquidity_ratio",
    "etl_timestamp",
]


def check_not_empty(df: pd.DataFrame) -> dict:
    passed = not df.empty

    return {
        "check": "dataset_not_empty",
        "passed": passed,
        "message": (
            "Dataset contains records."
            if passed
            else "Dataset is empty."
        ),
    }


def check_required_columns(df: pd.DataFrame) -> dict:
    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return {
        "check": "required_columns",
        "passed": not missing,
        "message": (
            "All required columns are present."
            if not missing
            else f"Missing columns: {missing}"
        ),
    }


def check_required_values(df: pd.DataFrame) -> dict:
    columns = [
        "coin_id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "total_volume",
        "etl_timestamp",
    ]

    missing = {
        column: int(df[column].isna().sum())
        for column in columns
        if column in df.columns
        and df[column].isna().any()
    }

    return {
        "check": "required_values_not_null",
        "passed": not missing,
        "message": (
            "No NULL values in required fields."
            if not missing
            else f"NULL values detected: {missing}"
        ),
    }


def check_duplicate_coins(df: pd.DataFrame) -> dict:
    if "coin_id" not in df.columns:
        return {
            "check": "unique_coin_id",
            "passed": False,
            "message": "coin_id column is missing.",
        }

    duplicates = int(
        df["coin_id"].duplicated().sum()
    )

    return {
        "check": "unique_coin_id",
        "passed": duplicates == 0,
        "message": (
            "No duplicated coin IDs."
            if duplicates == 0
            else f"{duplicates} duplicated coin IDs."
        ),
    }


def check_prices(df: pd.DataFrame) -> dict:
    if "current_price" not in df.columns:
        return {
            "check": "valid_current_price",
            "passed": False,
            "message": "current_price column is missing.",
        }

    invalid = int(
        (df["current_price"] <= 0).sum()
    )

    return {
        "check": "valid_current_price",
        "passed": invalid == 0,
        "message": (
            "All prices are valid."
            if invalid == 0
            else f"{invalid} invalid prices detected."
        ),
    }


def check_market_cap(df: pd.DataFrame) -> dict:
    if "market_cap" not in df.columns:
        return {
            "check": "valid_market_cap",
            "passed": False,
            "message": "market_cap column is missing.",
        }

    invalid = int(
        (df["market_cap"] <= 0).sum()
    )

    return {
        "check": "valid_market_cap",
        "passed": invalid == 0,
        "message": (
            "All market cap values are valid."
            if invalid == 0
            else f"{invalid} invalid market cap values."
        ),
    }


def check_volume(df: pd.DataFrame) -> dict:
    if "total_volume" not in df.columns:
        return {
            "check": "valid_total_volume",
            "passed": False,
            "message": "total_volume column is missing.",
        }

    invalid = int(
        (df["total_volume"] < 0).sum()
    )

    return {
        "check": "valid_total_volume",
        "passed": invalid == 0,
        "message": (
            "All volume values are valid."
            if invalid == 0
            else f"{invalid} negative volume values."
        ),
    }


def check_liquidity(df: pd.DataFrame) -> dict:
    if "liquidity_ratio" not in df.columns:
        return {
            "check": "valid_liquidity_ratio",
            "passed": False,
            "message": "liquidity_ratio column is missing.",
        }

    invalid = int(
        (
            (df["liquidity_ratio"] < 0)
            | (df["liquidity_ratio"] > 100)
        ).sum()
    )

    return {
        "check": "valid_liquidity_ratio",
        "passed": invalid == 0,
        "message": (
            "Liquidity ratio values are valid."
            if invalid == 0
            else f"{invalid} invalid liquidity ratios."
        ),
    }


def check_market_cap_rank(df: pd.DataFrame) -> dict:
    if "market_cap_rank" not in df.columns:
        return {
            "check": "valid_market_cap_rank",
            "passed": False,
            "message": "market_cap_rank column is missing.",
        }

    invalid = int(
        (df["market_cap_rank"] <= 0).sum()
    )

    return {
        "check": "valid_market_cap_rank",
        "passed": invalid == 0,
        "message": (
            "All market cap ranks are valid."
            if invalid == 0
            else f"{invalid} invalid market cap ranks."
        ),
    }


def run_quality_checks(df: pd.DataFrame) -> dict:
    """
    Execute all data quality checks.
    """

    checks = [
        check_not_empty,
        check_required_columns,
        check_required_values,
        check_duplicate_coins,
        check_prices,
        check_market_cap,
        check_volume,
        check_liquidity,
        check_market_cap_rank,
    ]

    results = [
        check(df)
        for check in checks
    ]

    passed = all(
        result["passed"]
        for result in results
    )

    return {
        "passed": passed,
        "total_checks": len(results),
        "passed_checks": sum(
            result["passed"]
            for result in results
        ),
        "failed_checks": sum(
            not result["passed"]
            for result in results
        ),
        "results": results,
    }