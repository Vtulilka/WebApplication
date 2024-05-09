from rest_framework import serializers
from .models import Transaction, Category
from taggit.serializers import TagListSerializerField, TaggitSerializer

class TransactionSerializerGeneric(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 
                  'amount', 
                  'is_expense']
        extra_kwargs = {
            'id': { 'read_only': True }
        }


class TransactionSerializerDetail(TaggitSerializer, serializers.ModelSerializer):
    user_tags = TagListSerializerField(required=False)

    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {
            'id': { 'read_only': True },
            'owner_id' : { 'read_only': True },
            'user_tags': { 'read_only': True },
            'category_id': { 'default': None },
            'description': { 'default': '' }
        }

    def validate(self, data):
        amount = data.get('amount') or None
        if amount:
            if int(amount) <= 0:
                raise serializers.ValidationError('Incorrect amount')
        
        is_expense = data.get('is_expense') or None
        if is_expense:
            if is_expense not in [True, False]:
                raise serializers.ValidationError('Incorrect type')
        
        user_tags = data.get('user_tags') or None
        method = self.context['request'].method
        if user_tags:
            raise serializers.ValidationError('To update tags use tag methods')
        
        owner_id = data.get('owner_id') or None
        if owner_id:
            raise serializers.ValidationError('Cannot update owner_id')
        
        category = data.get('category_id') or None
        if category and not Category.objects.filter(id=category.id).exists():
            raise serializers.ValidationError('Incorrect category')
        
        data['owner_id'] = self.context['request'].user
        return data
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 
            'name', 
            'description'
        ]