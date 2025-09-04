from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name:str
    app_version:str
    debug:bool

    database_url: str
    database_url_sync: str

    allowed_origins: List[str] = ["*"]


    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()

setting=get_settings()
