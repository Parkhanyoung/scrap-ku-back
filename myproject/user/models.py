from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
                                        BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Create a new user"""
        if not email:
            raise ValueError("User object must have an email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create a new superuser"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
