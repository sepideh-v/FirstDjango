from django.db import models


class Category(models.Model):
    id = models.IntegerField
    title = models.CharField(max_length=40)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False, db_column='create_at')

    class Meta:
        db_table = 'category'


class Content(models.Model):
    id = models.BigIntegerField
    title = models.CharField(max_length=50)
    categoryId = models.IntegerField(db_column='category_id')

    class Meta:
        db_table = 'content'
