from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'email', 'password', 'phone_number', 'role']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)