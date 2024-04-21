import requests
import random
import requests
from core.settings import API_BASE_URL, BEARER_TOKEN, MOVIE_BASE_URL


def populate_movie_database():
    from apps.movies.models import Movie
    query_list = ['now_playing', 'popular', 'top_rated', 'upcoming']
    movie_base_url = f"{API_BASE_URL}/movie/"
    movie_list_query = random.choice(query_list)
    url = f"{movie_base_url}{movie_list_query}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "accept": "application/json"}
    response = requests.get(url=url, headers=headers)
    response_data = response.json().get("results", [])
    for data in response_data:
        movie_data = {
            "title": data["title"],
            "tag": movie_list_query,
            "overview": data["overview"],
            "poster_path": f"{MOVIE_BASE_URL}/w200{data['poster_path']}",
            "release_date": data["release_date"],
            "rating": data["vote_average"]
        }
        instance = Movie.objects.filter(title=movie_data.get("title")).first()
        if instance:
            patch_existing_movie(instance, movie_data)
        Movie.objects.get_or_create(**movie_data)

def patch_existing_movie(instance, movie_data):
    for key, value in movie_data.items():
        setattr(instance, key, value)
    instance.save()
