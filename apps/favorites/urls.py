from django.urls import path
from .import views



urlpatterns = [
    path('add-to-favorite/<str:id>', views.AddToFavoriteView.as_view(), name="add_to_favorites"),
    path('favorites', views.FavoriteListView.as_view(), name="favorites"),
    path('remove-from-favorites/<str:id>', views.DeleteFavoriteView.as_view(), name="remove_from_favorites")
]
