import re
from rest_framework import serializers
from sales.models import CustomerDetails


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = [
            'id',
            'purchase',
            'customer_name',
            'phone',
            'email',
            'customer_type',
            'company_name',
            'gstin',
            'address',
            'city',
            'state',
            'pincode',
            'payment_method',
            'notes',
            'created_at',
        ]
        read_only_fields = ['id', 'purchase', 'created_at']
        extra_kwargs = {
            'company_name': {'required': False, 'allow_blank': True, 'allow_null': True},
            'gstin': {'required': False, 'allow_blank': True, 'allow_null': True},
            'notes': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def validate_phone(self, value):
        cleaned = value.strip()
        if not re.match(r'^[6-9]\d{9}$', cleaned):
            raise serializers.ValidationError("Enter a valid 10-digit Indian mobile number.")
        return cleaned

    def validate_pincode(self, value):
        cleaned = value.strip()
        if not re.match(r'^\d{6}$', cleaned):
            raise serializers.ValidationError("Enter a valid 6-digit pincode.")
        return cleaned

    def validate(self, attrs):
        customer_type = attrs.get('customer_type', 'Individual')
        company_name = (attrs.get('company_name') or '').strip()
        gstin = (attrs.get('gstin') or '').strip().upper()

        if customer_type == 'Business':
            if not company_name:
                raise serializers.ValidationError({
                    'company_name': 'Company name is required for Business orders.'
                })
            if gstin and not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', gstin):
                raise serializers.ValidationError({
                    'gstin': 'Enter a valid 15-character GSTIN.'
                })

        attrs['company_name'] = company_name or None
        attrs['gstin'] = gstin or None
        attrs['notes'] = (attrs.get('notes') or '').strip() or None
        return attrs