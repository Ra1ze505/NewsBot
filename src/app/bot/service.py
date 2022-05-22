from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiohttp

from models import User, get_async_session
from config.settings import WEATHER_API_NOW_URL, WEATHER_API_KEY


async_session = get_async_session()


async def commit(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()


async def user_create(chat_id: int):
    async with async_session() as session:
        user = User(chat_id=chat_id)
        session.add(user)
        await commit(session)


async def get_user_city(chat_id: int):
    async with async_session() as session:
        stmt = select([User.city]).where(User.chat_id == chat_id)
        user = await session.execute(stmt)
        return user.fetchone().city


async def valid_city(city: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_NOW_URL.format(city=city, token=WEATHER_API_KEY)) as resp:
            if resp.status == 200:
                return True
            return False


async def user_city_update(chat_id: int, city: str):
    async with async_session() as session:
        stmt = User.__table__.update().where(User.chat_id == chat_id).values(city=city)
        await session.execute(stmt)
        await commit(session)


async def change_city(conv):
    city = await get_user_city(conv.chat_id)
    await conv.send_message(f'Ваш город сейчас: {city}\nНапишите свой город')
    new_city = await _get_city(conv)
    await user_city_update(conv.chat_id, new_city)
    await conv.send_message(f'Ваш регион изменен на: {new_city}')


async def _get_city(conv):
    answer = await conv.get_response()
    valid = await valid_city(answer.raw_text)
    if valid:
        return answer.raw_text
    else:
        await conv.send_message('Некорректный город\nПопробуйте еще раз')
        return await _get_city(conv)