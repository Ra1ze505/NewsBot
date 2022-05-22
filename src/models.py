from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config.db import Base, engine


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)


class NewsMessage(Base):
    __tablename__ = 'news_messages'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), unique=True)


def get_async_session():
    return sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )