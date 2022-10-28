from django.db import models
from django.conf import settings


class Photo(models.Model):
    title = models.CharField(max_length=100)
    album_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=100)  # validation for it
    url = models.URLField(max_length=200)
    image = models.ImageField(upload_to=settings.PHOTOS_DIR)
