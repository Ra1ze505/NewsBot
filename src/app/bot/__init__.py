from telethon import events
from telethon.sync import TelegramClient

from app.bot.service import user_create
from config.settings import BOT_TOKEN, API_ID, API_HASH

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage)
async def handler(event):
    match event.raw_text:
        case '/start':
            await user_create(event.sender_id)
            await event.respond('Hello!')
        case _:
            await event.respond('I don\'t understand you!')


if __name__ == '__main__':
    # bot = bot.start(bot_token=BOT_TOKEN)
    with bot:
        bot.run_until_disconnected()
