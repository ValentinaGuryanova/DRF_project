from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Lesson


class LessonTestCase(APITestCase):

    def setUp(self):
        self.lesson = Lesson.objects.create(
            title='test lesson',
            description='testing',
            course_id= 2
        )

    def test_lesson_list(self):
        """
        Тест на список уроков
        """

        response = self.client.get(
            #reverse('education:lesson-list')
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "title": "test lesson",
                        "description": "testing",
                        "video_link": ''
                    },
                ]
            }
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_create_lesson(self):
        """
        Тест на создание урока
        """

        data = {
            "title": "test lesson",
            "description": "testing"
        }

        response = self.client.post(
            #reverse('education:lesson-create'),
            '/lesson/',
            data=data
        )

        self.assertTrue(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_lesson_retrieve(self):
        """
        Тест на просмотр урока
        """

        response = self.client.get(
            f'/lesson/{self.lesson.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):
        """
        Тест на изменение урока
        """

        data = {
            "title": "test lesson_update"
        }

        response = self.client.put(
            f'/lesson/{self.lesson.id}/update/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        """
        Тест на удаление урока
        """

        response = self.client.delete(
            f'/lesson/{self.lesson.id}/delete/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Lesson.objects.all().exists()
        )

    def tearDown(self) -> None:
        self.lesson.delete()
