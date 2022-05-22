from sqlalchemy import select, func

from models import NewsMessage, get_async_session, User

async_session = get_async_session()


async def get_all_users():
    async with async_session() as session:
        stmt = select([User.chat_id, User.city])
        return await session.execute(stmt)


async def get_day_news():
    """
    Get news messages from database
    :return: NewsMessage
    """
    async with async_session() as session:
        sub_query = select([func.max(NewsMessage.created_at)]).scalar_subquery()
        stmt = select([NewsMessage.text]).where(NewsMessage.created_at == sub_query)
        result = await session.execute(stmt)
        return result.fetchone()
