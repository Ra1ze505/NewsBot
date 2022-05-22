import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mailing.run import Mailing
from parser.run import Parser

if __name__ == '__main__':
    mailing_trigger = CronTrigger(hour='8', minute='0', second='0', timezone='Europe/Moscow')
    parser_trigger = CronTrigger(hour='7', minute='30', second='0', timezone='Europe/Moscow')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(Mailing().start_mailing, mailing_trigger)
    scheduler.add_job(Parser().parse_last_news, parser_trigger)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
