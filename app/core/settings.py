from pydantic import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "The Biill"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "prd"
    APP_PATH: str = "/api"

    DATABASE_URL: PostgresDsn
    RABBITMQ_HOST: AmqpDsn
    RABBITMQ_QUEUE: str

    SECRET_KEY: str

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )


settings = Settings()
