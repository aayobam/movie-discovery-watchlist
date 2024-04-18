import random
from django.db.models.query import QuerySet
import requests
from django.db.models import Q
from django.views import generic
from django.shortcuts import render
from apps.common.choices import TAGS
from apps.movies.models import Movie
from core.settings import API_BASE_URL, BEARER_TOKEN, MOVIE_BASE_URL


class FetchMoviewsFromTmdbApiView(generic.TemplateView):
    template_name = "api_response.html"

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
        for data in response_data:
            movie_data = {
                "title": data["title"],
                "tag": movie_list_query,
                "overview": data["overview"],
                "poster_path": f"{MOVIE_BASE_URL}/w200{data['poster_path']}",
                "release_date": data["release_date"],
                "rating": data["vote_average"]
            }
            instance = Movie.objects.filter(
                title=movie_data.get("title")).first()
            if instance:
                self.patch_existing_movie(instance, movie_data)
            Movie.objects.get_or_create(**movie_data)
        context = {"response": response.text}
        return render(request, self.template_name, context)

    def patch_existing_movie(self, instance, movie_data):
        for key, value in movie_data.items():
            setattr(instance, key, value)
        instance.save()


class MovieListView(generic.ListView):
    model = Movie
    fields = '__all__'
    template_name = "index.html"
    context_object_name = 'movies'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_tag_query = self.request.GET.get("tags", "")
        movie_title_query = self.request.GET.get("title")

        if movie_title_query:
            qs = queryset.filter(title__iexact=movie_title_query)
            return qs

        if movie_tag_query:
            qs = queryset.filter(tag__iexact=movie_tag_query)
            return qs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie_slides"] = self.model.objects.all()[:5]
        context["TAGS"] = TAGS
        return context


class MovieFilterResultView(generic.ListView):
    model = Movie
    fields = "__all__"
    context_object_name = "movies"
    template_name = "partial/movie_result.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_tag_query = self.request.GET.get("tags", "")
        if movie_tag_query:
            qs = queryset.filter(tag__iexact=movie_tag_query)
            return qs
        return queryset
