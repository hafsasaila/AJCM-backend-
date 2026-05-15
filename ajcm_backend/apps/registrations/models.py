from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import TimeStampedModel
from apps.users.models import User
from apps.events.models import Event


class Registration(TimeStampedModel):
    """
    Modèle Registration - Inscription d'un utilisateur à un événement
    
    Relation : User ↔ Event (Many-to-Many avec attributs supplémentaires)
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('CANCELLED', 'Annulé'),
    ]
    
    # ==========================================
    # RELATIONS
    # ==========================================
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Utilisateur',
        help_text="L'utilisateur qui s'inscrit"
    )
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Événement',
        help_text="L'événement auquel on s'inscrit"
    )
    
    # ==========================================
    # STATUT
    # ==========================================
    
    status = models.CharField(
        'Statut',
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Statut de l'inscription"
    )
    
    # ==========================================
    # DATES IMPORTANTES
    # ==========================================
    
    confirmed_at = models.DateTimeField(
        'Date de confirmation',
        null=True,
        blank=True,
        help_text="Date à laquelle l'inscription a été confirmée"
    )
    
    cancelled_at = models.DateTimeField(
        'Date d\'annulation',
        null=True,
        blank=True,
        help_text="Date à laquelle l'inscription a été annulée"
    )
    
    # ==========================================
    # INFORMATIONS COMPLÉMENTAIRES
    # ==========================================
    
    notes = models.TextField(
        'Notes',
        blank=True,
        help_text="Notes optionnelles (ex: besoins spécifiques, commentaires)"
    )
    
    # ==========================================
    # MÉTADONNÉES
    # ==========================================
    
    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        ordering = ['-created_at']
        # Empêche un utilisateur de s'inscrire deux fois au même événement
        unique_together = ['user', 'event']
        indexes = [
            models.Index(fields=['user', 'event']),  # Pour vérifier les doublons
            models.Index(fields=['status']),         # Pour filtrer par statut
            models.Index(fields=['created_at']),     # Pour trier par date
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.event.Event_Name} ({self.get_status_display()})"
    
    # ==========================================
    # VALIDATION (avec vérifications des places)
    # ==========================================
    
    def clean(self):
        """
        Validation personnalisée avant sauvegarde
        
        Vérifications dans l'ordre :
        1. L'événement existe
        2. L'événement est publié (status = PUBLISHED)
        3. L'événement n'est pas annulé (status ≠ CANCELLED)
        4. L'événement n'est pas passé (date début > maintenant)
        5. L'événement n'est pas complet (places restantes > 0)
        """
        
        if not self.event:
            raise ValidationError({
                'event': "Événement requis"
            })
        
        # VÉRIFICATION 1 : L'événement doit être publié (pas en brouillon)
        if not self.event.is_published:
            raise ValidationError({
                'event': f"Cet événement n'est pas encore publié. Inscription impossible."
            })
        
        # VÉRIFICATION 2 : L'événement ne doit pas être annulé
        if self.event.is_cancelled:
            raise ValidationError({
                'event': f"Cet événement a été annulé. Inscription impossible."
            })
        
        # VÉRIFICATION 3 : L'événement ne doit pas être passé
        if self.event.is_past:
            raise ValidationError({
                'event': f"Impossible de s'inscrire à un événement passé."
            })
        
        # VÉRIFICATION 4 : Il doit rester des places (sauf si inscription déjà confirmée)
        if self.status == 'CONFIRMED' and self.event.is_full and not self.pk:
            raise ValidationError({
                'event': f"Plus de places disponibles. Cet événement est complet (max {self.event.max_places} places)."
            })
        
        # VÉRIFICATION 5 : L'utilisateur n'est pas déjà inscrit (géré par unique_together)
        # Cette vérification est automatique grâce à unique_together
        
        # ==========================================
        # MISE À JOUR AUTOMATIQUE DES DATES
        # ==========================================
        
        # Si le statut passe à CONFIRMED, enregistrer la date
        if self.status == 'CONFIRMED' and not self.confirmed_at:
            self.confirmed_at = timezone.now()
            
            # Mettre à jour le statut de l'événement (peut devenir COMPLET)
            self.event.update_status_based_on_capacity()
        
        # Si le statut passe à CANCELLED, enregistrer la date
        if self.status == 'CANCELLED' and not self.cancelled_at:
            self.cancelled_at = timezone.now()
            
            # Mettre à jour le statut de l'événement (une place s'est libérée)
            self.event.update_status_based_on_capacity()
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec validation automatique"""
        self.full_clean()  # Appelle clean() automatiquement
        super().save(*args, **kwargs)
    
    # ==========================================
    # PROPRIÉTÉS
    # ==========================================
    
    @property
    def is_confirmed(self):
        """Vérifie si l'inscription est confirmée"""
        return self.status == 'CONFIRMED'
    
    @property
    def is_pending(self):
        """Vérifie si l'inscription est en attente"""
        return self.status == 'PENDING'
    
    @property
    def is_cancelled(self):
        """Vérifie si l'inscription est annulée"""
        return self.status == 'CANCELLED'
    
    @property
    def can_cancel(self):
        """
        Vérifie si l'utilisateur peut encore annuler son inscription
        Un utilisateur peut annuler si :
        - L'événement n'est pas encore passé
        - L'inscription est confirmée
        """
        return self.event and not self.event.is_past and self.is_confirmed