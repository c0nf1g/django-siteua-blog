from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models


class BlogUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not first_name:
            raise ValueError('The given first_name must be set')
        if not last_name:
            raise ValueError('The given last_name must be set')

        email = self.normalize_email(email)
        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=email,
                          **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_super_user(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                password=password,
                                **extra_fields)


class BlogUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(verbose_name='email address', unique=True, blank=False)
    profile_photo = models.ImageField(upload_to='users_images/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = BlogUserManager()

    def __str__(self):
        return self.email
