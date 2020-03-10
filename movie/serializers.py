from rest_framework import serializers

from movie.models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'title']


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    genre = GenreSerializer(read_only=True)
    genreId = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'createdAt', 'genreId']


class MovieListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    genreId = serializers.PrimaryKeyRelatedField(source='genre', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'createdAt', 'genreId']
