from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.movies.models import Movie
from apps.watchlists.models import WatchList


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
