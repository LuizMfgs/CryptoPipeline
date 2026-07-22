def validate(df):

    errors = []

    if df.empty:
        errors.append("Dataset is empty.")

    if df["market_cap"].isna().any():
        errors.append("Missing market_cap values.")

    if df["current_price"].isna().any():
        errors.append("Missing current_price values.")

    if (df["current_price"] < 0).any():
        errors.append("Negative prices detected.")

    if (df["market_cap"] <= 0).any():
        errors.append("Invalid market_cap values.")

    if (df["total_volume"] < 0).any():
        errors.append("Negative trading volume detected.")

    if errors:

        print("\nDATA QUALITY ERRORS:")

        for error in errors:
            print(f"- {error}")

        return False

    print("Data Quality Checks Passed")

    return True

def quality_report(df):

    print("\n")
    print("=" * 50)
    print("QUALITY REPORT")
    print("=" * 50)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Missing Values: {df.isnull().sum().sum()}")
    print(f"Duplicate Rows: {df.duplicated().sum()}")
    print(f"Unique Coins: {df['id'].nunique()}")

    print(f"Average Price: ${df['current_price'].mean():,.2f}")
    print(f"Average Market Cap: ${df['market_cap'].mean():,.0f}")
    print(f"Average 24h Change: {df['price_change_percentage_24h'].mean():.2f}%")
    print(f"Average Liquidity Ratio: {df['liquidity_ratio'].mean():.2f}%")

    print("\n")
    print("=" * 50)
    print("QUALITY STATUS")
    print("=" * 50)

    if df.isnull().sum().sum() == 0:
        print("PASS - No missing values.")
    else:
        print("WARNING - Missing values found.")

    if df.duplicated().sum() == 0:
        print("PASS - No duplicate rows.")
    else:
        print("WARNING - Duplicate rows found.")

    if (df["current_price"] <= 0).any():
        print("WARNING - Invalid prices detected.")
    else:
        print("PASS - All prices are valid.")

    if (df["market_cap"] <= 0).any():
        print("WARNING - Invalid market cap values.")
    else:
        print("PASS - All market cap values are valid.")

    if (df["total_volume"] < 0).any():
        print("WARNING - Negative trading volume detected.")
    else:
        print("PASS - Trading volume values are valid.")
    