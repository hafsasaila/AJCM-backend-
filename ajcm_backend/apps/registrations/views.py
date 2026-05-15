from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin
from .models import Registration
from .serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Registration.objects.all()
        return Registration.objects.filter(user=user)