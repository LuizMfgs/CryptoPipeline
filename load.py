import sqlite3

DATABASE = "data/crypto.db"

def load (df): 
    conn = sqlite3.connect(DATABASE)

    df.to_sql(
        "cryptocurrencies",
        conn,
        if_exists ="append",
        index=False
    )
    conn.commit()
    conn.close()

    print(
        f"{len(df)} records loaded successfully into {DATABASE}"
    )

    #TESTEEE
if __name__ == "__main__":
    from Extract import extract
    from transform import transform

    print("=" * 50)
    print("Loading Test")
    print("=" * 50)

    df = extract()
    transformed_df = transform(df)

    load(transformed_df)

    print("\nLoad completed sucessfully.")