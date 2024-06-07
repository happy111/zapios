from rest_framework import serializers
from .models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlanType
        fields = "__all__"


class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPaymentModel
        fields = ("secret", "key")



