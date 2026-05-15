from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.permissions import IsAdmin
from .models import Partner
from .serializers import PartnerSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Partner.objects.all()
        return Partner.objects.filter(is_active=True)