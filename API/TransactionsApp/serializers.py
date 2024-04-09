from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'ownerId', 'date', 'type', 'amount']
        extra_kwargs = {
            'id': { 'read_only': True },
            'ownerId': {'read_only': True},
        }

    def validate(self, attrs):
        print(self.context['request'].user.id)
        if not self.context['request'].user.is_staff:
            attrs['ownerId'] = self.context['request'].user
        
        return super().validate(attrs)   
