from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)


class LogConfig(Config):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="log_")
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class ServiceConfig(Config):
    service_name: str = "reco_service"
    k_recs: int = 10

    log_config: LogConfig


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )


class Settings(BaseSettings):
    APP_NAME: str = "Reco Service"
    API_VERSION: str = "production"
    API_DESCRIPTION: str = "Reco Service For AI Talent Hub"

    DEBUG: bool = False

    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_ORIGINS: List[str] = ["*"]

    SECRET_KEY: SecretStr = SecretStr("09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"


settings = Settings()
