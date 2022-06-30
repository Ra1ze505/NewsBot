import asyncio
import pytest
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import models
from config import settings, db


#  Setup test database connect for tests
async_test_engine = create_async_engine(db.async_connection_url + '_test', echo=True)


def get_test_async_session():
    return sessionmaker(
        async_test_engine, expire_on_commit=False, class_=AsyncSession
    )


models.get_async_session = get_test_async_session


def db_prep(conn_url: str):
    """Create test database"""
    engine = create_engine(conn_url)
    conn = engine.connect()
    try:
        conn = conn.execution_options(autocommit=False)
        conn.execute("ROLLBACK")
        conn.execute(f"DROP DATABASE {settings.DB_NAME}_test")
    except ProgrammingError:
        conn.execute("ROLLBACK")
    except OperationalError:
        conn.execute("ROLLBACK")
    conn.execute(f"CREATE DATABASE {settings.DB_NAME}_test")
    try:
        conn.execute(f"create user {settings.DB_USERNAME} with encrypted password '{settings.DB_PASSWORD}'")
    except:
        conn.execute(f"grant all privileges on database {settings.DB_NAME} to {settings.DB_USERNAME}")
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def fake_db():
    db_prep(db.connection_url)
    test_engine = create_engine(db.connection_url + '_test')
    db.Base.metadata.create_all(test_engine)
    yield
    db.Base.metadata.drop_all(test_engine)


@pytest.fixture
def fake_async_connect():
    test_async_session = get_test_async_session()
    yield test_async_session
    test_async_session.close_all()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
