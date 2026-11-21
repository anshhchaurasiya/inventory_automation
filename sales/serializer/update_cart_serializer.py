
from rest_framework import serializers

class UpdateCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
