from rest_framework import serializers
from .models import Movie, Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ('movie',)


class MovieSerializer(serializers.ModelSerializer):
    video_set = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'