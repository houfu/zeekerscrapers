from pydantic import BaseSettings


class Settings(BaseSettings):
    DEVELOPMENT: bool = True
    """
    Environment variable for setting testing and development code.
    """

    SQL_DATABASE_URI: str = "sqlite://"
    """
    Environment variable for the URI to the SQL database. If not set, the in-memory database is used for
    development and testing
    """


settings = Settings()

