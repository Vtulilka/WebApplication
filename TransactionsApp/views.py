from rest_framework import viewsets
from rest_framework import permissions
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(ownerId=user)
