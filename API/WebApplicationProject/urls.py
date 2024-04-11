from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from TransactionsApp.views import TransactionViewSet, TagViewset, tags
from UsersApp.views import UserViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'transactions', TagViewset, basename='transactions')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/transactions/tags/', tags),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls, name='admin'),
]