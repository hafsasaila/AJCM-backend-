from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.permissions import IsAdmin
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Announcement.objects.all()
        return Announcement.objects.filter(is_active=True, is_visible=True)