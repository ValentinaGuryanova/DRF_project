from rest_framework import serializers

from users.models import Subscription
from users.validators import AlreadySubscribedCheck


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [AlreadySubscribedCheck()]