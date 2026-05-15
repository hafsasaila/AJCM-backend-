from django.contrib import admin
from django.utils.html import format_html
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les inscriptions
    """
    
    # Colonnes affichées dans la liste
    list_display = (
        'id',
        'user_info',
        'event_info',
        'status_colored',
        'event_status_info',
        'confirmed_at',
        'cancelled_at',
        'created_at'
    )
    
    # Filtres latéraux
    list_filter = ('status', 'event__status', 'event__type', 'created_at', 'confirmed_at')
    
    # Champs recherchables
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'event__Event_Name')
    
    # Champs en lecture seule
    readonly_fields = ('confirmed_at', 'cancelled_at', 'created_at', 'updated_at')
    
    # Organisation du formulaire
    fieldsets = (
        ('Informations principales', {
            'fields': ('user', 'event', 'status')
        }),
        ('Dates', {
            'fields': ('confirmed_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Ordre par défaut
    ordering = ('-created_at',)
    
    # Actions personnalisées
    actions = ['confirm_registrations', 'cancel_registrations']
    
    # ==========================================
    # MÉTHODES D'AFFICHAGE PERSONNALISÉES
    # ==========================================
    
    def user_info(self, obj):
        """Affiche les informations de l'utilisateur"""
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            obj.user.full_name,
            obj.user.email
        )
    user_info.short_description = 'Utilisateur'
    
    def event_info(self, obj):
        """Affiche les informations de l'événement"""
        places_info = ""
        if obj.event.max_places > 0:
            places_info = f"<br><small>Places: {obj.event.registrations_count}/{obj.event.max_places}</small>"
        
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{} - {}</small>{}',
            obj.event.Event_Name,
            obj.event.start_date.strftime('%d/%m/%Y %H:%M'),
            obj.event.location,
            places_info
        )
    event_info.short_description = 'Événement'
    
    def event_status_info(self, obj):
        """Affiche le statut de l'événement avec une couleur"""
        colors = {
            'DRAFT': '#ff9800',      # Orange
            'PUBLISHED': '#4caf50',  # Vert
            'CANCELLED': '#f44336',  # Rouge
            'COMPLET': '#9c27b0',    # Violet
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.event.status, '#000'),
            obj.event.get_status_display()
        )
    event_status_info.short_description = 'Statut événement'
    
    def status_colored(self, obj):
        """Affiche le statut de l'inscription avec une couleur"""
        colors = {
            'PENDING': '#ff9800',    # Orange
            'CONFIRMED': '#4caf50',  # Vert
            'CANCELLED': '#f44336',  # Rouge
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_colored.short_description = 'Statut inscription'
    
    # ==========================================
    # ACTIONS GROUPÉES
    # ==========================================
    
    def confirm_registrations(self, request, queryset):
        """
        Action admin pour confirmer des inscriptions
        Vérifie les places disponibles avant confirmation
        """
        confirmed_count = 0
        error_count = 0
        
        for registration in queryset:
            if registration.status == 'PENDING':
                # Vérifier qu'il reste des places
                if registration.event.is_full:
                    self.message_user(
                        request, 
                        f"❌ {registration.event.Event_Name} est complet - impossible de confirmer {registration.user.full_name}",
                        level='ERROR'
                    )
                    error_count += 1
                else:
                    registration.status = 'CONFIRMED'
                    registration.confirmed_at = timezone.now()
                    registration.save()
                    confirmed_count += 1
            else:
                error_count += 1
        
        if confirmed_count > 0:
            self.message_user(request, f'✅ {confirmed_count} inscription(s) confirmée(s)')
        if error_count > 0:
            self.message_user(request, f'⚠️ {error_count} inscription(s) non confirmée(s)', level='WARNING')
    
    confirm_registrations.short_description = 'Confirmer les inscriptions sélectionnées'
    
    def cancel_registrations(self, request, queryset):
        """Action admin pour annuler des inscriptions"""
        updated = queryset.update(status='CANCELLED', cancelled_at=timezone.now())
        
        # Mettre à jour le statut des événements concernés
        for registration in queryset:
            registration.event.update_status_based_on_capacity()
        
        self.message_user(request, f'{updated} inscription(s) annulée(s)')
    
    cancel_registrations.short_description = 'Annuler les inscriptions sélectionnées'