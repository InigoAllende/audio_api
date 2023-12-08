from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_PATH: str
    API_KEYS: List[str]


settings = Settings()
