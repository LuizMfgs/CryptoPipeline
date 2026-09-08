from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parents[1]

LOG_DIR = BASE_DIR / "logs"


# APPLICATION SETTINGS

class Settings(BaseSettings):

    # Application

    APP_NAME: str = "Crypto ETL"
    ENVIRONMENT: str = "development"

    # CoinGecko API

    COINGECKO_BASE_URL: str = (
        "https://api.coingecko.com/api/v3"
    )

    COINGECKO_MARKETS_ENDPOINT: str = (
        "/coins/markets"
    )

    VS_CURRENCY: str = "usd"

    ORDER: str = "market_cap_desc"

    PER_PAGE: int = 100

    TOTAL_PAGES: int = 5

    # HTTP / Retry


    REQUEST_TIMEOUT: int = 30

    MAX_RETRIES: int = 3

    BACKOFF_FACTOR: float = 2.0

    REQUEST_DELAY: float = 1.0

    RETRY_STATUS_CODES: tuple[int, ...] = (
        429,
        500,
        502,
        503,
        504,
    )

    # PostgreSQL

    POSTGRES_HOST: str = "localhost"

    POSTGRES_PORT: int = 5432

    POSTGRES_DB: str = "Crypto_Market"

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: str = ""

    # Data retention

    DATA_RETENTION_DAYS: int = 7

    # Logging

    LOG_LEVEL: str = "INFO"

    LOG_FILE: str = "pipeline.log"

    # Pydantic configuration

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # DERIVED CONFIGURATION


    @property
    def DATABASE_URL(self) -> str:

        return (
            "postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def COINGECKO_MARKETS_URL(self) -> str:

        return (
            f"{self.COINGECKO_BASE_URL}"
            f"{self.COINGECKO_MARKETS_ENDPOINT}"
        )


# SETTINGS INSTANCE

settings = Settings()
