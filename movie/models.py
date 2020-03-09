from django.db import models


class Genre(models.Model):
    id = models.IntegerField
    title = models.CharField(max_length=50)

    class Meta:
        db_table = 'genre'


class Movie(models.Model):
    id = models.BigIntegerField
    title = models.CharField(max_length=70)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False, db_column='created_at')

    class Meta:
        db_table = 'movie'
