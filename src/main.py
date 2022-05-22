import optparse

bot = optparse.OptionParser(version='1.0', description='A simple bot for get news from the internet')
bot.add_option('-m', '--mode', type='string', default='bot', help='Choose mode: bot or scheduler')

(options, args) = bot.parse_args()

if options.mode == 'bot':
    from app.bot.handler import bot
    with bot:
        bot.run_until_disconnected()
elif options.mode == 'scheduler':
    from scheduler import run_scheduler
    run_scheduler()