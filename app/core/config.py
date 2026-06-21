from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This automatically looks for a "DATABASE_URL" in .env
    APP_NAME: str = "Medi CRM"
    DEBUG: bool = True
    DATABASE_URL: str  # e.g., postgresql://user:pass@localhost/dbname
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env",
                                        extra="ignore"
                                        )

settings = Settings()