from telethon import events
from telethon.sync import TelegramClient

from config.settings import BOT_TOKEN, API_ID, API_HASH

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage)
async def handler(event):
    match event.raw_text:
        case '/start':
            await event.respond('Hello!')
        case _:
            await event.respond('I don\'t understand you!')

with bot:
    bot.run_until_disconnected()
