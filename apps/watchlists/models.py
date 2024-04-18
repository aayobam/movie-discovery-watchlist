from django.db import models
from django.urls import reverse

from apps.common.base_model import BaseModel
from apps.movies.models import Movie
from apps.users.models import CustomUser


class WatchList(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watchlist', blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.movie.title

    def get_absolute_url(self):
        return reverse("watchlist_detail", kwargs={"id": self.id})
