from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.movies.models import Movie
from apps.watchlists.models import WatchList


class AddToWatchListView(LoginRequiredMixin, generic.CreateView):
    model = WatchList
    fields = '__all__'
    context_object_name = "watchlist"
    pk_url_kwarg = "id"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        movie_id = request.POST.get("movie_id")
        movie_obj = get_object_or_404(Movie, id=movie_id)
        if movie_obj is not None:
            movie_data = {
                "user": request.user,
                "movie_id": movie_obj.id
            }
            instance = self.model.objects.all()
            if instance.filter(movie__title=movie_obj.title).exists():
                messages.info(
                    request, f"{movie_obj.title.upper()} already exist in your watchlist.")
                return redirect("home")
            instance.create(**movie_data)
            messages.success(
                request, f"{movie_obj.title.upper()} added to watchlist.")
            return redirect("home")
        messages.error(request, "cannot add movie  to watchlist.")
        return redirect("home")


class WatchListView(LoginRequiredMixin, generic.ListView):
    model = WatchList
    fields = '__all__'
    template_name = "watchlists/watch_list.html"
    context_object_name = "watchlists"
    paginate_by = 4

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteWatchListView(LoginRequiredMixin, generic.DeleteView):
    model = WatchList
    context_object_name = "watchlist"
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        title: str = instance.movie.title
        instance.delete()
        messages.success(request, f"{title.upper()} removed from watchlist.")
        return redirect("watchlist")
