from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import generic
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.favorites.models import Favorite
from apps.movies.models import Movie
from django.shortcuts import get_object_or_404, redirect
from apps.watchlists.models import WatchList


class MovieDetailView(generic.DetailView):
    model = Movie
    fields = "__all__"
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        if 'add_to_watchlist' in request.POST:
            return self.add_to_watchlist(request)
        elif 'add_to_favorite' in request.POST:
            return self.add_to_favorites(request)
        else:
            return super().get(request)

    @transaction.atomic
    @method_decorator(login_required(login_url='user_login'))
    def add_to_watchlist(self, request, *args, **kwargs):
        if request.method == "POST":
            movie_id = request.POST.get("movie_id")
            movie_obj = get_object_or_404(Movie, id=movie_id)
            if movie_obj is not None:
                watchlist_qs = WatchList.objects.filter(user=self.request.user, movie=movie_obj)
                if watchlist_qs.exists():
                    messages.info(request, f"{movie_obj.title.upper()} already exists in your watchlist.")
                    return redirect("movie_detail", movie_obj.id)
                WatchList.objects.create(user=request.user, movie=movie_obj)
                messages.success(request, f"{movie_obj.title.upper()} added to watchlist.")
                return redirect("movie_detail", movie_obj.id)
            messages.error(request, "movie not found.")
            return redirect("movie_detail", movie_obj.id)

    @transaction.atomic
    @method_decorator(login_required(login_url='user_login'))
    def add_to_favorites(self, request, *args, **kwargs):
        if request.method == "POST":
            movie_id = request.POST.get("movie_id")
            movie_obj = get_object_or_404(Movie, id=movie_id)
            if movie_obj is not None:
                favorites_qs = Favorite.objects.filter(user=self.request.user, movie=movie_obj)
                if favorites_qs.exists():
                    messages.info(request, f"{movie_obj.title.upper()} already exists in your favorites.")
                    return redirect("movie_detail", movie_obj.id)
                Favorite.objects.create(user=request.user, movie=movie_obj)
                messages.success(request, f"{movie_obj.title.upper()} added to favorites.")
                return redirect("movie_detail", movie_obj)
            messages.error(request, "movie not found.")
            return redirect("movie_detail", movie_obj.id)
