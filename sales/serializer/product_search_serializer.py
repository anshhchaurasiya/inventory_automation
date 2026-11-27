from rest_framework import serializers
from inventory.models import Product


class ProductSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'price',
            'stock_quantity',
            'gst'
        ]