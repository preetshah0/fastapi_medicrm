from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Automatically looks for matching variables in .env
    APP_NAME: str = "MediCRM"
    APP_ENV: str = "local"
    APP_DEBUG: bool = True
    DATABASE_URL: str  # e.g., mysql+pymysql://user:pass@localhost/dbname
    SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()