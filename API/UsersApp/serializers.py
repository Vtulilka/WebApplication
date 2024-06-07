from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):  
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=150, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', ]
        extra_kwargs = { 
            'id': { 'read_only': True },
            }        
        
    def validate(self, data):
        if 'username' in data:
            try:
                username_is_changed = data['username'] != self.context['request'].user.username
            except:
                username_is_changed = data['username'] != self.context['request']['user'].username
            username_exists = User.objects.filter(username=data['username']).exists()

            if username_is_changed and username_exists:
                raise serializers.ValidationError('Username already exists')
            
        if 'email' in data:
            try:
                email_is_changed = data['email'] != self.context['request'].user.email
            except:
                email_is_changed = data['email'] != self.context['request']['user'].email
            email_exists = User.objects.filter(email=data['email']).exists()

            if email_is_changed and email_exists:
                raise serializers.ValidationError('Email already exists')
        
        return data


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
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        # Проверка имени пользователя и пароля
        if username and password:
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                except ObjectDoesNotExist:
                    user = None
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
            msg = 'Both username/email and password are required.'
            raise serializers.ValidationError(msg, code='authorization')
        
        data['user'] = user
        return data
    

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', ]
        extra_kwargs = { 
            'password': { 'write_only': True },
            'id': { 'read_only': True },
            }
        
    def validate(self, data):
        email_exists = User.objects.filter(email=data['email']).exists()
        if email_exists:
            raise serializers.ValidationError('Error: email already exists')
        
        username_exists = User.objects.filter(username=data['username']).exists()
        if username_exists:
            raise serializers.ValidationError('Error: username already exists')
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user