from django.urls import path
from .import views


urlpatterns = [
    path('movie-list', views.FetchMoviesView.as_view(), name="movie_list")
]
