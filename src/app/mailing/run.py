import asyncio

from telethon import TelegramClient
from telethon.errors import UserIsBlockedError
from telethon.sessions import StringSession

from app.mailing.service import get_all_users, get_day_news
from app.parser.service import Weather
from config.settings import BOT_TOKEN, API_ID, API_HASH


class Mailing:
    def __init__(self):
        self.client = TelegramClient(StringSession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    async def start_mailing(self):
        users = await get_all_users()
        news_message = await get_day_news()

        await asyncio.gather(*[self.mailing(user.chat_id, [
            await Weather().get_pretty_weather(user.city),
            news_message.text
        ]) for user in users])

    async def mailing(self, user_id: str, messages: list[str]):
        # todo need add field in db
        try:
            for message in messages:
                await self.client.send_message(user_id, message)
        except UserIsBlockedError:
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mailing().start_mailing())
