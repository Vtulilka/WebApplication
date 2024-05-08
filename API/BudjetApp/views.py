from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Budjet
from .serializers import BudjetSerializerDetail, BudjetSerializerGeneric


class BudjetViewSet(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticated, ]
    serializer_class = BudjetSerializerDetail

    # Получение данных
    def get_queryset(self):
        start_at_id = int(self.request.GET.get('start_at_id') or 0)
        queryset = Budjet.objects.filter(id__gte=start_at_id)
        
        user = self.request.user
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner_id=user.id) 

        return queryset
    
    # Список бюджетов
    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = BudjetSerializerGeneric

        serializer = serializer_class(queryset[:10], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = request.data
        data['owner_id'] = request.user.id

        serializer = self.serializer_class(data=data,
                                           context={ 'request': self.request })
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        data = request.data
        data['owner_id'] = request.user.id

        serializer = self.serializer_class(data=data,
                                           context={ 'requst': self.request })
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data, status=status.HTTP_202_ACCEPTED)
