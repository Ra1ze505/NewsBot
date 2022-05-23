# import asyncio
#
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.cron import CronTrigger
import threading

from app.mailing.run import Mailing
# from app.parser.run import Parser
#
#
# def run_scheduler():
#     scheduler = AsyncIOScheduler()
#     parser_trigger = CronTrigger(hour='7', minute='30', second='0', timezone='Europe/Moscow')
#     mailing_trigger = CronTrigger(hour='8', minute='0', second='0', timezone='Europe/Moscow')
#     scheduler.add_job(Parser().parse_last_news, parser_trigger)
#     scheduler.add_job(Mailing().start_mailing, mailing_trigger)
#     scheduler.start()
#
#     try:
#         asyncio.get_event_loop().run_forever()
#     except (KeyboardInterrupt, SystemExit):
#         pass
import asyncio
from celery import Celery

# import celery_pool_asyncio  # noqa
# Sometimes noqa does not disable linter (Spyder IDE)cd ..
# celery_pool_asyncio.__package__

BROKER_URL = 'redis://localhost:6379/0'

app = Celery('tasks', broker=BROKER_URL)

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
}


async def async_task():
    await Mailing().start_mailing()


@app.task
def mailing():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mailing().start_mailing())


@app.task
def regular_task():
    print('Regular task')
    add_task()
    print(app.conf.beat_schedule)
    # app.task(Mailing().start_mailing)


regular_task.delay()


def add_task():
    app.conf.beat_schedule['example'] = {
        'task': 'tasks.mailing',
        'schedule': 10.0,
        'args': ()
    }