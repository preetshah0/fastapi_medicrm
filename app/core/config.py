from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This automatically looks for a "DATABASE_URL" in .env
    APP_NAME: str = "MediCRM"
    DEBUG: bool = True
    DATABASE_URL: str  # e.g., postgresql://user:pass@localhost/dbname
    SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=".env",
                                        extra="ignore"
                                        )

settings = Settings()