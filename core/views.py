from apps.favorites.models import Favorite
from django.shortcuts import render, redirect, get_object_or_404
import random
import requests
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.contrib import messages
from apps.movies.models import Movie
from apps.common.choices import TAGS
from apps.watchlists.models import WatchList
from core.settings import API_BASE_URL, BEARER_TOKEN, MOVIE_BASE_URL
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
            instance = Movie.objects.filter(title=movie_data.get("title")).first()
            if instance:
                self.patch_existing_movie(instance, movie_data)
            Movie.objects.get_or_create(**movie_data)
        context = {"response": response.text}
        return render(request, self.template_name, context)

    def patch_existing_movie(self, instance, movie_data):
        for key, value in movie_data.items():
            setattr(instance, key, value)
        instance.save()


class HomeView(generic.ListView):
    model = Movie
    fields = "__all__"
    template_name = "index.html"
    context_object_name = 'movies'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_title_query = self.request.GET.get("title")
        movie_tag_query = self.request.GET.get("tags")

        if movie_title_query:
            queryset = queryset.filter(title__icontains=movie_title_query)

        if movie_tag_query:
            queryset = queryset.filter(tag__iexact=movie_tag_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie_slides"] = Movie.objects.all()[:5]
        context["TAGS"] = TAGS
        context["user"] = self.request.user
        return context

    def post(self, request):
        if 'add_to_watchlist' in request.POST:
            return self.add_to_watchlist(request)
        elif 'add_to_favorites' in request.POST:
            return self.add_to_favorites(request)
        else:
            return super().get(request)

    @transaction.atomic
    @method_decorator(login_required(login_url='user_login'))
    def add_to_watchlist(self, request):
        if request.method == "POST":
            movie_id = request.POST.get("movie_id")
            movie_obj = get_object_or_404(Movie, id=movie_id)
            watchlist_qs = WatchList.objects.filter(user=self.request.user, movie=movie_obj)
            if watchlist_qs.exists():
                messages.info(request, f"{movie_obj.title.upper()} already exists in your watchlist.")
                return redirect("home")
            WatchList.objects.create(user=request.user, movie=movie_obj)
            messages.success(request, f"{movie_obj.title.upper()} added to watchlist.")
            return redirect("home")

    @transaction.atomic
    @method_decorator(login_required(login_url='user_login'))
    def add_to_favorites(self, request):
        if request.method == "POST":
            movie_id = request.POST.get("movie_id")
            movie_obj = get_object_or_404(Movie, id=movie_id)
            favorites_qs = Favorite.objects.filter(user=self.request.user, movie=movie_obj)
            if favorites_qs.exists():
                messages.info(request, f"{movie_obj.title.upper()} already exists in your favorites.")
                return redirect("home")
            Favorite.objects.create(user=request.user, movie=movie_obj)
            messages.success(request, f"{movie_obj.title.upper()} added to favorites.")
            return redirect("home")


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
