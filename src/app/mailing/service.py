from sqlalchemy import select, func

from models import NewsMessage, get_async_session, User

async_session = get_async_session()


async def get_all_users() -> list[User]:
    async with async_session() as session:
        stmt = select([User.chat_id, User.city])
        return await session.execute(stmt)


async def get_user_by_chat_id(chat_id) -> User:
    async with async_session() as session:
        stmt = select([User.chat_id, User.city]).where(User.chat_id == chat_id)
        result = await session.execute(stmt)
        return result.fetchone()


async def get_day_news() -> NewsMessage:
    async with async_session() as session:
        sub_query = select([func.max(NewsMessage.created_at)]).scalar_subquery()
        stmt = select([NewsMessage.text]).where(NewsMessage.created_at == sub_query)
        result = await session.execute(stmt)
        return result.fetchone()
