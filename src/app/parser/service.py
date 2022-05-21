import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from telethon.tl.types import Message

from app.models import NewsMessage, get_async_session
from config.db import engine


logger = logging.getLogger(__name__)

async_session = get_async_session()


async def create_news(message: Message):
    """
    Create news from message
    :param message: telethon.Message
    :return:
    """
    async with async_session() as session:
        news = NewsMessage(text=message.message, created_at=message.date)
        session.add(news)
        try:
            await session.commit()
        except IntegrityError:
            logger.debug('News already exists')

