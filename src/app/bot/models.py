from sqlalchemy import Column, Integer

from src.config.db import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
