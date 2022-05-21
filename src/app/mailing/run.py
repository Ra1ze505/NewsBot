import asyncio

from telethon import TelegramClient

from app.mailing.service import get_all_users, get_day_news
from config.settings import BOT_TOKEN, API_ID, API_HASH


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


async def mailing(user_id, message):
    await bot.send_message(user_id, message.text)


async def start_mailing():
    users = await get_all_users()
    message = await get_day_news()
    await asyncio.gather(*[mailing(user.chat_id, message) for user in users])


if __name__ == '__main__':
    bot.loop.run_until_complete(start_mailing())