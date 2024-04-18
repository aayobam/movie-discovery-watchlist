from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.MovieListView.as_view(), name="home"),
    path("fetch-movies", views.FetchMoviewsFromTmdbApiView.as_view(), name="fetch_movies"),
    path('movies/', include("apps.movies.urls")),
    path("filtered-movies-result/", views.MovieFilterResultView.as_view(), name="filtered_movie_result"),
    path('users/', include("apps.users.urls")),
    path("watchlist/", include("apps.watchlists.urls")),
    path("favorites/", include("apps.favorites.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
