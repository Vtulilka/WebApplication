from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializerDetail, TransactionSerializerGeneric
from rest_framework.decorators import action, api_view, permission_classes
from taggit.models import Tag


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TransactionSerializerDetail

    # Получение данных только о текущем пользователе
    def get_queryset(self):
        start_at_id = int(self.request.GET.get('start_at_id') or 0)

        if not self.request.user.is_staff:
            user = self.request.user
            return Transaction.objects.filter(owner_id=user.id).filter(id__gte=start_at_id)
        else:
            return Transaction.objects.filter(id__gte=start_at_id)
    
    # Список транзакций
    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = TransactionSerializerGeneric

        transactions_requested = int(request.GET.get('transactions_requested') or 0)
        if transactions_requested <= 0 or transactions_requested > 100:
            transactions_requested = 100

        serializer = serializer_class(queryset[:transactions_requested], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = request.data
        data['owner_id'] = request.user.id

        serializer = self.serializer_class(data=data,
                                           context={ 'request': self.request })
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data, status=status.HTTP_201_CREATED)


class TagViewset(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Transaction.objects.all()

    @action(detail=True,
            methods=['patch'])
    def add_tag(self, request, pk=None):
        request_tags = [tag.strip() for tag in request.data['user_tags']]
        if not all([tag for tag in request_tags]): 
            raise serializers.ValidationError('Incorrect tag name')
        
        transaction = self.get_object()
        for tag in request_tags:
            transaction.user_tags.add(tag)

        return Response({'user_tags': transaction.user_tags.names()}, status=status.HTTP_206_PARTIAL_CONTENT)

    @action(detail=True,
            methods=['patch'])
    def remove_tag(self, request, pk=None):
        user_tags = [t.strip() for t in request.data['user_tags']]
        if not all([t for t in tags]): 
            raise serializers.ValidationError('Incorrect tag name')
        
        transaction = self.get_object()
        for tag in user_tags:
            transaction.tags.remove(tag)

        return Response({'user_tags': transaction.user_tags.names()}, status=status.HTTP_206_PARTIAL_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def tags(request):
    user_tags = Tag.objects.all()
    user_tag_names = [tag.name for tag in user_tags]
    
    return Response({'user_tags': user_tag_names}, status=status.HTTP_200_OK)
