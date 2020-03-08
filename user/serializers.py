from django.contrib.auth.hashers import make_password
from pyexpat import model

from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    @staticmethod
    def validate_password(value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    class Meta:
        model = User
        fields = ['id', 'createdAt', 'name', 'lastName', 'username', 'password']
