from rest_framework import serializers
from inventory.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'phone_number',
            'alternate_phone_number',
            'email',
            'gst_number',
            'address'
        ]

        read_only_fields = ['id']

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value



