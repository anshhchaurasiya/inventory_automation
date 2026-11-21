
from rest_framework import serializers
from sales.models.Purchase import Purchase
from .purchase_item_serializer import PurchaseItemSerializer


class PurchaseSerializer(serializers.ModelSerializer):

    items = PurchaseItemSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id',
            'user',
            'total_amount',
            'purchase_date',
            'status',
            'items'
        ]
        read_only_fields = [
            'id',
            'user',
            'total_amount',
            'purchase_date',
            'status',
            'items'
        ]
