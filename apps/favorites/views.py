from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.favorites.models import Favorite
from apps.movies.models import Movie


class AddToFavoriteView(LoginRequiredMixin, generic.CreateView):
    model = Favorite

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        movie_id = request.GET.get("movie_id")
        movie_obj = get_object_or_404(Movie, id=movie_id)
        if movie_obj is not None:
            movie_data = {"user": request.user, "movie_id": movie_obj.id}
            instance = self.model.objects.all()
            if instance.filter(movie__title=movie_obj.title).exists():
                messages.info(request, f"{movie_obj.title.upper()} already exist in your favorites.")
                return redirect("home")
            instance.create(**movie_data)
            messages.success(request, f"{movie_obj.title.upper()} added to favorites.")
            return redirect("home")
        messages.error(request, "cannot add movie to favorites.")
        return redirect("home")


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
