import asyncio

from telethon import TelegramClient
from telethon.errors import UserIsBlockedError
from telethon.sessions import StringSession

from app.mailing.service import get_all_users, get_day_news
from config.settings import BOT_TOKEN, API_ID, API_HASH


class Mailing:
    def __init__(self):
        self.client = TelegramClient(StringSession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    async def start_mailing(self):
        users = await get_all_users()
        message = await get_day_news()
        await asyncio.gather(*[self.mailing(user.chat_id, message) for user in users])

    async def mailing(self, user_id, message):
        # todo need add field in db
        try:
            await self.client.send_message(user_id, message.text)
        except UserIsBlockedError:
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mailing().start_mailing())
