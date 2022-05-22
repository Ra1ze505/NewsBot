from telethon import events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from app.bot.service import user_create, change_city
from config.settings import BOT_TOKEN, API_ID, API_HASH
from app.bot.buttons import start_markup

bot = TelegramClient(StringSession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage)
async def handler(event):
    if event.message.sender.bot:
        return

    match event.raw_text:
        case '/start':
            await user_create(event.sender_id)
            await event.respond('Hello!', buttons=start_markup)
        case 'Изменить мой регион':
            async with bot.conversation(event.sender_id) as conv:
                await change_city(conv)


# For run bot
# with bot:
#     bot.run_until_disconnected()
