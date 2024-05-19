from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = ConfigDict(env_file = "docker.env")
    DEBUG: bool = True

    DB_HOST: str

    DB_PORT: str

    DB_NAME: str

    DB_USER: str

    DB_PASS: str

    JWT_SECRET: str

    BASE_URL: str = "http://localhost:1234"
    TEST_DB_NAME: str = "test"


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
