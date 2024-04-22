from rest_framework import serializers
from .models import Transaction, Category
from taggit.serializers import TagListSerializerField, TaggitSerializer

class TransactionSerializerGeneric(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 
                  'owner_id', 
                  'amount', 
                  'date', 
                  'type']
        extra_kwargs = {
            'id': { 'read_only': True },
            'owner_id' : { 'read_only': True }
        }


class TransactionSerializerDetail(TaggitSerializer, serializers.ModelSerializer):
    user_tags = TagListSerializerField(required=False)

    class Meta:
        model = Transaction
        fields = ['id', 
                  'owner_id', 
                  'amount', 
                  'date', 
                  'type', 
                  'category_id', 
                  'description', 
                  'user_tags']
        extra_kwargs = {
            'id': { 'read_only': True },
            'owner_id' : { 'read_only': True },
            'user_tags': { 'read_only': True },
            'category_id': { 'default': None },
            'description': { 'default': '' }
        }

    def validate(self, data):
        amount = int(data.get('amount') or 0)
        if amount <= 0:
            raise serializers.ValidationError('Incorrect amount')
        
        type = data.get('type') or None
        if type not in ['Expense', 'Income']:
            raise serializers.ValidationError('Incorrect type')
        
        user_tags = data.get('user_tags') or None
        method = self.context['request'].method
        if user_tags:
            raise serializers.ValidationError('To update tags use tag methods')
        
        owner_id = data.get('owner_id') or None
        if owner_id:
            raise serializers.ValidationError('Cannot update owner_id')
        
        category_id = data.get('category_id') or None
        if category_id and not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError('Incorrect category')
        
        data['owner_id'] = self.context['request'].user
        return data