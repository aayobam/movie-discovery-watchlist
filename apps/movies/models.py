from django.db import models
from django.urls import reverse
from apps.common.base_model import BaseModel


class Movie(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=50, null=True, blank=True)
    poster_path = models.URLField(max_length=50, null=True, blank=True)
    rating = models.CharField(max_length=50, null=True, blank=True)
    overview = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("video_detail", kwargs={"id": self.id})
    
