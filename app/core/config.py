from pydantic import BaseSettings


class Settings(BaseSettings):
    SQL_DATABASE_URI: str = None


settings = Settings()
