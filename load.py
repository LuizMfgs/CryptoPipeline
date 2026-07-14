import sqlite3
import logging

DATABASE = "data/crypto.db"
TABLE_NAME = "cryptocurrencies"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def table_exists(conn):

    cursor = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (TABLE_NAME,)
    )

    return cursor.fetchone() is not None


def get_table_columns(conn):

    cursor = conn.execute(
        f"PRAGMA table_info({TABLE_NAME})"
    )

    return [
        row[1]
        for row in cursor.fetchall()
    ]


def schema_changed(conn, df):

    if not table_exists(conn):
        return True

    db_columns = get_table_columns(conn)

    df_columns = list(df.columns)

    return db_columns != df_columns


def recreate_table(conn):

    logging.warning(
        "Schema changed. Recreating table..."
    )

    conn.execute(
        f"DROP TABLE IF EXISTS {TABLE_NAME}"
    )

    conn.commit()


def load(df):

    conn = sqlite3.connect(DATABASE)

    try:

        if schema_changed(conn, df):

            recreate_table(conn)

            mode = "replace"

        else:

            mode = "append"

        df.to_sql(
            TABLE_NAME,
            conn,
            if_exists=mode,
            index=False
        )

        conn.commit()

        logging.info(
            f"{len(df)} records loaded successfully."
        )

    finally:

        conn.close()


# ===========================================
# TEST
# ===========================================

if __name__ == "__main__":

    from Extract import extract
    from transform import transform

    print("=" * 50)
    print("Loading Test")
    print("=" * 50)

    df = extract()

    transformed_df = transform(df)

    load(transformed_df)

    print("\nLoad completed successfully.")