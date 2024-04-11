from rest_framework import serializers
from .models import Transaction
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer

class TransactionSerializer(TaggitSerializer, serializers.ModelSerializer):
    
    tags = TagListSerializerField()

    class Meta:
        model = Transaction
        fields = ['id', 'ownerId', 'date', 'type', 'amount', 'tags']
        extra_kwargs = {
            'id': { 'read_only': True },
            'tags' : {'read_only': True},
            'ownerId': {'write_only': True}
        }

    def validate(self, data):
        amount = int(data.get('amount') or 0)
        if amount <= 0:
            raise serializers.ValidationError('Incorrect amount')
        
        type = int(data.get('type') or 0)
        if type <= 0:
            raise serializers.ValidationError('Incorrect type')
        
        tags = data.get('tags') or None
        method = self.context['request'].method
        if tags and method != 'POST':
            raise serializers.ValidationError('Cannot update tags')
        
        ownerId = data.get('ownerId') or None
        if ownerId:
            raise serializers.ValidationError('Cannot update ownerId')
        
        return data
