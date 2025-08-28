#thie file is used to define serializers for user models
from rest_framework import serializers
from .models import Account,Addresses

# Serializer for the Account model
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields = '__all__'
        read_only_fields = ('date_joined', 'last_updated','is_active', 'is_staff', 'is_superuser', 'is_verified')
        required_fields = ['email', 'username', 'password']
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Addresses
        fields='__all__'