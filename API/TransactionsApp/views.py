from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializerDetail, TransactionSerializerGeneric
from rest_framework.decorators import action, api_view, permission_classes
from taggit.models import Tag


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TransactionSerializerDetail

    # Получение данных
    def get_queryset(self):
        start_at_id = int(self.request.GET.get('start_at_id') or 0)
        queryset = Transaction.objects.filter(id__gte=start_at_id)
        
        user = self.request.user
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner_id=user.id) 

        requested_user_tags = self.request.query_params.getlist('user_tags') or None
        if requested_user_tags:
            for tag in requested_user_tags:
                queryset = queryset.filter(user_tags__name__iexact=tag).distinct()

        return queryset
    
    # Список транзакций
    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = TransactionSerializerGeneric

        transactions_requested = int(request.query_params.get('transactions_requested') or 0)
        if transactions_requested <= 0 or transactions_requested > 100:
            transactions_requested = 100

        serializer = serializer_class(queryset[:transactions_requested], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = request.data

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
        tag = request.data['user_tags'].strip()
        if not tag: 
            raise serializers.ValidationError('Incorrect tag name')
        
        transaction = self.get_object()
        transaction.user_tags.add(tag)

        return Response({'user_tags': transaction.user_tags.names()}, status=status.HTTP_206_PARTIAL_CONTENT)

    @action(detail=True,
            methods=['patch'])
    def remove_tag(self, request, pk=None):
        transaction = self.get_object()
        
        tag = request.data['user_tags'].strip()
        if not tag or tag not in transaction.user_tags.names():
            raise serializers.ValidationError('Incorrect tag name')
        
        
        transaction.user_tags.remove(tag)

        return Response({'user_tags': transaction.user_tags.names()}, status=status.HTTP_206_PARTIAL_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def tags(request):
    user_tags = Tag.objects.all()
    user_tag_names = [tag.name for tag in user_tags]
    
    return Response({'user_tags': user_tag_names}, status=status.HTTP_200_OK)
