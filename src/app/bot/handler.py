from telethon import events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from app.bot.service import user_create, change_city, START_MESSAGE, change_time_mailing
from app.parser.service import get_weather, get_pretty_rate
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
            await event.respond(START_MESSAGE, buttons=start_markup)
        case 'Изменить город':
            async with bot.conversation(event.sender_id) as conv:
                await change_city(conv)
        case 'Изменить время рассылки':
            async with bot.conversation(event.sender_id) as conv:
                await change_time_mailing(conv)
        case 'Погода':
            weather_message = await get_weather(event.sender_id)
            await event.respond(weather_message)
        case 'Курс':
            rate_message = await get_pretty_rate()
            await event.respond(rate_message)


# For run bot
# with bot:
#     bot.run_until_disconnected()
