from app.bot.handlers import bot
from config.settings import BOT_TOKEN


bot.start(bot_token=BOT_TOKEN)
with bot:
    bot.run_until_disconnected()
