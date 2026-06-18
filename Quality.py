def validate(df):
    if df.empty:
        raise ValueError(
            "Dataset is empty"
        )

    if df["market_cap"].isna().any():
        raise ValueError(
            "Missing market_cap values"
        )

    if df["current_price"].isna().any():
        raise ValueError(
            "Missing current_price values"
        )

    if (df["current_price"] < 0).any():
        raise ValueError(
            "Negative prices detected"
        )

    print(
        "Data Quality Checks Passed"
    )


def quality_report(df):

    print("\n")
    print("=" * 50)
    print("QUALITY REPORT")
    print("=" * 50)

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print(
        f"Missing Values: "
        f"{df.isna().sum().sum()}"
    )

    print(
        f"Duplicate Rows: "
        f"{df.duplicated().sum()}"
    )

    print(
        f"Unique Coins: "
        f"{df['symbol'].nunique()}"
    )

    print(
        f"Average Price: "
        f"${df['current_price'].mean():,.2f}"
    )

    print(
        f"Average Volatility: "
        f"{df['volatility'].mean():.2f}%"
    )

    print(
        f"Highest Price: "
        f"${df['current_price'].max():,.2f}"
    )

    print(
        f"Largest Market Cap: "
        f"${df['market_cap'].max():,.0f}"
    )