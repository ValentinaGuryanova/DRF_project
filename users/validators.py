from collections import OrderedDict
from rest_framework import serializers


class AlreadySubscribedCheck:

    def __call__(self, fields: OrderedDict) -> None:
        """
        Проверка при создании подписки на существующую подписку.
        """
        course, user = fields.items()
        course = course[1]
        user = user[1]

        subs = user.subscriptions.all()

        if subs.filter(course=course).exists():
            raise serializers.ValidationError(f'Пользователь подписан на этот курс.')