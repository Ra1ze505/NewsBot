import asyncio
from celery import Celery
from celery.signals import worker_ready
import datetime

from app.mailing.run import Mailing
from tasks.service import get_users

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def run_mailing(chat_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mailing().send_mailing(chat_id))


# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.schedule.create_day_task',
#         'schedule': 5.0,
#     },
# }


# @app.task
# def hello(*args):
#     # app.conf.beat_schedule['test'] = {
#     #     'task': 'tasks.run_parser',
#     #     'schedule': 5.0,
#     # }
#     run_parser.apply_async(countdown=5)

@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        sender.app.send_task('tasks.schedule.create_day_task', connection=conn)


@app.task
def create_day_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_day_task())


async def get_day_task():
    users = await get_users()
    for user in users:
        datetime_mailing = datetime.datetime.combine(datetime.date.today(), user.time_mailing) - datetime.timedelta(hours=user.timezone)
        if datetime_mailing > datetime.datetime.utcnow():
            delta = datetime_mailing - datetime.datetime.utcnow()
            run_mailing.apply_async(args=(user.chat_id,), countdown=delta.seconds)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_day_task())
