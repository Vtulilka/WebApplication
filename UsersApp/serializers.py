from rest_framework import serializers
from django.contrib.auth import authenticate
from TransactionsApp.serializers import TransactionSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', ]
        extra_kwargs = { 
            'password': { 'write_only': True },
            'id': { 'read_only': True },
            }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label='Username', 
        write_only=True
    )
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Проверка имени пользователя и пароля
        if username and password:
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                except ObjectDoesNotExist:
                    pass
            else:
                user = authenticate(request=self.context['request'],
                        username=username, 
                        password=password)

            # Пользователь не прошёл аутентификацию
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            # В запросе не переданы данные для аутентификации
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
    

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', ]
        extra_kwargs = { 
            'password': { 'write_only': True },
            'id': { 'read_only': True },
            }
        
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('Error: email already exists')
        
        username_exists = User.objects.filter(username=attrs['username']).exists()
        if username_exists:
            raise ValidationError('Error: username already exists')
        
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user