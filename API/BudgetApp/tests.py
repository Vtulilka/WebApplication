from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Budget
import json

class BudgetCreateTestCase(APITestCase):
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

        self.data = [
            # All fields present
            {'name': 'test_budget', 'amount': 1000, 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000', },
            # Incorrect amount
            {'name': 'test_budget', 'amount': -1000, 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000', },
            # No amount
            {'name': 'test_budget', 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000', },
            # No name
            {'amount': 1000, 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000', },
            # No start_date
            {'name': 'test_budget', 'amount': 1000, 'end_date': '2024-09-04 06:00:00.000000', },
            # No end_date
            {'name': 'test_budget', 'amount': 1000, 'start_date': '2020-09-04 06:00:00.000000', },
            # Start_date > end_date
            {'name': 'test_budget', 'amount': 1000, 'start_date': '2024-09-04 06:00:00.000000', 'end_date': '2020-09-04 06:00:00.000000', },
        ]

        self.answers = [
            True,
            False,
            False,
            False,
            False,
            False,
            False
        ]

    def test_budget_created(self):
        results = []
        for entry in self.data:
            response = self.client.post('http://testserver/api/budgets/',
                                        data=entry)
            results.append(response.status_code == 201)
        self.assertEqual(results, self.answers)


class BudgetUpdateTestCase(APITestCase):
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

        Budget.objects.create(owner_id=self.user,
                              name='test_budget',
                              amount=1000,
                              start_date='2020-09-04 06:00:00.000000',
                              end_date='2024-09-04 06:00:00.000000')

        self.data = [
            # All fields present
            {'name': 'test_budget', 'amount': 1000, 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000'},
            # Incorrect amount
            {'name': 'test_budget', 'amount': -1000, 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000'},
            # No amount
            {'name': 'test_budget', 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000', },
            # No name
            {'amount': 1000, 'start_date': '2020-09-04 06:00:00.000000', 'end_date': '2024-09-04 06:00:00.000000', },
            # No start_date
            {'name': 'test_budget', 'amount': 1000, 'end_date': '2024-09-04 06:00:00.000000', },
            # No end_date
            {'name': 'test_budget', 'amount': 1000, 'start_date': '2020-09-04 06:00:00.000000', },
            # Start_date > end_date
            {'name': 'test_budget', 'amount': 1000, 'start_date': '2024-09-04 06:00:00.000000', 'end_date': '2020-09-04 06:00:00.000000', },
        ]

        self.full_update_answers = [
            True,
            False,
            False,
            False,
            False,
            False,
            False
        ]

        self.partial_update_answers = [
            True,
            False,
            True,
            True,
            True,
            True,
            False
        ]

    def test_budget_fully_updated(self):
        results = []
        for entry in self.data:
            response = self.client.put('http://testserver/api/budgets/1/',
                                        data=entry)
            results.append(response.status_code == 200)
        self.assertEqual(results, self.full_update_answers)

    def test_budget_partially_updated(self):
        results = []
        for entry in self.data:
            response = self.client.patch('http://testserver/api/budgets/1/',
                                        data=entry)
            results.append(response.status_code == 200)
        self.assertEqual(results, self.partial_update_answers)


class BudgetRetrieveTestCase(APITestCase):
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
        
        self.base_budget_data = {'owner_id': self.user,
                                 'amount': 1000,
                                 'start_date': '2020-09-04 06:00:00.000000',
                                 'end_date': '2024-09-04 06:00:00.000000',
                                 'name': 'test_name'}
        
        self.budget = Budget.objects.create(owner_id=self.user,
                                                      amount = self.base_budget_data['amount'],
                                                      start_date = self.base_budget_data['start_date'],
                                                      end_date = self.base_budget_data['end_date'],
                                                      name = self.base_budget_data['name'])
        
        self.budget = Budget.objects.create(owner_id=self.user,
                                                      amount = self.base_budget_data['amount'],
                                                      start_date = self.base_budget_data['start_date'],
                                                      end_date = self.base_budget_data['end_date'],
                                                      name = self.base_budget_data['name'])
        
        self.budget = Budget.objects.create(owner_id=User.objects.all()[2],
                                                      amount = self.base_budget_data['amount'],
                                                      start_date = self.base_budget_data['start_date'],
                                                      end_date = self.base_budget_data['end_date'],
                                                      name = self.base_budget_data['name'])
        
    def test_admin_can_list_all_budgets(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/budgets/')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        budget_ids = list(Budget.objects.all().values_list('id', flat=True))
        self.assertEqual(response_ids, budget_ids)
    
    def test_admin_can_retrieve_any_budget(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('http://testserver/api/budgets/2/')
        self.assertEqual(200, response.status_code)

    def test_user_can_list_only_owned_budgets(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/budgets/')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        budget_ids = list(Budget.objects.all().values_list('id', flat=True))[:2]
        self.assertEqual(response_ids, budget_ids)

    def test_user_can_retrieve_only_owned_budgets(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('http://testserver/api/budgets/2/')
        self.assertEqual(200, response.status_code)

        response = self.client.get('http://testserver/api/budgets/3/')
        self.assertEqual(404, response.status_code)
        
    def test_pagination(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get('http://testserver/api/budgets/?start_at_id=2')
        response_ids = [entry['id'] for entry in json.loads(response.content)]
        budget_ids = list(Budget.objects.all().values_list('id', flat=True))[1:]
        self.assertEqual(response_ids, budget_ids)
        

class BudgetDeleteTestCase(APITestCase):
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
        
        self.base_budget_data = {'owner_id': self.user,
                                 'amount': 1000,
                                 'start_date': '2020-09-04 06:00:00.000000',
                                 'end_date': '2024-09-04 06:00:00.000000',
                                 'name': 'test_name'}
        
        self.budget = Budget.objects.create(owner_id=self.user,
                                                      amount = self.base_budget_data['amount'],
                                                      start_date = self.base_budget_data['start_date'],
                                                      end_date = self.base_budget_data['end_date'],
                                                      name = self.base_budget_data['name'])
        
    def test_budget_deleted(self):
        response = self.client.delete('http://testserver/api/budgets/1/')
        self.assertEqual(False, Budget.objects.exists())
        