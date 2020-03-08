from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.utils.crypto import salted_hmac


class User(AbstractBaseUser):
    id = models.BigIntegerField
    createdAt = models.DateTimeField(auto_now_add=True, editable=False, db_column='created_at')
    name = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, db_column='last_name')
    username = models.CharField(max_length=70, unique=True)
    password = models.CharField(max_length=70)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user'

    REQUIRED_FIELDS = ('password', 'name', 'lastName')
    USERNAME_FIELD = 'username'

    objects = BaseUserManager()
