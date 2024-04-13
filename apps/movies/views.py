from django.views import generic
from apps.movies.models import Movie


class MovieDetailView(generic.DetailView):
    model = Movie
    fields = "__all__"
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"
    pk_url_kwarg = "id"
