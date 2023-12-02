from rest_framework.generics import CreateAPIView, DestroyAPIView

from users.models import Subscription
from users.serializers import SubscriptionSerializer


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()