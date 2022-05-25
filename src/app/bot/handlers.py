from telethon import events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from app.bot.service import user_create, change_city, START_MESSAGE, change_time_mailing
from app.parser.service import get_weather, get_pretty_rate
from config.settings import BOT_TOKEN, API_ID, API_HASH
from app.bot.buttons import start_markup

bot = TelegramClient(StringSession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await user_create(event.sender_id)
    await event.respond(START_MESSAGE, buttons=start_markup)


@bot.on(events.NewMessage(pattern='Изменить город'))
async def change_city_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        await change_city(conv)


@bot.on(events.NewMessage(pattern='Изменить время рассылки'))
async def change_time_mailing_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        await change_time_mailing(conv)


@bot.on(events.NewMessage(pattern='Погода'))
async def weather_handler(event):
    weather_message = await get_weather(event.sender_id)
    await event.respond(weather_message, buttons=start_markup)


@bot.on(events.NewMessage(pattern='Курс'))
async def rate_handler(event):
    rate_message = await get_pretty_rate()
    await event.respond(rate_message, buttons=start_markup)


# For run bot
# with bot:
#     bot.run_until_disconnected()
