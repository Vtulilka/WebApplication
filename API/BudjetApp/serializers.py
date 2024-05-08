from rest_framework import serializers
from .models import Budjet

class BudjetSerializerGeneric(serializers.ModelSerializer):
    class Meta:
        model = Budjet
        fields = [
            'id',  
            'amount'
        ]
        extra_kwargs = {
            'id': { 'read_only': True }
        }


class BudjetSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Budjet
        fields = [
            'id', 
            'name', 
            'owner_id', 
            'amount', 
            'start_date',
            'end_date'
        ]
        extra_kwargs = {
            'id': { 'read_only': True },
            'owner_id' : { 'read_only': True }
        }

    def validate(self, data):
        amount = int(data.get('amount') or 0)
        if amount <= 0:
            raise serializers.ValidationError('Incorrect amount')
        
        owner_id = data.get('owner_id') or None
        if owner_id:
            raise serializers.ValidationError('Cannot update owner_id')
        
        start_date = data.get('start_date') or None
        end_date = data.get('end_date') or None
        if not(start_date and end_date) or start_date >= end_date:
            raise serializers.ValidationError('Wrong dates')
        
        data['owner_id'] = self.context['request'].user
        return data