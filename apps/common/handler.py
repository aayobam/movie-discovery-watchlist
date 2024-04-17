import requests
import random
import requests
from core.settings import API_BASE_URL, BEARER_TOKEN, MOVIE_BASE_URL
from apps.movies.models import Movie


class FetchMovieHandler:
    @staticmethod
    def populate_movie_database_task():
        query_list = ['now_playing', 'popular', 'top_rated', 'upcoming']
        api_base_url = f"{API_BASE_URL}movie/"
        movie_list_query = random.choice(query_list)
        url = f"{api_base_url}{movie_list_query}"

        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
        except requests.ConnectionError as e:
            raise Exception("failed operation", e)

        if response.status_code in ['200', '201']:

            response_data = response.json().get("results", [])

            for data in response_data:
                movie_data = {
                    "title": data["title"],
                    "tag": movie_list_query,
                    "overview": data["overview"],
                    "poster_path": f"{MOVIE_BASE_URL}w200{data['poster_path']}",
                    "release_date": data["release_date"],
                    "rating": data["vote_average"]
                }
                instance, created = Movie.objects.get_or_create(**movie_data)
                if not created:
                    instance.title = movie_data["title"]
                    instance.overview = movie_data["overview"]
                    instance.poster_path = movie_data["poster_path"]
                    instance.release_date = movie_data["release_date"]
                    instance.rating = movie_data["rating"]
                    instance.tag = movie_data["tag"]
                    instance.save()
                    return "movies fetched successfully."
