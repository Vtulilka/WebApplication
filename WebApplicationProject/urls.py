from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from TransactionsApp.views import TransactionViewSet
from UsersApp.views import UserViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls, name='admin'),
]