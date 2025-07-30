from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_CONNECT_URL: str
    JWT_SECURE_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_IN_MINUTES: int
    REDIS_CONNECT_URL: str

    model_config = SettingsConfigDict(env_file=".env")

app_settings = Settings()
