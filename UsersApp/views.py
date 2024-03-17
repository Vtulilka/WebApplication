from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

