from sqlalchemy import text

from app.Database.Database import engine


def reset_database():
    """
    Remove todos os registros da tabela cryptocurrencies
    e reinicia o contador da chave primária (caso exista).
    """

    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "TRUNCATE TABLE cryptocurrencies RESTART IDENTITY;"
                )
            )

        print("Database reset completed.")

    except Exception as error:
        print(f"Database reset failed: {error}")
        raise


if __name__ == "__main__":
    reset_database()