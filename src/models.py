import datetime
from sqlalchemy import Column, Integer, Text, DateTime, func, String, Time, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config.db import Base, engine


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    city = Column(String(50), default='Москва')
    timezone = Column(Integer, default=3)
    time_mailing = Column(Time, default=datetime.time(hour=8, minute=0))


class NewsMessage(Base):
    __tablename__ = 'news_messages'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), unique=True)


class Rate(Base):
    __tablename__ = 'rate'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    date = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.chat_id'))
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Weather(Base):
    __tablename__ = 'weather'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    city = Column(String)
    data = Column(JSON)
    date = Column(DateTime(timezone=True), server_default=func.now())


def get_async_session():
    return sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
