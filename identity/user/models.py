from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .manager import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True,
                                validators=[RegexValidator(
                                    regex=r'^(?=.*[A-Za-z0-9])[A-Za-z0-9._]+$',
                                    message='Username should not contain special characters')])  # Tests are needed
    password = models.CharField(max_length=32)
    created_at = models.DateField(editable=False, auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def __repr__(self):
        return '%s(%s)' % (self.username, self.created_at)
