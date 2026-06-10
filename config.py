from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str

    # Anthropic
    anthropic_api_key: str = ""

    # App
    app_name: str = "MeridianAI"
    debug: bool = False
    allowed_origins: list[str] = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]

    # Model
    model_path: str = "model.joblib"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
