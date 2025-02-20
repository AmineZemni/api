# from pydantic import BaseSettings

from pydantic_settings import BaseSettings # type: ignore


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/fastapi_db"

    class Config:
        env_file = ".env"

settings = Settings()
