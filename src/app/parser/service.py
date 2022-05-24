import json
import logging

import aiohttp
from sqlalchemy.exc import IntegrityError
from telethon.tl.types import Message

from app.bot.service import get_user_city
from config.settings import WEATHER_API_URL, WEATHER_API_KEY, CURRENCY_API_URL, WEATHER_API_NOW_URL
from models import NewsMessage, get_async_session

logger = logging.getLogger(__name__)

async_session = get_async_session()

PRETTY_WEATHER_MESSAGE = '''**Погода в городе {city}**
В течении дня:
-- Cредняя температура  {mean_temp}°C
-- Максимальная температура {max_temp}°C
-- Минимальная температура {min_temp}°C'''

PRETTY_RATE_MESSAGE = '''**Курс валют на сегодня**
Доллар: {usd}
Евро: {eur}
'''

PRETTY_WEATHER_NOW_MESSAGE = '''
**Погода в городе {city}:**
{description}
Температура: {temp}°C
Ветер {wind_direction}
Скорость ветра: {wind_speed} м/с
Влажность: {humidity}%
Облачность: {clouds_all}%
'''


async def create_news(message: Message):
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


class Weather:
    def __init__(self):
        pass

    async def _get_weather(self, city: str):
        async with aiohttp.ClientSession() as session:
            url = WEATHER_API_URL.format(city=city, token=WEATHER_API_KEY)
            async with session.get(url) as resp:
                return await resp.json()

    async def get_pretty_weather_by_day(self, city: str):
        weather = await self._get_weather(city)

        min_temp = int(min([temp['main']['temp_min'] for temp in weather['list']]))
        max_temp = int(max([temp['main']['temp_max'] for temp in weather['list']]))
        mean_temp = int(sum([temp['main']['temp'] for temp in weather['list']]) / len(weather['list']))

        return PRETTY_WEATHER_MESSAGE.format(city=city, mean_temp=mean_temp, max_temp=max_temp, min_temp=min_temp)


async def get_pretty_rate():
    """
    Get pretty rate
    :return: str
    """
    rate = await _get_rate()
    return PRETTY_RATE_MESSAGE.format(usd=rate['Valute']['USD']['Value'], eur=rate['Valute']['EUR']['Value'])


async def _get_rate():
    async with aiohttp.ClientSession() as session:
        url = CURRENCY_API_URL
        async with session.get(url) as resp:
            data = await resp.read()
            data_json = json.loads(data)
            return data_json


async def get_weather(chat_id: int):
    city = await get_user_city(chat_id)
    return await get_pretty_weather(city)


async def get_pretty_weather(city: str):
    weather_data = await _get_weather(city)
    return PRETTY_WEATHER_NOW_MESSAGE.format(city=city, description=weather_data["weather"][0]["description"].title(),
                                             temp=int(weather_data["main"]["temp"]),
                                             wind_direction=_get_wind_direction(weather_data["wind"]["deg"]),
                                             wind_speed=int(weather_data["wind"]["speed"]),
                                             humidity=int(weather_data["main"]["humidity"]),
                                             clouds_all=int(weather_data["clouds"]["all"]))


async def _get_weather(city: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_NOW_URL.format(city=city, token=WEATHER_API_KEY)) as resp:
            return await resp.json()


def _get_wind_direction(wind_deg: int):
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


