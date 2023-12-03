from rest_framework import generics
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from education.permissions import IsOwner, IsModerator
from users.models import Subscription, User
from users.serializers import SubscriptionSerializer, UserSerializer, AnyUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """ Класс для создания пользователя """

    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    """ Класс для вывода списка пользователей """

    serializer_class = AnyUserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Класс для вывода одного пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.request.user == self.get_object():
            return UserSerializer
        else:
            return AnyUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Класс для изменения пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """ Класс для удаления пользователя """

    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(CreateAPIView):
    """ Класс для создания подписки """

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()


class SubscriptionListAPIView(generics.ListAPIView):
    """ Класс для вывода списка подписок """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """ Класс для изменения подписки """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class SubscriptionDestroyAPIView(DestroyAPIView):
    """ Класс для удаления подписки """

    queryset = Subscription.objects.all()