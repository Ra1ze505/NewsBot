from app.bot.handler import bot


with bot:
    bot.run_until_disconnected()