import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
