from django.urls import path
from .import views


urlpatterns = [
    path('watchlist', views.WatchListView.as_view(), name="watchlist"),
    path('remove-from-watchlist/<str:id>', views.DeleteWatchListView.as_view(), name="remove_from_watchlist")
]
