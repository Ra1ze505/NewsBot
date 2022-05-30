from sqlalchemy import select, func

from models import NewsMessage, get_async_session, User, Rate


async_session = get_async_session()

PRETTY_RATE_MESSAGE = '''
**Курс валют на сегодня**
Доллар: {usd}
Евро: {eur}
'''


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


async def get_pretty_rate() -> str:
    rate = await _get_last_rate()
    usd = round(rate.data['USD']['Value'], 2)
    eur = round(rate.data['EUR']['Value'], 2)
    return PRETTY_RATE_MESSAGE.format(usd=usd, eur=eur)


async def _get_last_rate() -> Rate:
    async with async_session() as session:
        sub_query = select([func.max(Rate.date)]).scalar_subquery()
        stmt = select([Rate.data]).where(Rate.date == sub_query)
        result = await session.execute(stmt)
        return result.fetchone()
