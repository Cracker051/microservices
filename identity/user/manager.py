from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError('User must have email and password!')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=email, password=password, is_superuser=True, is_staff=True, **extra_fields)
        return user
