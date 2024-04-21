from celery import shared_task
from core.handler import populate_movie_database
from ..core.celery import app


@shared_task
def seed_movie_to_db_task():
    try:
        populate_movie_database()
    except Exception as e:
        print(f"{e}: Could not run task")
    return "task completed."


# @app.task()
# def seed_movie_to_db_task():
#     populate_movie_database()
#     return "task completed."
