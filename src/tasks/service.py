from sqlalchemy import select

from models import User, get_async_session


async def get_users() -> list[User]:
    async_session = get_async_session()
    async with async_session() as session:
        stmt = select([User.chat_id, User.timezone, User.time_mailing])
        user = await session.execute(stmt)
        return user.fetchall()