from django.urls import path
from .import views



urlpatterns = [
    path('favorites', views.FavoriteListView.as_view(), name="favorites"),
    path('remove-from-favorites/<str:id>', views.DeleteFavoriteView.as_view(), name="remove_from_favorites")
]
