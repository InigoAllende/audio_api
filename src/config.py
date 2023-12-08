from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_PATH: str
    API_KEY: str


settings = Settings()
