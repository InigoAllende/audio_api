from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_PATH: str
    API_KEY: str
    ENCRYPTION_KEY: str


settings = Settings()
