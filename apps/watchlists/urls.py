from django.urls import path
from .import views


urlpatterns = [
    path("add-to-watchlist", views.AddToWatchListView.as_view(), name="add_to_watchlist"),
    path('watchlist', views.WatchListView.as_view(), name="watchlist"),
    path('remove-from-watchlist/<str:id>', views.DeleteWatchListView.as_view(), name="remove_from_watchlist")
]
