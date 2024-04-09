from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    # Получение данных только о текущем пользователе
    def get_queryset(self):
        start_at_id = 0
        if 'start_at_id' in self.request.data:
            start_at_id = int(self.request.data['start_at_id'])

        if not self.request.user.is_staff:
            user = self.request.user
            return Transaction.objects.filter(ownerId=user).filter(id>=start_at_id)
        else:
            return Transaction.objects.filter(id>=start_at_id)
    
    # Список транзакций
    def list(self, request):
        queryset = self.get_queryset()

        transactions_requested = min(100, queryset.count())
        if 'transactions_requested' in self.request.data:
            transactions_requested = min(transactions_requested, 
                                         int(self.request.data['transactions_requested']))
        
        serializer = self.serializer_class(queryset[:transactions_requested], many=True)

        return Response(serializer.data)
    
    
