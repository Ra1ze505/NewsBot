import asyncio
from datetime import datetime, timedelta, date
from celery import Celery

from app.mailing.run import Mailing
from app.parser.run import Parser
from config.settings import CELERY_BROKER_URL
from tasks.service import get_users


app = Celery('tasks', broker=CELERY_BROKER_URL)

app.conf.beat_schedule = {
    'parse-news-every-day': {
        'task': 'tasks.schedule.parse_all',
        'schedule': timedelta(minutes=30),
    },
    'add-mailing-tasks-every-30-minute': {
        'task': 'tasks.schedule.create_hour_task',
        'schedule': timedelta(minutes=30),
    },
}


@app.task
def parse_all():
    parser = Parser()
    parser.client.loop.run_until_complete(Parser().parse_all())


@app.task
def run_mailing(chat_id):
    mailing = Mailing()
    mailing.client.loop.run_until_complete(Mailing().send_mailing(chat_id))


@app.task
def create_hour_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_hour_task())


async def get_hour_task():
    users = await get_users()
    for user in users:
        datetime_mailing = datetime.combine(date.today(), user.time_mailing) - timedelta(hours=user.timezone)
        if timedelta(minutes=30) < datetime_mailing - datetime.utcnow() < timedelta(hours=1):
            delta = datetime_mailing - datetime.utcnow()
            run_mailing.apply_async(args=(user.chat_id,), countdown=delta.seconds)
