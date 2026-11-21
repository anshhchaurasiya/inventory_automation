
from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):
    confirm_checkout = serializers.BooleanField(default=True)
