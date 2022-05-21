import asyncio

from app.bot.service import get_all_users, get_day_news
from app.bot import bot
from config.settings import BOT_TOKEN


async def mailing(user_id, message):
    print(f'Mailing to {user_id}')
    # chat = await parser.get_entity('@redakciya_channel')
    # msg = await parser.get_messages(chat, limit=1)
    # msg = msg[0]
    print(msg)
    # await bot.send_message(user_id, msg)
    # await bot.forward_messages(user_id, chat, msg)
    await bot.send_message(user_id, msg.message)
    # await bot.forward_messages(), user_id)


async def start_mailing():
    users = await get_all_users()
    message = await get_day_news()
    await asyncio.gather(*[mailing(user.chat_id, message) for user in users])


if __name__ == '__main__':
    bot.start(bot_token=BOT_TOKEN)
    bot.loop.run_until_complete(start_mailing())