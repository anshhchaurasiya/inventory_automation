
from rest_framework import serializers
from sales.models.CartItem import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    sku = serializers.CharField(
        source='product.sku',
        read_only=True
    )
    unit_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
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
        return obj.quantity * obj.product.price
