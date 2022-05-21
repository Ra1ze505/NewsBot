import asyncio

from telethon import TelegramClient

from app.mailing.service import get_all_users, get_day_news
from config.settings import BOT_TOKEN, API_ID, API_HASH


class Mailing:
    def __init__(self):
        self.client = TelegramClient('mailing', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    async def start_mailing(self):
        users = await get_all_users()
        message = await get_day_news()
        await asyncio.gather(*[self.mailing(user.chat_id, message) for user in users])

    async def mailing(self, user_id, message):
        await self.client.send_message(user_id, message.text)


if __name__ == '__main__':
    asyncio.run(Mailing().start_mailing())
