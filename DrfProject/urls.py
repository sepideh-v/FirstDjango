"""DrfProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import content
import movie
import user
from user import views
from content import views
from movie import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', user.views.UserViewSet, basename='users')
router.register('category', content.views.CategoryViewSet, basename='category')
router.register('content', content.views.ContentViewSet, basename='content')
router.register('genre', movie.views.GenreViewSet, basename='genre')
router.register('movie', movie.views.MovieViewSet, basename='movie')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
