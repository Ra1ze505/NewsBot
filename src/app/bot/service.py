from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiohttp

from app.bot.buttons import cansel_markup, start_markup, change_time_markup, change_city_markup
from models import User, Feedback, get_async_session
from config.settings import WEATHER_API_NOW_URL, WEATHER_API_KEY

async_session = get_async_session()

START_MESSAGE = '''
**Привет!**
Я новостной бот, который будет отправлять вам каждое утро **новости**, **погоду** и **курс валют**!
По умолчанию я отправляю вам новости и погоду в Москве в 8 утра, но ты можешь изменить эти настройки.
Не переживайте за разницу во времени, все будет в порядке.
'''


async def commit(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()


async def user_create(chat_id: int) -> None:
    async with async_session() as session:
        user = User(chat_id=chat_id)
        session.add(user)
        await commit(session)


async def get_user_city(chat_id: int) -> str:
    async with async_session() as session:
        stmt = select([User.city]).where(User.chat_id == chat_id)
        user = await session.execute(stmt)
        return user.fetchone().city


async def get_time_mailing(chat_id: int) -> datetime.time:
    async with async_session() as session:
        stmt = select([User.time_mailing]).where(User.chat_id == chat_id)
        user = await session.execute(stmt)
        return user.fetchone().time_mailing


async def valid_city(city: str) -> (bool, int):
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_NOW_URL.format(city=city, token=WEATHER_API_KEY)) as resp:
            if resp.status == 200:
                data = await resp.json()
                return True, data['timezone'] / 3600
            return False, None


async def user_city_update(chat_id: int, city: str, timezone: int) -> None:
    async with async_session() as session:
        stmt = User.__table__.update().where(User.chat_id == chat_id).values(city=city, timezone=timezone)
        await session.execute(stmt)
        await commit(session)


async def user_time_mailing_update(chat_id: int, time_mailing: datetime.time) -> None:
    async with async_session() as session:
        stmt = User.__table__.update().where(User.chat_id == chat_id).values(time_mailing=time_mailing)
        await session.execute(stmt)
        await commit(session)


async def change_city(conv) -> None:
    city = await get_user_city(conv.chat_id)
    await conv.send_message(f'Ваш город сейчас: {city}\nНапишите свой город', buttons=change_city_markup)
    new_city, timezone, updated = await _get_city(conv, city)
    if updated:
        await user_city_update(conv.chat_id, new_city, timezone)
        await conv.send_message(f'Ваш город изменен на: {new_city}', buttons=start_markup)
    else:
        await conv.send_message('Ваш город не изменен', buttons=start_markup)


async def _get_city(conv, city: str = None) -> (str, int, bool):
    answer = await conv.get_response()
    if answer.text == 'Отмена':
        return city, None, False
    valid, timezone = await valid_city(answer.raw_text)
    if valid:
        return answer.raw_text, timezone, True
    else:
        await conv.send_message('Некорректный город\nПопробуйте еще раз')
        return await _get_city(conv)


async def change_time_mailing(conv) -> None:
    time_mailing: datetime.time = await get_time_mailing(conv.chat_id)
    await conv.send_message(f'Ваше время получения рассылки сейчас: {time_mailing.strftime("%H:%M")}\nОтправьте новое '
                            f'время получения рассылки\nP.S. вы можете указать любое время☺️',
                            buttons=change_time_markup)
    new_time_mailing, updated = await _get_time_mailing(conv, time_mailing)
    if updated:
        await user_time_mailing_update(conv.chat_id, new_time_mailing)
        await conv.send_message(f'Ваше время получения рассылки изменено на: {new_time_mailing.strftime("%H:%M")}.\n'
                                f'Время отправки изменится через час',
                                buttons=start_markup)
    else:
        await conv.send_message('Ваше время получения рассылки не изменено', buttons=start_markup)


async def _get_time_mailing(conv, time_mailing: str = None) -> (datetime.time, bool):
    answer = await conv.get_response()
    if answer.text == 'Отмена':
        return time_mailing, False
    try:
        new_time = datetime.strptime(answer.raw_text, '%H:%M').time()
        return new_time, True
    except ValueError:
        await conv.send_message('Некорректное время\nПопробуйте еще раз')
        return await _get_time_mailing(conv)


async def get_feedback(conv) -> str:
    await conv.send_message('Отправьте свой отзыв', buttons=cansel_markup)
    feedback = await _get_feedback(conv)
    if feedback is None:
        return await conv.send_message('Отзыв отменен', buttons=start_markup)
    await conv.send_message(f'Ваше сообщение: {feedback}')
    await conv.send_message('Отправляем...')
    await create_feedback(feedback, conv.chat_id)
    await conv.send_message('Спасибо за отзыв!', buttons=start_markup)
    return feedback


async def create_feedback(text: str, chat_id: int) -> None:
    async with async_session() as session:
        feedback = Feedback(text=text, user=chat_id)
        session.add(feedback)
        await commit(session)


async def _get_feedback(conv) -> Optional[str]:
    answer = await conv.get_response()
    if answer.text == 'Отмена':
        return None
    return answer.raw_text
