from django.db import connection
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.permission import CustomUpdatePermission
from user.serializers import UserSerializer


# class UserViewSet(mixins.ListModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.CreateModelMixin,
#                   mixins.UpdateModelMixin,
#                   GenericViewSet):

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch']
    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [IsAuthenticated],
                                    'retrieve': [IsAuthenticated],
                                    'partial_update': [IsAuthenticated, CustomUpdatePermission]}

    # permission_classes = (CustomUpdatePermission,)  # specify custom permission class here

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True, context=context)
        data = serializer.data
        print(connection.queries)
        return Response(data)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, pk=None, **kwargs):
        context = {'request': request}

        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context=context)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = UserSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated], url_path='change_username')
    # def change_username(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     user = request.user
    #     user.username =
    #     serializer = UserSerializer(instance, data=request.da, partial=True)
    #     userId = request.user.id
    #     return self.update(request, userId)
