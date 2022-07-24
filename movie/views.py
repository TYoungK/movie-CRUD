from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import exceptions
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
import asyncio
from asgiref.sync import sync_to_async

class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #http_method_names = ['get', 'post', 'put']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.count() == 0:
            raise exceptions.NotFound

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            Movie.objects.get(title=request.data['title'], director=request.data['director'],
                              casts=request.data['casts'], release_date=request.data['release_date'])
        except:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        exc = exceptions.APIException(detail="동일한 영화 정보가 존재합니다.")
        exc.status_code = status.HTTP_409_CONFLICT
        raise exc

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = Movie.objects.get(id=kwargs['pk'])
        except:
            raise exceptions.NotAcceptable(detail="리소스가 존재하지 않습니다.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        sync_to_async(self.perform_update(serializer))
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        if 'delete' not in self.http_method_names:
            raise exceptions.MethodNotAllowed
        movie = self.get_object()
        sync_to_async(self.perform_destroy(movie))
        return Response(status=status.HTTP_202_ACCEPTED)


class VideoView(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def list(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        videos = movie.video_set.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    def create(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.movie.id != kwargs['movie_id']:
            raise exceptions.NotFound(detail="해당 리소스의 상위 리소스가 일치하지 않습니다.")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.movie.id != kwargs['movie_id']:
            raise exceptions.NotFound(detail="해당 리소스의 상위 리소스가 일치하지 않습니다.")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.movie.id != kwargs['movie_id']:
            raise exceptions.NotFound(detail="해당 리소스의 상위 리소스가 일치하지 않습니다.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
