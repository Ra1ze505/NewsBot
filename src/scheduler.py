import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.mailing.run import Mailing
from app.parser.run import Parser


def run_scheduler():
    scheduler = AsyncIOScheduler()
    parser_trigger = CronTrigger(hour='7', minute='30', second='0', timezone='Europe/Moscow')
    mailing_trigger = CronTrigger(hour='8', minute='0', second='0', timezone='Europe/Moscow')
    scheduler.add_job(Parser().parse_last_news, parser_trigger)
    scheduler.add_job(Mailing().start_mailing, mailing_trigger)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
