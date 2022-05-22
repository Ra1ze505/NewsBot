import logging

import aiohttp
from sqlalchemy.exc import IntegrityError
from telethon.tl.types import Message

from config.settings import WEATHER_API_URL, WEATHER_API_KEY
from models import NewsMessage, get_async_session

logger = logging.getLogger(__name__)

async_session = get_async_session()

PRETTY_MESSAGE = '''{city} 
Cредняя температура {mean_temp}°C
Максимальная температура {max_temp}°C
Минимальная температура {min_temp}°C'''


async def create_news(message: Message):
    """
    Create news from message
    :param message: telethon.Message
    :return:
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

    async def _get_weather(self, city):
        async with aiohttp.ClientSession() as session:
            url = WEATHER_API_URL.format(city=city, token=WEATHER_API_KEY)
            async with session.get(url) as resp:
                return await resp.json()

    async def get_pretty_weather(self, city):
        weather = await self._get_weather(city)

        min_temp = int(min([temp['main']['temp_min'] for temp in weather['list']]))
        max_temp = int(max([temp['main']['temp_max'] for temp in weather['list']]))
        mean_temp = int(sum([temp['main']['temp'] for temp in weather['list']]) / len(weather['list']))

        return PRETTY_MESSAGE.format(city=city, mean_temp=mean_temp, max_temp=max_temp, min_temp=min_temp)




