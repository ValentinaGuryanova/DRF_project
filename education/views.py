from datetime import datetime, timedelta

import pytz
import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from stripe.http_client import requests

import education

from education.models import Course, Lesson, Payment
from education.paginators import ListPaginator
from education.permissions import IsModerator, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    pagination_class = ListPaginator

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """

    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        education.send_mail.delay(new_lesson.course_id)

class LessonListAPIView(generics.ListAPIView):
    """ Просмотр списка всех уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    pagination_class = ListPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [AllowAny, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Изменение урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, IsModerator | IsOwner]

    def perform_update(self, serializer):
        changed_lesson = serializer.save()
        date_time_now = datetime.now()
        moscow_timezone = pytz.timezone('Europe/Moscow')
        date_now = date_time_now.astimezone(moscow_timezone)
        if changed_lesson.lesson_datetime_changing:
            lesson_last_change_date = changed_lesson.lesson_datetime_changing.astimezone(moscow_timezone)
            if abs(date_now - lesson_last_change_date) > timedelta(hours=4):
                education.send_mail.delay(changed_lesson.course_id)
        changed_lesson.lesson_datetime_changing = date_now
        changed_lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """

    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание платежа """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def payment_create(self, serializer):
        payment = serializer.save()
        stripe.api_key = "sk_test_51OIyYKCkqWIHezmzqscY7yo2kHjIqColutBIHgqEEZKq7FtZriwc4jmUc5KtAxOnRo4dkDiOfP6s3ZFhWNlrRSKN00B4CHbgIU"
        pay = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency='usd',
            automatic_payment_methods={'enabled': True},
        )
        pay.save()
        return super().perform_create(serializer)


class PaymentListAPIView(generics.ListAPIView):
    """ Список платежей """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'pay_type')
    ordering_fields = ('payment_date', 'pay_type')
    permission_classes = [AllowAny]
    pagination_class = ListPaginator


class PaymentRetrieveView(generics.RetrieveAPIView):
    """ Просмотр платежа """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_payment(self, request, payment_id):
        """ Получение информации о платеже """

        stripe.api_key = "sk_test_51OIyYKCkqWIHezmzqscY7yo2kHjIqColutBIHgqEEZKq7FtZriwc4jmUc5KtAxOnRo4dkDiOfP6s3ZFhWNlrRSKN00B4CHbgIU"

        payments_retrieve = stripe.PaymentIntent.retrieve(payment_id)
        print(payments_retrieve.status)
        return Response({
            'status': payments_retrieve.status,
            'body': payments_retrieve})