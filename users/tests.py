from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson
from users.models import User, Subscription


class SubscriptionPositiveTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='vmalnova@yandex.ru',
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            title='test course',
            description='test course',
        )

        self.lesson = Lesson.objects.create(
            title='test lesson',
            description='test lesson',
            video_link='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )

    def test_subscription_create(self):
        """
        Тест на создание подписки
        """
        data = {
            'course': self.course.pk,
            'user': self.user.pk
        }

        response = self.client.post(
            reverse('users:subscription_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_delete(self):
        """
        Тест на удаление подписки
        """

        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
        )

        url = reverse('users:subscription_delete', kwargs={'pk': subscription.pk})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )


class SubscriptionNegativeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='vmalnova@yandex.ru',
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            title='test course',
            description='test course',
        )

        self.lesson = Lesson.objects.create(
            title='test lesson',
            description='test lesson',
            video_link='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )

    def test_subscription_create(self):
        data = {
            'course': self.course.pk,
            'user': self.user.pk,
        }

        response = self.client.post(
            reverse('users:subscription_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse('users:subscription_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
