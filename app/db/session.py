from sqlmodel import create_engine, SQLModel

from app.core.config import settings

engine = create_engine(settings.SQL_DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
