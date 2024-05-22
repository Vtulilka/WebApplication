from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer

# Create your tests here.

# Тест проверяет работу сериализатора создания нового пользователя
class UserSignUpTestCase(TestCase):
    def setUp(self):
        self.data = [
            # передаются все поля - True
            {'username': 'first', 'password': 'password_1', 'email': 'first@e.mail', 'first_name': 'first_first_name', 'last_name': 'first_last_name'}, 
            # нет last_name - True
            {'username': 'second', 'password': 'password_2', 'email': 'second@e.mail', 'first_name': 'second_first_name'}, 
            # нет first_name - True
            {'username': 'third', 'password': 'password_3', 'email': 'third@e.mail', 'last_name': 'third_last_name'},
            # не уникальный пароль - True
            {'username': 'fourth', 'password': 'password_1', 'email': 'fourth@e.mail'}, 
            # не уникальный username - False
            {'username': 'first', 'password': 'password_5', 'email': 'fifth@e.mail'},
            # не уникальный email - False
            {'username': 'sixth', 'password': 'password_6', 'email': 'first@e.mail'},
            # нет password - False
            {'username': 'seventh', 'email': 'seventh@e.mail'}, 
            # нет email - False
            {'username': 'eigth', 'password': 'password_8'},
            # нет username - False
            {'password': 'password_9', 'email': 'ninth@e.mail'}
        ]
        self.answers = [
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False
        ]

    def test_users_created(self):
        results = []
        for entry in self.data:
            try:
                response = self.client.post('/api/users/', entry)
                results.append(response.status_code < 300)
            except:
                results.append(False)

        self.assertEqual(results, self.answers)


class UserUpdateTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='test_first_name', 
                            last_name='test_last_name', 
                            username='test_username', 
                            password='test_password', 
                            email='test_email@e.mail'
                            )
        
        self.object = User.objects.get(username='test_username')
        self.client.login(username=self.object.username, password=self.object.password)

        self.data = [
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username', 'email': 'upd_email@e.mail'},
            {'first_name': 'upd_first_name', 'username': 'upd_username', 'email': 'upd_email@e.mail'},
            {'last_name': 'upd_last_name', 'username': 'upd_username', 'email': 'upd_email@e.mail'},
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'email': 'upd_email@e.mail'},
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username'},
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username', 'email': 'upd_email@e.mail', 'password': 'upd_password'}
        ]

        self.answers = [
            False,
            False,
            False,
            False,
            False,
            False
        ]

    def test_users_updated(self):
        results = []
        
        for entry in self.data:
            try:
                response = self.client.put('/api/users/', entry)
                response.request['user'] = self.object
                serializer = UserSerializer(self.object, data=entry, partial=False, context={'request': response.request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                results.append(response.status_code < 300)
            except:
                results.append(False)


        self.assertEqual(results, self.answers)