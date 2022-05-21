from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, get_async_session


async_session = get_async_session()


async def commit(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()


async def user_create(chat_id):
    async with async_session() as session:
        user = User(chat_id=chat_id)
        session.add(user)
        await commit(session)



async def get_day_news():
    return 'Новости за день'


