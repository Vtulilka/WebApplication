from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from .permissions import NotAuthorizedPermission
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from . import serializers
from django.core import exceptions


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes=[permissions.IsAuthenticated, ]
    permission_classes_by_action = {'create': [NotAuthorizedPermission, ],
                                    'login': [NotAuthorizedPermission, ],
                                    'list': [permissions.IsAdminUser, ], }

    # Получение данных только о текущем пользователе
    def get_queryset(self):
        start_at_id = int(self.request.GET.get('start_at_id') or 0)

        if not self.request.user.is_staff:
            user = self.request.user
            qs = User.objects.filter(id=user.id)
        else:
            qs = User.objects.all()
        
        return qs.filter(id__gte=start_at_id)

    def get_permissions(self):
        try: 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
        
    def create(self, request):
        data = request.data

        serializer = serializers.SignUpSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, 
            methods=['post'])
    def login(self, request):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        user_serializer = serializers.UserSerializer(instance=user)
        return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, 
            methods=['get'])
    def logout(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post'])
    def change_password(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            raise exceptions.BadRequest('Both old and new password must be provided')
        
        user = request.user    
        if not user.check_password(old_password):
            raise exceptions.PermissionDenied('Permission denied')
        user.set_password(new_password)
        user.save()

        return Response(None, status=status.HTTP_202_ACCEPTED)


