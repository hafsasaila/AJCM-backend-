from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.permissions import IsAdmin
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        # Vérifier si l'utilisateur est connecté ET admin
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'is_admin') and user.is_admin:
            return Announcement.objects.all()
        # Pour les visiteurs non connectés : annonces actives et visibles
        return Announcement.objects.filter(is_active=True, is_visible=True)