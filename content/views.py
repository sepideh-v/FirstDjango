from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from content.models import Category, Content
from content.serializers import CategorySerializer, ContentSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category, context=context)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = CategorySerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        context = {'request': request}

        instance = self.get_object()
        serializer = CategorySerializer(instance, data=request.data, partial=False, context=context)
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


class ContentViewSet(viewsets.ModelViewSet):

    serializer_class = ContentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'categoryId']

    def get_queryset(self):
        return Content.objects.filter()

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)

        # Other condition for different filter backend goes here

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def list(self, request, *args, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        page = self.paginate_queryset(self.filter_queryset(queryset))
        if page is not None:
            serializer = ContentSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = ContentSerializer(queryset, many=True, context=context)
            return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        content = get_object_or_404(queryset, pk=pk)
        serializer = ContentSerializer(content, context=context)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = ContentSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        context = {'request': request}

        instance = self.get_object()
        serializer = ContentSerializer(instance, data=request.data, partial=False, context=context)
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
