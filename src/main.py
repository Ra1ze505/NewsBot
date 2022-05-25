from app.bot.handlers import bot


with bot:
    bot.run_until_disconnected()