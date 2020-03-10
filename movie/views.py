from django.db import connection
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from movie.filters import MovieFilter
from movie.models import Genre, Movie
from movie.serializers import GenreSerializer, MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):

    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Genre.objects.all()

    def list(self, request, *args, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        serializer = GenreSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        genre = get_object_or_404(queryset, pk=pk)
        serializer = GenreSerializer(genre, context=context)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = GenreSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        context = {'request': request}

        instance = self.get_object()
        serializer = GenreSerializer(instance, data=request.data, partial=False, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieViewSet(viewsets.ModelViewSet):

    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'genre__id', 'genre__title']
    # filter_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.filter()

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)

        # Other condition for different filter backend goes here

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset().prefetch_related('genre')
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MovieSerializer(page, many=True, context=context)
            print(connection.queries)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = MovieSerializer(queryset, many=True, context=context)
            data = serializer.data
            print(connection.queries)
            return Response(data)

    def retrieve(self, request, pk=None, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        movie = get_object_or_404(queryset, pk=pk)
        serializer = MovieSerializer(movie, context=context)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = MovieSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        context = {'request': request}

        instance = self.get_object()
        serializer = MovieSerializer(instance, data=request.data, partial=False, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
