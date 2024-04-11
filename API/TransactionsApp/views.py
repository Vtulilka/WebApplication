from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    # Получение данных только о текущем пользователе
    def get_queryset(self):
        start_at_id = int(self.request.GET.get('start_at_id') or 0)

        if not self.request.user.is_staff:
            user = self.request.user
            return Transaction.objects.filter(ownerId=user.id).filter(id__gte=start_at_id)
        else:
            return Transaction.objects.filter(id__gte=start_at_id)
    
    # Список транзакций
    def list(self, request):
        queryset = self.get_queryset()

        transactions_requested = int(request.GET.get('transactions_requested') or 0)
        if transactions_requested <= 0 or transactions_requested > 100:
            transactions_requested = 100

        serializer = self.serializer_class(queryset[:transactions_requested], many=True)

        return Response(serializer.data)
