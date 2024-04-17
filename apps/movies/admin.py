from django.contrib import admin
from apps.movies.models import Movie


@admin.register(Movie)
class AdminMovie(admin.ModelAdmin):
    list_display = ('title', 'tag', 'release_date',
                    'rating', 'date_created', 'date_updated')
    readonly_fields = ('id',)
    list_per_page = 20
