from tests.setup_db import fake_db

from app.bot.handlers import start_handler
import pytest


class EventMock:
    def __init__(self):
        self.history = []
        self.sender_id = 247719236

    async def respond(self, text, *args, **kwargs):
        self.history.append(text)


@pytest.mark.asyncio
async def test_handler(fake_db):
    event = EventMock()
    await start_handler(event)
    # print(async_connection_url, 'test')
    assert len(event.history) == 1


# def test_db_connection():
#     db_prep(connection_url)
#     engine = create_engine(db.connection_url)
#     conn = engine.connect()
#     conn.execute("select 1")
#     conn.close()
