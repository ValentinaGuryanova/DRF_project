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


class Subscription(models.Model):
    course_name = models.CharField(max_length=300, verbose_name='Название подписки', **NULLABLE)
    course = models.ForeignKey('education.Course', verbose_name='Курс для подписки', on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='subscriptions')

    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка оформлена')

    def __str__(self):
        return f'{self.course} {self.user}'

    def save(self, *args, **kwargs):
        self.course_name = self.course.title

        return super(Subscription, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курс'