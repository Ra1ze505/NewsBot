import asyncio
import logging
from typing import Optional

import aiohttp
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from telethon.tl.types import Message

from config.settings import WEATHER_API_URL, WEATHER_API_KEY, CURRENCY_API_URL, WEATHER_API_NOW_URL
from models import NewsMessage, Rate, get_async_session, User, Weather

logger = logging.getLogger(__name__)

async_session = get_async_session()

PRETTY_WEATHER_MESSAGE = '''
**Погода в городе {city}**
В течении дня:
-- Cредняя температура  {mean_temp}°C
-- Максимальная температура {max_temp}°C
-- Минимальная температура {min_temp}°C'''

PRETTY_WEATHER_NOW_MESSAGE = '''
**Погода в городе {city}:**
{description}
Температура: {temp}°C
Ветер {wind_direction}
Скорость ветра: {wind_speed} м/с
Влажность: {humidity}%
Облачность: {clouds_all}%
'''

TIMEOUT_SECONDS = 5


def timeout_exception_handler(error_msg: str) -> None:
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except asyncio.TimeoutError:
                logger.error('Timeout error')
                return error_msg

        return wrapper

    return decorator


async def create_news(message: Message) -> None:
    """
    Create news from message
    :param message: telethon.Message
    """
    async with async_session() as session:
        news = NewsMessage(text=message.message, created_at=message.date)
        session.add(news)
        try:
            await session.commit()
        except IntegrityError:
            logger.debug('News already exists')


async def create_rate(data: dict) -> None:
    """
    Create rate from data
    :param data: dict
    """
    async with async_session() as session:
        rate = Rate(data=data)
        session.add(rate)
        await session.commit()


async def get_all_cities() -> list[str]:
    """
    Get all users cities
    :return: list cities
    """
    async with async_session() as session:
        stmt = select(User.city).distinct(User.city)
        users = await session.execute(stmt)
        return [user.city for user in users.fetchall()]


async def create_weather(data: list[dict]) -> None:
    """
    Bulk create weather in database
    :param data: list of items dict from OpenWeatherApi
    :return: None
    """
    async with async_session() as session:
        items = [Weather(city=item.get('city'), data=item) for item in data]
        session.add_all(items)
        await session.commit()


async def get_weather_data_by_day(city: str) -> Optional[dict]:
    """
    Get last row Weather in database
    :param city: str
    :return: dict with weather data or None
    """
    async with async_session() as session:
        stmt = select(Weather.data).where(Weather.city == city).order_by(Weather.date.desc())
        weather = await session.execute(stmt)
        result = weather.fetchone()
        if result is not None:
            return result.data


class WeatherService:
    ERROR_MESSAGE = 'Не удалось получить погоду. Попробуйте позже'

    @timeout_exception_handler(ERROR_MESSAGE)
    async def get_pretty_weather_by_day(self, city: str) -> str:
        weather = await get_weather_data_by_day(city)

        if weather is None:  # Not in db
            weather = await self._get_weather_by_day(city)

        min_temp = int(min([temp['main']['temp_min'] for temp in weather['list']]))
        max_temp = int(max([temp['main']['temp_max'] for temp in weather['list']]))
        mean_temp = int(sum([temp['main']['temp'] for temp in weather['list']]) / len(weather['list']))

        return PRETTY_WEATHER_MESSAGE.format(city=city, mean_temp=mean_temp, max_temp=max_temp, min_temp=min_temp)

    @timeout_exception_handler(ERROR_MESSAGE)
    async def get_pretty_weather(self, city: str) -> str:
        weather_data = await self._get_weather(city)
        return PRETTY_WEATHER_NOW_MESSAGE.format(city=city,
                                                 description=weather_data["weather"][0]["description"].title(),
                                                 temp=int(weather_data["main"]["temp"]),
                                                 wind_direction=_get_wind_direction(weather_data["wind"]["deg"]),
                                                 wind_speed=int(weather_data["wind"]["speed"]),
                                                 humidity=int(weather_data["main"]["humidity"]),
                                                 clouds_all=int(weather_data["clouds"]["all"]))

    async def _get_weather(self, city: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_NOW_URL.format(city=city, token=WEATHER_API_KEY),
                                   timeout=TIMEOUT_SECONDS) as resp:
                return await resp.json()

    async def _get_weather_by_day(self, city: str) -> dict:
        async with aiohttp.ClientSession() as session:
            url = WEATHER_API_URL.format(city=city, token=WEATHER_API_KEY)
            async with session.get(url, timeout=TIMEOUT_SECONDS) as resp:
                return await resp.json()

    async def parse_weather_by_cities(self, cities: list[str]) -> list[dict]:
        result = []
        for city in cities:
            _result = await self._get_weather_by_day(city)
            _result['city'] = city
            result.append(_result)
        return result


def _get_wind_direction(wind_deg: int) -> str:
    if 337.5 <= wind_deg < 360 or 0 <= wind_deg < 22.5:
        return 'северный'
    elif 22.5 <= wind_deg < 67.5:
        return 'северо-восточный'
    elif 67.5 <= wind_deg < 112.5:
        return 'восточный'
    elif 112.5 <= wind_deg < 157.5:
        return 'юго-восточный'
    elif 157.5 <= wind_deg < 202.5:
        return 'южный'
    elif 202.5 <= wind_deg < 247.5:
        return 'юго-западный'
    elif 247.5 <= wind_deg < 292.5:
        return 'западный'
    elif 292.5 <= wind_deg < 337.5:
        return 'северо-западный'
