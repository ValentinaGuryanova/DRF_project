from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import NULLABLE
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    EDITOR = 'editor', _('editor')
    MEMBER = 'member', _('member')


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='Номер телефона', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Фото', **NULLABLE)
    role = models.CharField(default=UserRoles.MEMBER, choices=UserRoles.choices, verbose_name='роль пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
