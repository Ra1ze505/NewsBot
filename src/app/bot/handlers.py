from telethon import events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from app.bot.service import user_create, change_city, START_MESSAGE, change_time_mailing, get_user_city, get_feedback, \
    get_username
from app.mailing.service import get_day_news, get_pretty_rate
from app.parser.service import WeatherService
from config.settings import BOT_TOKEN, API_ID, API_HASH, ADMIN_TG_ID
from app.bot.buttons import start_markup
from config import db


bot = TelegramClient(StringSession(), API_ID, API_HASH)


@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event: events.NewMessage.Event):
    await user_create(event.sender_id)
    await event.respond(START_MESSAGE, buttons=start_markup)
    print(db.async_connection_url())


@bot.on(events.NewMessage(pattern=r'Изменить\sгород$'))
async def change_city_handler(event: events.NewMessage.Event):
    async with bot.conversation(event.sender_id) as conv:
        await change_city(conv)


@bot.on(events.NewMessage(pattern=r'Изменить\sвремя\sрассылки$'))
async def change_time_mailing_handler(event: events.NewMessage.Event):
    async with bot.conversation(event.sender_id) as conv:
        await change_time_mailing(conv)


@bot.on(events.NewMessage(pattern=r'Погода$'))
async def weather_handler(event: events.NewMessage.Event):
    user_city = await get_user_city(event.sender_id)
    weather_message = await WeatherService().get_pretty_weather(user_city)
    await event.respond(weather_message, buttons=start_markup)


@bot.on(events.NewMessage(pattern=r'Курс$'))
async def rate_handler(event: events.NewMessage.Event):
    rate_message = await get_pretty_rate()
    await event.respond(rate_message, buttons=start_markup)


@bot.on(events.NewMessage(pattern=r'Новости$'))
async def help_handler(event: events.NewMessage.Event):
    news = await get_day_news()
    await event.respond(news.text, buttons=start_markup)


@bot.on(events.NewMessage(pattern=r'Написать\sнам$'))
async def write_us_handler(event: events.NewMessage.Event):
    async with bot.conversation(event.sender_id) as conv:
        feedback = await get_feedback(conv)
    username = await get_username(event)
    await bot.send_message(ADMIN_TG_ID, f'Новый отзыв от {username} : {feedback}')


@bot.on(events.NewMessage(pattern=r'О боте$'))
async def about_handler(event: events.NewMessage.Event):
    await event.respond(
        'Этот бот предназначен для получения новостей, погоды и курса валют.\n'
        'Код бота можно посмотреть [здесь](https://github.com/Ra1ze505/NewsBot)',
        buttons=start_markup
    )


# For run bot
if __name__ == '__main__':
    bot.start(bot_token=BOT_TOKEN)
    with bot:
        bot.run_until_disconnected()
