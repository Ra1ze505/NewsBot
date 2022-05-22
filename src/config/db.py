from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from .settings import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT


Base = declarative_base()
connection_url = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'  # for alembic
async_connection_url = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(async_connection_url, echo=True)