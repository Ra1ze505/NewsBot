import json

import aiohttp
from telethon import TelegramClient
from telethon.sessions import StringSession

from app.parser.service import create_news, create_rate, get_all_cities, WeatherService, create_weather
from config.settings import API_ID, API_HASH, NEWS_CHANEL, KEY_WORD, STRING_SESSION, CURRENCY_API_URL


class Parser:
    def __init__(self):
        self.client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

    async def parse_all(self):
        await self.parse_last_news()
        await self.parse_rate()
        await self.parse_weather()

    async def parse_last_news(self):
        chat = await self.client.get_entity(NEWS_CHANEL)
        async for message in self.client.iter_messages(chat, search=KEY_WORD):
            await create_news(message)
            break

    async def parse_rate(self):
        data = await self._get_parsed_rate()
        await create_rate(data['Valute'])

    async def parse_weather(self):
        cities = await get_all_cities()
        weathers_by_cities = await WeatherService().parse_weather_by_cities(cities)
        await create_weather(weathers_by_cities)

    async def _get_parsed_rate(self):
        async with aiohttp.ClientSession() as session:
            url = CURRENCY_API_URL
            async with session.get(url) as resp:
                data = await resp.read()
                data_json = json.loads(data)
                return data_json


if __name__ == '__main__':
    p = Parser()
    p.client.loop.run_until_complete(p.parse_all())