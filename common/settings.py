from pydantic import BaseSettings


class Settings(BaseSettings):
    DEVELOPMENT: bool = True
    """
    Environment variable for setting testing and development code.
    """

    SQL_DATABASE_URI: str = "sqlite:///database.db"
    """
    Environment variable for the URI to the SQL database. 
    If not set, a local file is used for development.
    To use the in memory SQLite database (especially for testing), override this environment value.
    """


settings = Settings()

