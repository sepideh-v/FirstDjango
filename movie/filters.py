import django_filters

from movie.models import Genre, Movie


class MovieFilter(django_filters.FilterSet):
    genreId = django_filters.ModelChoiceFilter(
        field_name='genre__id', to_field_name='genreId', queryset=Genre.objects.all()
    )
    # genreTitle = django_filters.ModelChoiceFilter(
    #     name="genre__title",
    #     queryset=Genre.objects.all()
    # )

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genreId')
