from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.movies.models import Movie
from apps.watchlists.models import WatchList


class AddToWatchListView(LoginRequiredMixin, generic.CreateView):
    model = WatchList
    fields = '__all__'
    context_object_name = "watchlist"
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        movie_id = self.kwargs.get("movie_id")
        movie_obj = get_object_or_404(Movie, id=movie_id)
        if movie_obj is not None:
            instance: WatchList = self.model.objects.create(
                movie__id=movie_obj.id, user=request.user)
            instance.save()
            messages.success(request, "movie added to watchlist.")
            return redirect("watchlists")
        messages.error(request, "cannot add movie  to watchlist.")
        return redirect("watchlists")


class WatchListView(LoginRequiredMixin, generic.ListView):
    model = WatchList
    fields = '__all__'
    template_name = "watchlists/watchlist_list.html"
    context_object_name = "watchlists"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteWatchListView(LoginRequiredMixin, generic.DeleteView):
    model = WatchList
    fields = '__all__'
    context_object_name = "watchlist"
    pk_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        messages.success(request, "movie removed from watchlist.")
        return redirect("watchlists")
