from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from TransactionsApp.views import TransactionViewSet, TagViewset, tags
from UsersApp.views import UserViewSet
from BudjetApp.views import BudjetViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'transactions', TagViewset, basename='transaction-tags')
router.register(r'users', UserViewSet, basename='users')
router.register(r'budjets', BudjetViewSet, basename='budjets')

urlpatterns = [
    path('api/transaction/tags/', tags),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls, name='admin'),
]