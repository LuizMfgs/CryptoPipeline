from sqlalchemy import create_engine
from urllib.parse import quote_plus

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

encoded_password = quote_plus(DB_PASSWORD)
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print(DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)