from django.urls import path
from .import views


urlpatterns = [
    path('movie-detail<str:id>', views.MovieDetailView.as_view(), name="movie_detail")
]
