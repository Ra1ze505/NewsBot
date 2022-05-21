from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config.db import engine

from app.bot.models import User


async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )


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


async def get_all_users():
    async with async_session() as session:
        stmt = select([User.chat_id])
        return await session.execute(stmt)


async def get_day_news():
    return 'Новости за день'


