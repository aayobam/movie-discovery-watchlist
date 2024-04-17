from core.celery import APP
from apps.common.handler import FetchMovieHandler


@APP.task
def seed_movie_to_db_task():
    handler = FetchMovieHandler()
    handler.populate_movie_database_task()
    return "task completed."
