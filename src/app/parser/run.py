from telethon import TelegramClient

from app.parser.service import create_news
from config.settings import API_ID, API_HASH, NEWS_CHANEL, KEY_WORD


async def parse_last_news():
    chat = await parser.get_entity(NEWS_CHANEL)
    async for message in parser.iter_messages(chat, search=KEY_WORD):
        await create_news(message)
        break


if __name__ == '__main__':
    parser = TelegramClient('parser', API_ID, API_HASH)
    parser.start()
    parser.loop.run_until_complete(parse_last_news())