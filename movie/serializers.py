from rest_framework import serializers

from movie.models import Genre, Movie


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(required=True)
    genreId = serializers.IntegerField(required=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genreId', 'createdAt']
