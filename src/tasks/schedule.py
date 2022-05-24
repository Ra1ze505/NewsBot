import asyncio
from datetime import datetime, timedelta, date
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready

from app.mailing.run import Mailing
from tasks.service import get_users

app = Celery('tasks', broker='redis://redis:6379/0')


app.conf.beat_schedule = {
    'add-mailing-tasks-every-day': {
        'task': 'tasks.schedule.create_day_task',
        'schedule': crontab(hour=0),
    },
}


@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    sender.app.send_task('tasks.schedule.create_day_task')


@app.task
def run_mailing(chat_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mailing().send_mailing(chat_id))


@app.task
def create_day_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_day_task())


async def get_day_task():
    users = await get_users()
    for user in users:
        datetime_mailing = datetime.combine(date.today(), user.time_mailing) - timedelta(hours=user.timezone)
        if datetime_mailing > datetime.utcnow():
            delta = datetime_mailing - datetime.utcnow()
            run_mailing.apply_async(args=(user.chat_id,), countdown=delta.seconds)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_day_task())
