from rest_framework import serializers
from inventory.models import StockMovement

class StockMovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMovement
        fields = [
            'id',
            'product',
            'movement_type',
            'quantity',
            'reason',
            'created_at'
        ]

        read_only_fields = ['id', 'created_at']

    def validate_movement_type(self, value):
        value=value.upper()
        allowed_choices = ['IN', 'OUT', 'ADJUSTMENT']

        if value not in allowed_choices:
            raise serializers.ValidationError(
                "Invalid movement type. Allowed values are: IN, OUT, ADJUSTMENT."
            )

        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value