from django.urls import path, include
from .views import *
from movie.views import MovieView
from rest_framework import routers

app_name = 'movie'

movie_router = routers.DefaultRouter()
movie_router.register(r'movies', MovieView)

video_router = routers.DefaultRouter()
video_router.register(r'videos', VideoView)

urlpatterns = [
    path('', include(movie_router.urls)),
    path('movies/<int:movie_id>/', include(video_router.urls)),
]
