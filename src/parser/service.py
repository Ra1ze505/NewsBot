import logging
from sqlalchemy.exc import IntegrityError
from telethon.tl.types import Message

from models import NewsMessage, get_async_session

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

