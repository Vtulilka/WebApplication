from rest_framework import serializers
from TransactionApp.serializers import TransactionSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    transactions = serializers.TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'transactions']