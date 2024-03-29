from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DEBUG: bool = True

    DB_HOST: str = "localhost"

    DB_PORT: str = "5432"

    DB_NAME: str = "postgres"

    DB_USER: str = "postgres"

    DB_PASS: str

    TEST_DB_NAME: str

    SUPABASE_URL: str = "http://213.171.3.136:8000"
    SUPABASE_KEY: str 

    class Config:
        env_file = ".env"

    @property
    def db_url_postgresql(self) -> str:
        """Product db url."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def test_db_url_postgresql(self) -> str:
        if self.TEST_DB_NAME:
            return (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"
            )

        return self.db_url_postgresql


settings = Settings()
