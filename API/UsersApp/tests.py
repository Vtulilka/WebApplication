from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, UserSerializer
import json


class UserSignUpTestCase(APITestCase):
    def setUp(self):
        # Test data
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
                results.append(response.status_code == 201)
            except:
                results.append(False)

        self.assertEqual(results, self.answers)


class UserUpdateTestCase(APITestCase):
    def setUp(self):
        self.base_user_data = {'first_name': 'test_first_name', 
                          'last_name': 'test_last_name',
                          'username': 'test_username',
                          'email': 'test_email@e.mail',
                          'password': 'test_password'
        }

        User.objects.create(first_name=self.base_user_data['first_name'], 
                            last_name=self.base_user_data['last_name'], 
                            username=self.base_user_data['username'],
                            email=self.base_user_data['email']
                            )
        
        #Logging user in
        self.user = User.objects.get(username=self.base_user_data['username'])
        self.user.set_password(self.base_user_data['password'])
        self.client.force_authenticate(user=self.user)

        # Test data
        self.data = [
            # All essential fields present - True/True
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username', 'email': 'upd_email@e.mail'},
            # No last_name - False/True
            {'first_name': 'upd_first_name', 'username': 'upd_username', 'email': 'upd_email@e.mail'},
            # No first_name - False/True
            {'last_name': 'upd_last_name', 'username': 'upd_username', 'email': 'upd_email@e.mail'},
            # No username - False/True
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'email': 'upd_email@e.mail'},
            # No email - False/True
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username'},
            # Password in parameters - True/True
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username', 'email': 'upd_email@e.mail', 'password': 'upd_password'},
            # Username unchanged - True/True
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': self.base_user_data['username'], 'email': 'upd_email@e.mail'},
            # Email unchanged - True/True
            {'first_name': 'upd_first_name', 'last_name': 'upd_last_name', 'username': 'upd_username', 'email': self.base_user_data['email']}
        ]

        # Full update test answers
        self.full_update_answers = [
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
        ]
        
        # Partial update test answers
        self.partial_update_answers = [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ]

    # Return User object to its original state
    def restore(self, object, data):
        object.first_name = data['first_name']
        object.last_name = data['last_name']
        object.username = data['username']
        object.email = data['email']
        object.set_password(data['password'])
        object.save()

    # Testing full update
    def test_users_fully_updated(self):
        results = []
        for data_entry in self.data:
                response = self.client.put('http://testserver/api/users/1/', 
                                        data=data_entry)
                self.restore(self.user, self.base_user_data)
                results.append(response.status_code == 200)
        self.assertEqual(results, self.full_update_answers)

    # Testing partial update
    def test_users_partially_updated(self):
        results = []
        for data_entry in self.data:
            response = self.client.patch('http://testserver/api/users/1/', 
                                        data=data_entry)
            self.restore(self.user, self.base_user_data)
            results.append(response.status_code == 200)
        self.assertEqual(results, self.partial_update_answers)


class UserRetrieveTestCase(APITestCase):
    def setUp(self):
        self.base_user_data = {'first_name': 'test_first_name', 
                          'last_name': 'test_last_name',
                          'username': 'test_username',
                          'email': 'test_email@e.mail',
                          'password': 'test_password'
        }
        
        # Admin id=1
        self.admin = User.objects.create_superuser('admin', 'admin@ad.min', 'admin')

        for i in '23456':
            User.objects.create(first_name=f"{self.base_user_data['first_name']}_{i}", 
                                last_name=f"{self.base_user_data['last_name']}_{i}", 
                                username=f"{self.base_user_data['username']}_{i}",
                                email=f"{self.base_user_data['email']}_{i}"
                                )
            user = User.objects.get(username=f"{self.base_user_data['username']}_{i}")
            user.set_password(self.base_user_data['password'])
        
        # User test_username_1, id=2
        self.user = User.objects.get(username=f"{self.base_user_data['username']}_2")
    
    # Test listing all users as admin
    def test_users_listed_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/users/')
        user_ids = list(User.objects.all().values_list('id', flat=True))
        response_ids = [user['id'] for user in json.loads(response.content)]
        self.assertEqual(user_ids, response_ids)

    # Test listing users from id=3 as admin
    def test_users_listed_admin_start(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/users/?start_at_id=3')
        user_ids = list(User.objects.all().values_list('id', flat=True)[2:])
        response_ids = [user['id'] for user in json.loads(response.content)]
        self.assertEqual(user_ids, response_ids)

    # Test admin can retrieve any user
    def test_admin_retrieves_any_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/users/2/')
        self.assertEqual(200, response.status_code)

    # Test non-staff user have no access to list method
    def test_users_listed(self):
        # Login as user with id=1
        self.client.force_authenticate(user=self.user) 
        response = self.client.get('http://testserver/api/users/')
        self.assertEqual(403, response.status_code)

    # Test that users can't retrieve other users
    def test_user_retrieves_any_user(self):
        self.client.force_authenticate(user=self.user)
        # Trying to retrieve user with id=3
        response = self.client.get('http://testserver/api/users/4/')
        self.assertEqual(404, response.status_code)

    # Test users can retrieve themselves
    def test_user_retrieves_themselves(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/users/2/')
        self.assertEqual(200, response.status_code)


class UserDeleteTestCase(APITestCase):
    def setUp(self):
        self.base_user_data = {'first_name': 'test_first_name', 
                          'last_name': 'test_last_name',
                          'username': 'test_username',
                          'email': 'test_email@e.mail',
                          'password': 'test_password'
        }
    

        User.objects.create(first_name=self.base_user_data['first_name'], 
                            last_name=self.base_user_data['last_name'], 
                            username=self.base_user_data['username'],
                            email=self.base_user_data['email']
                            )
        
        # User test_username, id=1
        self.user = User.objects.get(username=self.base_user_data['username'])
        self.user.set_password(self.base_user_data['password'])
        self.client.force_authenticate(user=self.user)

    def test_user_deleted(self):
        response = self.client.delete('http://testserver/api/users/1/')
        users_exist = User.objects.exists()
        self.assertEqual(users_exist, False)
