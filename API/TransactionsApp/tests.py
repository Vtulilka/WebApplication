from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Transaction, Category
from .serializers import TransactionSerializerDetail
from taggit.models import Tag
import json


class TransactionCreateTestCase(APITestCase):
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
        
        Category.objects.create(name='test_category_name',
                                description='test_category_description')

        # User test_username, id=1
        self.user = User.objects.get(username=self.base_user_data['username'])
        self.user.set_password(self.base_user_data['password'])
        self.client.force_authenticate(user=self.user)

    # Correct way. No category and description
    def test_transaction_created_basic(self):
        data = {'amount': 1000, 'is_expense': True, 'date': '2024-09-04 06:00:00.000000'}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        response_content = json.loads(response.content)
        self.assertEqual(str(data['amount']), response_content['amount'])
        self.assertEqual(str(data['is_expense']), response_content['is_expense'])
        self.assertEqual(data['date'], response_content['date'])

    # Test creating transaction with description
    def test_transaction_created_description(self):
        data = {'amount': 1000, 'is_expense': True, 'date': '2024-09-04 06:00:00.000000', 'description': 'test_description'}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        response_content = json.loads(response.content)
        self.assertEqual(str(data['amount']), response_content['amount'])
        self.assertEqual(str(data['is_expense']), response_content['is_expense'])
        self.assertEqual(data['date'], response_content['date'])
        self.assertEqual(data['description'], response_content['description'])

    # Test creating transaction with category id present
    def test_transaction_created_category(self):
        # Category with id=1 exists
        data = {'amount': 1000, 'is_expense': True, 'date': '2024-09-04 06:00:00.000000', 'category_id': 1}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        self.assertEqual(201, response.status_code)

        # Category with id=2 does not exist
        data = {'amount': 1000, 'is_expense': True, 'date': '2024-09-04 06:00:00.000000', 'category_id': 2}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        self.assertEqual(400, response.status_code)

    # Test creating transaction with user_tags present
    def test_transaction_created_tags(self):
        data = {'amount': 1000, 'is_expense': True, 'date': '2024-09-04 06:00:00.000000', 'user_tags': ['test_tag1', 'test_tag2']}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        self.assertEqual(400, response.status_code)

    # Test creating transaction without specifying is_expense
    def test_transaction_created_no_is_expense(self):
        data = {'amount': 1000, 'date': '2024-09-04 06:00:00.000000',}
        # Default is_expense=False
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        response_content = json.loads(response.content)
        transaction = Transaction.objects.all()[0]
        self.assertEqual(False, transaction.is_expense)

    # Test creating transactions with incomplete data
    def test_transaction_created_incomplete_data(self):
        data = [
            # No date
            {'amount': 1000},
            # No amount
            {'date': '2024-09-04 06:00:00.000000'}
        ]
        for entry in data:
            response = self.client.post('http://testserver/api/transactions/', 
                                    data=entry)
            self.assertEqual(400, response.status_code)

    def test_transaction_created_validated(self):
        data = {'amount': -1000, 'date': '2024-09-04 06:00:00.000000'}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        self.assertEqual(400, response.status_code)

        data = {'owner_id': 1, 'amount': 1000, 'date': '2024-09-04 06:00:00.000000'}
        response = self.client.post('http://testserver/api/transactions/', 
                                    data=data)
        self.assertEqual(201, response.status_code)


class TransactionTagTestCase(APITestCase):
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

        Category.objects.create(name='test_category_name',
                                description='test_category_description')
        
        Transaction.objects.create(owner_id=self.user,
                                   amount=1000,
                                   date='2024-09-04 06:00:00.000000',
                                   is_expense=True,
                                   description='test_description'
                                   )
    # Add tags to transaction
    def test_tag_added(self):
        response = self.client.patch('http://testserver/api/transactions/1/add_tag/',
                                     data={'user_tags': 'tag1'})
        response = self.client.patch('http://testserver/api/transactions/1/add_tag/',
                                     data={'user_tags': 'tag2'})
        transaction = Transaction.objects.all()[0]
        self.assertEqual(list(transaction.user_tags.names()), ['tag1', 'tag2'])

    # Test adding an empty tag
    def test_tag_added_blank(self):
        response = self.client.patch('http://testserver/api/transactions/1/add_tag/',
                                     data={'user_tags': ''})
        response = self.client.patch('http://testserver/api/transactions/1/add_tag/',
                                     data={'user_tags': '      '})
        transaction = Transaction.objects.all()[0]
        self.assertEqual(list(transaction.user_tags.names()), [])

    # Test removing a tag
    def test_tag_removed(self):
        response = self.client.patch('http://testserver/api/transactions/1/remove_tag/',
                                     data={'user_tags': 'tag1'})
        self.assertEqual(400, response.status_code)
            
        response = self.client.patch('http://testserver/api/transactions/1/add_tag/',
                                     data={'user_tags': 'tag1'})
        response = self.client.patch('http://testserver/api/transactions/1/remove_tag/',
                                     data={'user_tags': 'tag1'})
        self.assertEqual(206, response.status_code)
        
    
class TransactionUpdateTestCase(APITestCase):
    def setUp(self):
        # User test_username, id=1
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

        self.user = User.objects.get(username=self.base_user_data['username'])
        self.user.set_password(self.base_user_data['password'])
        self.client.force_authenticate(user=self.user)

        # Id=1
        Category.objects.create(name='test_category_name_1',
                                description='test_category_description')
        # Id=2
        Category.objects.create(name='test_category_name_2',
                                description='test_category_description')
        
        self.base_transaction_data = {'owner_id': self.user,
                                      'amount': 1000,
                                      'date': '2024-09-04 06:00:00.000000',
                                      'is_expense': True,
                                      'description': 'test_description',
                                      'category_id': Category.objects.all()[0]}
        
        self.transaction = Transaction.objects.create(owner_id=self.base_transaction_data['owner_id'],
                                                      amount = self.base_transaction_data['amount'],
                                                      date = self.base_transaction_data['date'],
                                                      is_expense = self.base_transaction_data['is_expense'],
                                                      description = self.base_transaction_data['description'],
                                                      category_id = self.base_transaction_data['category_id'])
        
        self.data = [
            # All fields present
            {'amount': 1000, 'date': '2024-09-04 06:00:00.000000', 'is_expense': True, 'description': 'test_description', 'category_id': 1},
            # Incorrect amount
            {'amount': -1000, 'date': '2024-09-04 06:00:00.000000', 'is_expense': True, 'description': 'test_description', 'category_id': 1},
            # No amount
            {'date': '2024-09-04 06:00:00.000000', 'is_expense': True, 'description': 'test_description', 'category_id': 1},
            # No date
            {'amount': 1000, 'is_expense': True, 'description': 'test_description', 'category_id': 1},
            # No is_expense
            {'amount': 1000, 'date': '2024-09-04 06:00:00.000000', 'description': 'test_description', 'category_id': 1},
            # No description
            {'amount': 1000, 'date': '2024-09-04 06:00:00.000000', 'is_expense': True, 'category_id': 1},
            # No category_id
            {'amount': 1000, 'date': '2024-09-04 06:00:00.000000', 'is_expense': True, 'description': 'test_description'},
        ]

        self.full_update_answers = [
            True,
            False,
            False,
            False,
            True,
            True,
            True
        ]

        self.partial_update_answers = [
            True,
            False,
            True,
            True,
            True,
            True,
            True
        ]

    def test_transaction_fully_update(self):
        results = []
        for entry in self.data:
            response = self.client.put('http://testserver/api/transactions/1/', 
                                        data=entry)
            results.append(response.status_code == 200)
        self.assertEqual(results, self.full_update_answers)

    def test_transaction_partially_updated(self):
        results = []
        for entry in self.data:
            response = self.client.patch('http://testserver/api/transactions/1/', 
                                        data=entry)
            results.append(response.status_code == 200)
        self.assertEqual(results, self.partial_update_answers)


class TransactionRetrieveTestCase(APITestCase):
    def setUp(self):
        # Admin id=1
        self.admin = User.objects.create_superuser('admin', 'admin@ad.min', 'admin')
        
        
        self.base_user_data = {'first_name': 'test_first_name', 
                          'last_name': 'test_last_name',
                          'username': 'test_username',
                          'email': 'test_email@e.mail',
                          'password': 'test_password'
        }

        # User test_username_2, id=2
        User.objects.create(first_name=self.base_user_data['first_name'] + '_2', 
                            last_name=self.base_user_data['last_name'] + '_2', 
                            username=self.base_user_data['username'] + '_2',
                            email=self.base_user_data['email'] + '_2'
                            )
        
        # User test_username_3, id=3
        User.objects.create(first_name=self.base_user_data['first_name'] + '_3', 
                            last_name=self.base_user_data['last_name'] + '_3', 
                            username=self.base_user_data['username'] + '_3',
                            email=self.base_user_data['email'] + '_3'
                            )

        self.user = User.objects.get(username=self.base_user_data['username'] + '_2')
        self.user.set_password(self.base_user_data['password'])

        # Id=1
        Category.objects.create(name='test_category_name_1',
                                description='test_category_description')
        # Id=2
        Category.objects.create(name='test_category_name_2',
                                description='test_category_description')
        
        self.base_transaction_data = {'owner_id': self.user,
                                      'amount': 1000,
                                      'date': '2024-09-04 06:00:00.000000',
                                      'is_expense': True,
                                      'description': 'test_description',
                                      'category_id': Category.objects.all()[0]}
        
        self.transaction = Transaction.objects.create(owner_id=self.base_transaction_data['owner_id'],
                                                      amount = self.base_transaction_data['amount'],
                                                      date = self.base_transaction_data['date'],
                                                      is_expense = self.base_transaction_data['is_expense'],
                                                      description = self.base_transaction_data['description'],
                                                      category_id = self.base_transaction_data['category_id'])
        
        self.transaction = Transaction.objects.create(owner_id=self.base_transaction_data['owner_id'],
                                                      amount = self.base_transaction_data['amount'],
                                                      date = self.base_transaction_data['date'],
                                                      is_expense = self.base_transaction_data['is_expense'],
                                                      description = self.base_transaction_data['description'],
                                                      category_id = self.base_transaction_data['category_id'])
        
        self.transaction = Transaction.objects.create(owner_id=User.objects.all()[2],
                                                      amount = self.base_transaction_data['amount'],
                                                      date = self.base_transaction_data['date'],
                                                      is_expense = self.base_transaction_data['is_expense'],
                                                      description = self.base_transaction_data['description'],
                                                      category_id = self.base_transaction_data['category_id'])
        
    def test_admin_can_list_all_transactions(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/transactions/')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        transaction_ids = list(Transaction.objects.all().values_list('id', flat=True))
        self.assertEqual(response_ids, transaction_ids)
    
    def test_admin_can_retrieve_any_transaction(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/transactions/2/')
        self.assertEqual(200, response.status_code)

    def test_user_can_list_only_owned_transactions(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/transactions/')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        transaction_ids = list(Transaction.objects.all().values_list('id', flat=True))[:2]
        self.assertEqual(response_ids, transaction_ids)

    def test_user_can_retrieve_only_owned_transactions(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('http://testserver/api/transactions/2/')
        self.assertEqual(200, response.status_code)

        response = self.client.get('http://testserver/api/transactions/3/')
        self.assertEqual(404, response.status_code)
        
    def test_pagination(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get('http://testserver/api/transactions/?start_at_id=2')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        transaction_ids = list(Transaction.objects.all().values_list('id', flat=True))[1:]
        self.assertEqual(response_ids, transaction_ids)

        response = self.client.get('http://testserver/api/transactions/?transactions_requested=2')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        transaction_ids = list(Transaction.objects.all().values_list('id', flat=True))[:2]
        self.assertEqual(response_ids, transaction_ids)

        response = self.client.get('http://testserver/api/transactions/?start_at_id=2&transactions_requested=1')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        transaction_ids = list(Transaction.objects.all().values_list('id', flat=True))[1:2]
        self.assertEqual(response_ids, transaction_ids)


class TransactionDeleteTestCase(APITestCase):
    def setUp(self):
        # User test_username, id=1
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

        self.user = User.objects.get(username=self.base_user_data['username'])
        self.user.set_password(self.base_user_data['password'])
        self.client.force_authenticate(user=self.user)

        # Id=1
        Category.objects.create(name='test_category_name_1',
                                description='test_category_description')
        # Id=2
        Category.objects.create(name='test_category_name_2',
                                description='test_category_description')
        
        self.base_transaction_data = {'owner_id': self.user,
                                      'amount': 1000,
                                      'date': '2024-09-04 06:00:00.000000',
                                      'is_expense': True,
                                      'description': 'test_description',
                                      'category_id': Category.objects.all()[0]}
        
        self.transaction = Transaction.objects.create(owner_id=self.base_transaction_data['owner_id'],
                                                      amount = self.base_transaction_data['amount'],
                                                      date = self.base_transaction_data['date'],
                                                      is_expense = self.base_transaction_data['is_expense'],
                                                      description = self.base_transaction_data['description'],
                                                      category_id = self.base_transaction_data['category_id'])
        
    def test_transaction_deleted(self):
        response = self.client.delete('http://testserver/api/transactions/1/')
        self.assertEqual(False, Transaction.objects.exists())
        