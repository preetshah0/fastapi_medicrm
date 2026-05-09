from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This automatically looks for a "DATABASE_URL" in your .env
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()