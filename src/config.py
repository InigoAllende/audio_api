from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_PATH: str


settings = Settings()
