from rest_framework import serializers
from django.db import models
from TransactionsApp.models import Transaction, Category
from django.db.models import Sum
from BudgetApp.models import Budget

class ReportTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 
                  'amount', 
                  'date',
                  'category_id'
        ]


class ReportCategorySerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'total_amount'
        ]

    def get_total_amount(self, object):
        return object['total_amount']

class ReportBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 
                  'name'
                  'amount', 
                  'start_date',
                  'end_date'
        ]


class ReportPeriodSerializer(serializers.Serializer):
    owner_id = serializers.SerializerMethodField()
    is_expense = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    transactions = ReportTransactionSerializer(many=True)
    categories = ReportCategorySerializer(many=True)

    def get_owner_id(self, object):
        return object['owner_id']
    
    def get_is_expense(self, object):
        return object['is_expense']
    
    def get_total_amount(self, object):
        return object['total_amount']
    
    def get_start_date(self, object):
        return object['start_date']
    
    def get_end_date(self, object):
        return object['end_date']


class ReportBudgetSerializer(serializers.Serializer):
    owner_id = serializers.SerializerMethodField()
    remainder = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    total_expense = serializers.SerializerMethodField()
    budget = ReportBudgetSerializer()
    
    def get_total_income(self, object):
        return object['total_income']
    
    def get_total_expense(self, object):
        return object['total_expense']

    def get_remainder(self, object):
        return object['remainder']
    
    def get_owner_id(self, object):
        return object['owner_id']