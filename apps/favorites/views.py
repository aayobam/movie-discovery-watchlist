from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.favorites.models import Favorite
from apps.movies.models import Movie



class FavoriteListView(LoginRequiredMixin, generic.ListView):
    model = Favorite
    fields = "__all__"
    template_name = "favorites/favorites.html"
    context_object_name = "favorites"
    paginate_by = 4

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteFavoriteView(LoginRequiredMixin, generic.DeleteView):
    model = Favorite
    context_object_name = "favorite"
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        title: str = instance.movie.title
        instance.delete()
        messages.success(request, f"{title.upper()} removed from favorite.")
        return redirect("favorites")
