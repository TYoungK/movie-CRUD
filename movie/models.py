from django.db import models
from datetime import datetime
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg')
    saved = models.BooleanField(default=False, blank=True)
    seen = models.BooleanField(default=False, blank=True)
    liked = models.BooleanField(default=None, blank=True, null=True)
    genre = models.CharField(max_length=200)
    running_time = models.IntegerField()
    director = models.CharField(max_length=200)
    casts = models.CharField(max_length=200)
    release_date = models.DateField(default=datetime.now, blank=True)

class Video(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)




