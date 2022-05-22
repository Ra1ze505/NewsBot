from telethon import TelegramClient

from parser.service import create_news
from config.settings import API_ID, API_HASH, NEWS_CHANEL, KEY_WORD


class Parser:
    def __init__(self):
        self.client = TelegramClient('parser', API_ID, API_HASH).start()

    async def parse_last_news(self):
        chat = await self.client.get_entity(NEWS_CHANEL)
        async for message in self.client.iter_messages(chat, search=KEY_WORD):
            await create_news(message)
            break

if __name__ == '__main__':
    p = Parser()
    p.client.loop.run_until_complete(p.parse_last_news())