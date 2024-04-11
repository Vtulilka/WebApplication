from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'ownerId', 'date', 'type', 'amount']
        extra_kwargs = {
            'id': { 'read_only': True },
            'ownerId': { 'read_only': True }
        }

    def validate(self, data):
        amount = int(data.get('amount') or 0)
        if amount <= 0:
            raise serializers.ValidationError('Incorrect amount')
        
        type = int(data.get('type') or 0)
        if type <= 0:
            raise serializers.ValidationError('Incorrect type')
        
        return data
