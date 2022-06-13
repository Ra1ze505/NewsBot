import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, OperationalError

from src.config import settings

connection_url = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@' + \
                 f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

settings.DB_NAME = settings.DB_NAME + '_test'

from src.config import db


def db_prep(conn_url: str):
    engine = create_engine(conn_url)
    conn = engine.connect()
    try:
        conn = conn.execution_options(autocommit=False)
        conn.execute("ROLLBACK")
        conn.execute(f"DROP DATABASE {settings.DB_NAME}")
    except ProgrammingError:
        conn.execute("ROLLBACK")
    except OperationalError:
        conn.execute("ROLLBACK")
    conn.execute(f"CREATE DATABASE {settings.DB_NAME}")
    try:
        conn.execute(f"create user {settings.DB_USERNAME} with encrypted password '{settings.DB_PASSWORD}'")
    except:
        conn.execute(f"grant all privileges on database {settings.DB_NAME} to {settings.DB_USERNAME}")
    conn.close()


@pytest.fixture(scope="session")
def fake_db():
    db_prep(connection_url)
    engine = create_engine(db.connection_url)
    from src.models import User
    # from app.database import SessionLocal, Base
    # db = SessionLocal()
    db.Base.metadata.create_all(engine)