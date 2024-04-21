from django_redis import get_redis_connection
import os
from celery import Celery

from .handler import populate_movie_database
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()


def tearDown(self):
    get_redis_connection("default").flushall()


@app.task()
def sample_task():
    return "sample task is running"


@app.task
def seed_movie_to_db_task():

    try:
        populate_movie_database()
    except Exception as e:
        print(f"{e}: Could not run task")
    return "task completed."


app.conf.beat_schedule = {
    'populate-movie-database-every-minute': {
        'task': 'core.celery.seed_movie_to_db_task',
        'schedule': crontab(),
    },
    'populate-movie-database-every-day-at-6am': {
        'task': 'core.celery.seed_movie_to_db_task',
        'schedule': crontab(hour=6, minute=0),
    }
}
