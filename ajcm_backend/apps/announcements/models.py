from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel
from apps.users.models import User
from apps.events.models import Event


class Announcement(TimeStampedModel):
    """
    Modèle Announcement - Annonces publiques
    L'image est OBLIGATOIRE selon le cahier des charges
    """
    
    TYPE_CHOICES = [
        ('NEWS', 'Actualité'),
        ('ALERT', 'Alerte'),
        ('PROMO', 'Promotion'),
        ('INFO', 'Information'),
        ('EVENT', 'Événement'),
    ]
    
    # ==========================================
    # CHAMPS PRINCIPAUX
    # ==========================================
    
    title = models.CharField(
        'Titre',
        max_length=200,
        help_text="Titre accrocheur de l'annonce"
    )
    
    content = models.TextField(
        'Contenu',
        help_text="Contenu détaillé de l'annonce"
    )
    
    type = models.CharField(
        'Type',
        max_length=20,
        choices=TYPE_CHOICES,
        default='NEWS',
        help_text="Type d'annonce (détermine l'apparence)"
    )
    
    # ==========================================
    # IMAGE (OBLIGATOIRE)
    # ==========================================
    
    image = models.ImageField(
        'Image',
        upload_to='announcements/',
        help_text="Image de l'annonce (obligatoire pour l'affichage visuel)"
    )
    
    # ==========================================
    # VISIBILITÉ
    # ==========================================
    
    is_active = models.BooleanField(
        'Active',
        default=True,
        help_text="Cochez pour afficher l'annonce sur le site"
    )
    
    is_featured = models.BooleanField(
        'À la une',
        default=False,
        help_text="Les annonces à la une apparaissent en premier"
    )
    
    # ==========================================
    # LIENS
    # ==========================================
    
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements',
        verbose_name='Événement lié',
        help_text="Lien optionnel vers un événement (affiche un bouton 'Participer')"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements',
        verbose_name='Auteur',
        help_text="Administrateur qui a créé l'annonce"
    )
    
    # ==========================================
    # EXPIRATION
    # ==========================================
    
    expires_at = models.DateTimeField(
        'Date d\'expiration',
        null=True,
        blank=True,
        help_text="Si renseigné, l'annonce disparaît automatiquement après cette date"
    )
    
    # ==========================================
    # MÉTADONNÉES
    # ==========================================
    
    class Meta:
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_expired(self):
        """Vérifie si l'annonce est expirée"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def is_visible(self):
        """Vérifie si l'annonce doit être affichée sur le site"""
        return self.is_active and not self.is_expired
    
    @property
    def type_color(self):
        """Retourne la couleur associée au type pour l'affichage CSS"""
        colors = {
            'NEWS': '#2196F3',   # Bleu
            'ALERT': '#F44336',  # Rouge
            'PROMO': '#4CAF50',  # Vert
            'INFO': '#9E9E9E',   # Gris
            'EVENT': '#9C27B0',  # Violet
        }
        return colors.get(self.type, '#2196F3')
    
    @property
    def type_icon(self):
        """Retourne l'icône associée au type"""
        icons = {
            'NEWS': '📰',
            'ALERT': '⚠️',
            'PROMO': '🏷️',
            'INFO': 'ℹ️',
            'EVENT': '📅',
        }
        return icons.get(self.type, '📰')