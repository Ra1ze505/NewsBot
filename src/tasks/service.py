from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiohttp

from app.bot.buttons import cansel_markup, start_markup
from models import User, get_async_session
from config.settings import WEATHER_API_NOW_URL, WEATHER_API_KEY


async def get_users():
    async_session = get_async_session()
    async with async_session() as session:
        stmt = select([User.chat_id, User.timezone, User.time_mailing])
        user = await session.execute(stmt)
        return user.fetchall()