from rest_framework import serializers

from content.models import Category, Content


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'createdAt']


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(required=True)
    categoryId = serializers.IntegerField(required=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'categoryId']
