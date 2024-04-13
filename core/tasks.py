from celery import shared_task
from .views import FetchMoviewsFromTmdbApiHandler


@shared_task
def fetch_movies_from_tmdb_and_save_to_database_task():
    movie_handler = FetchMoviewsFromTmdbApiHandler()
    movie_handler.fetch_movies_from_api()
    return "movies fetched successfully."
