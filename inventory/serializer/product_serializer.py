from rest_framework import serializers
from inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'category',
            'supplier',
            'price',
            'gst',
            'stock_quantity'
        ]

        read_only_fields = ['id']

    def validate_sku(self, value):
        value=value.strip().upper()
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError(
                "SKU must be unique. A product with this SKU already exists."
            )
        
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Stock quantity cannot be negative."
            )
        return value

    def validate_gst(self,value):
        if value<0:
            raise serializers.ValidationError(
                "Stock quantity cannot be negative."
            )
        return value



class AddExistingProductSerializer(serializers.Serializer):

    sku = serializers.CharField(max_length=100)

    additional_quantity = serializers.IntegerField(min_value=1)

    def validate_sku(self, value):
        if not Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("Product with this SKU does not exist.")

        return value