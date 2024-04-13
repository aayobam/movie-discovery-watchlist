from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.favorites.models import Favorite
from apps.movies.models import Movie


class AddToFavoriteView(LoginRequiredMixin, generic.CreateView):
    model = Favorite
    fields = '__all__'
    pk_url_kwarg = "id"

    def post(self, request, *args, **kwargs):
        movie_id = self.kwargs.get("movie_id")
        movie_obj = get_object_or_404(Movie, id=movie_id)
        if movie_obj is not None:
            instance: Favorite = self.model.objects.create(movie__id=movie_obj.id, user=request.user)
            instance.save()
            messages.success(request, "movie added to favorites.")
            return redirect("favorites")
        messages.error(request, "cannot add movie  as favorite.")
        return redirect("favorites")


class FavoriteListView(LoginRequiredMixin, generic.ListView):
    model = Favorite
    fields = "__all__"
    template_name = "favorites/favorite_list.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteWatchListView(LoginRequiredMixin, generic.DeleteView):
    model = Favorite
    fields = '__all__'
    context_object_name = "favorite"
    pk_url_kwarg = "id"

    def delete(self, request):
        instance = self.get_object()
        instance.delete()
        messages.success(request, "movie removed from favorite.")
        return redirect("favorites")