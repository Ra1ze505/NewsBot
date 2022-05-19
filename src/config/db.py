from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from .settings import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DRIVER


Base = declarative_base()
if DB_DRIVER == 'sqlite':
    connection_url = f'sqlite:///{DB_NAME}'
else:
    connection_url = f'{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(connection_url, echo=True)