from rest_framework import serializers

from education.models import Payment
from users.models import Subscription
from users.validators import AlreadySubscribedCheck

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Класс сериализатора для модели User """

    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        # fields = ('email', 'phone', 'avatar', 'city', 'is_active', 'payments')

    def get_payments(self, user):
        """ Метод определения поля payments, возвращает список платежей пользователя """

        payments = []
        for payment in Payment.objects.filter(payment_user=user):
            pay = [payment.payment_date, payment.amount]
            payments.append(pay)
        return payments


class AnyUserSerializer(serializers.ModelSerializer):
    """ Класс сериализатора для модели User при использовании стронним пользователем """

    class Meta:
        model = User
        fields = ('id', 'email', 'city')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [AlreadySubscribedCheck()]