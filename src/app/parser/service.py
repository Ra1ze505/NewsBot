import json
import logging

import aiohttp
from sqlalchemy.exc import IntegrityError
from telethon.tl.types import Message

from config.settings import WEATHER_API_URL, WEATHER_API_KEY, CURRENCY_API_URL
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

    async def get_pretty_weather(self, city: str):
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