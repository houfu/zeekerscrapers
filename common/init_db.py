from sqlmodel.pool import StaticPool
from sqlmodel import create_engine, SQLModel

from common.settings import settings

if settings.DEVELOPMENT:
    engine = create_engine(settings.SQL_DATABASE_URI, connect_args={"check_same_thread": False},
                           poolclass=StaticPool, echo=True)
else:
    engine = create_engine(settings.SQL_DATABASE_URI)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
