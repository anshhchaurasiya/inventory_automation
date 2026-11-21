
from rest_framework import serializers
from sales.models.PurchaseItem import PurchaseItem


class PurchaseItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    sku = serializers.CharField(
        source='product.sku',
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseItem
        fields = [
            'id',
            'product',
            'product_name',
            'sku',
            'quantity',
            'unit_price',
            'subtotal'
        ]

    def get_subtotal(self, obj):
        return obj.quantity * obj.unit_price
