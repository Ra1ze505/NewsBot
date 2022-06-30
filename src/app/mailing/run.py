import asyncio

from telethon import TelegramClient
from telethon.errors import UserIsBlockedError
from telethon.sessions import StringSession

from app.bot.buttons import start_markup
from app.mailing.service import get_all_users, get_day_news, get_user_by_chat_id, get_pretty_rate
from app.parser.service import WeatherService
from config.settings import BOT_TOKEN, API_ID, API_HASH


class Mailing:
    def __init__(self):
        self.client = TelegramClient(StringSession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    async def send_mailing(self, user_id: int):
        user = await get_user_by_chat_id(user_id)
        news_message = await get_day_news()
        rate_message = await get_pretty_rate()
        weather_message = await WeatherService().get_pretty_weather_for_day(user.city)
        await self.mailing(user.chat_id, [weather_message, rate_message, news_message.text])

    async def start_mailing(self):
        users = await get_all_users()
        news_message = await get_day_news()
        rate_message = await get_pretty_rate()

        await asyncio.gather(*[self.mailing(user.chat_id, [
            await WeatherService().get_pretty_weather_by_day(user.city),
            rate_message,
            news_message.text
        ]) for user in users])

    async def mailing(self, user_id: str, messages: list[str]):
        try:
            message = '\n'.join(messages)
            await self.client.send_message(user_id, message, buttons=start_markup)
        except UserIsBlockedError:
            pass


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(Mailing().start_mailing())
