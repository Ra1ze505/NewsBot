from types import MethodType

import pytest
from sqlalchemy import select

from app.bot.handlers import start_handler, change_city_handler
from app.bot import handlers
from models import User


@pytest.mark.asyncio
async def test_handler(fake_async_connect, fake_event):
    await start_handler(fake_event)
    assert len(fake_event.history) == 1  # got received message

    async with fake_async_connect() as session:
        stmt = select([User]).where(User.chat_id == fake_event.sender_id)
        _user = await session.execute(stmt)
        user = _user.fetchone()

    assert user is not None  # user created


@pytest.mark.asyncio
async def test_handler_change_city(fake_async_connect, fake_event, fake_conversation):
    handlers.bot.conversation = MethodType(fake_conversation, handlers.bot)

    await change_city_handler(fake_event)
    print('End')
