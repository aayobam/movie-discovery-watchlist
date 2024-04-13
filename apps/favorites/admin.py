from django.contrib import admin
from apps.favorites.models import Favorite


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('user', 'movie', 'date_created', 'date_updated')
    readonly_fields = ('id', 'user', 'movie')
