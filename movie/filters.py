import django_filters

from movie.models import Genre, Movie


class MovieFilter(django_filters.FilterSet):
    genreId = django_filters.ModelChoiceFilter(
        field_name='genre__id', to_field_name='id', queryset=Genre.objects.all()
    )
    # genreTitle = django_filters.ModelChoiceFilter(
    #     field_name="genre__title",
    #     to_field_name='title',
    #     queryset=Genre.objects.all()
    # )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genreId']
