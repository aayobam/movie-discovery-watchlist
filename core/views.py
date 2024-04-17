import random
import requests
from django.db.models import Q
from django.views import generic
from django.shortcuts import render
from apps.movies.models import Movie
from core.settings import API_BASE_URL, BEARER_TOKEN, MOVIE_BASE_URL


class FetchMoviewsFromTmdbApiView(generic.TemplateView):
    template_name = "movie_list.html"

    def get(self, request):
        query_list = ['now_playing', 'popular', 'top_rated', 'upcoming']
        movie_base_url = f"{API_BASE_URL}/movie/"
        movie_list_query = random.choice(query_list)
        url = f"{movie_base_url}{movie_list_query}"

        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "accept": "application/json"
        }

        response = requests.get(url=url, headers=headers)
        response_data = response.json().get("results", [])

        print(f"\n--------- RESULTS: {response_data} -----------\n")

        for data in response_data:
            movie_data = {
                "title": data["title"],
                "tag": movie_list_query,
                "overview": data["overview"],
                "poster_path": f"{MOVIE_BASE_URL}/w200{data['poster_path']}",
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
        context = {"response": response.text}
        return render(request, self.template_name, context)


class MovieListView(generic.ListView):
    model = Movie
    fields = '__all__'
    template_name = "index.html"
    context_object_name = 'movies'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_tag_query = self.request.GET.get("tag")
        movie_title_query = self.request.GET.get("title")

        if movie_title_query:
            qs = queryset.filter(title__iexact=movie_title_query)
            return qs

        if movie_tag_query:
            qs = queryset.filter(tag__iexact=movie_tag_query)
            return qs

        if movie_title_query and movie_tag_query:
            chained_qs = Q(title__iexact=movie_title_query) & Q(
                tag__iexact=movie_tag_query)
            qs = queryset.filter(chained_qs)
            return qs

        return queryset
