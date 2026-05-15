from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les annonces
    """
    
    # Colonnes affichées dans la liste
    list_display = (
        'id',
        'title_preview',
        'type_colored',
        'event_link',
        'is_featured_icon',
        'is_active_icon',
        'is_visible_status',
        'expires_at',
        'created_at'
    )
    
    # Filtres latéraux
    list_filter = (
        'type',
        'is_active',
        'is_featured',
        'event',
        'created_at',
        'expires_at'
    )
    
    # Champs recherchables
    search_fields = ('title', 'content')
    
    # Champs en lecture seule
    readonly_fields = ('created_at', 'updated_at', 'author', 'image_preview')
    
    # Organisation du formulaire
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'content', 'type', 'image', 'image_preview')
        }),
        ('Visibilité', {
            'fields': ('is_active', 'is_featured', 'expires_at')
        }),
        ('Liens', {
            'fields': ('event',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('author', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Actions personnalisées
    actions = ['activate_announcements', 'deactivate_announcements', 'feature_announcements']
    
    # ==========================================
    # MÉTHODES D'AFFICHAGE
    # ==========================================
    
    def save_model(self, request, obj, form, change):
        """Sauvegarde automatique de l'auteur"""
        if not change:
            obj.author = request.user
        obj.save()
    
    def title_preview(self, obj):
        """Aperçu du titre tronqué"""
        if len(obj.title) > 50:
            return obj.title[:47] + '...'
        return obj.title
    title_preview.short_description = 'Titre'
    
    def image_preview(self, obj):
        """Aperçu de l'image dans le formulaire"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 200px;" />',
                obj.image.url
            )
        return "Pas d'image"
    image_preview.short_description = 'Aperçu de l\'image'
    
    def type_colored(self, obj):
        """Affiche le type avec une couleur"""
        colors = {
            'NEWS': '#2196F3',   # Bleu
            'ALERT': '#F44336',  # Rouge
            'PROMO': '#4CAF50',  # Vert
            'INFO': '#9E9E9E',   # Gris
            'EVENT': '#9C27B0',  # Violet
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            colors.get(obj.type, '#2196F3'),
            obj.get_type_display()
        )
    type_colored.short_description = 'Type'
    
    def event_link(self, obj):
        """Affiche le lien vers l'événement"""
        if obj.event:
            return format_html(
                '<a href="/admin/events/event/{}/change/">{}</a>',
                obj.event.id,
                obj.event.Event_Name
            )
        return "-"
    event_link.short_description = 'Événement lié'
    
    def is_featured_icon(self, obj):
        """Icône pour 'À la une'"""
        if obj.is_featured:
            return format_html('<span style="color: #ff9800; font-size: 16px;">⭐</span>')
        return "-"
    is_featured_icon.short_description = 'Une'
    
    def is_active_icon(self, obj):
        """Icône pour 'Active'"""
        if obj.is_active:
            return format_html('<span style="color: #4caf50; font-size: 16px;">✅</span>')
        return format_html('<span style="color: #f44336; font-size: 16px;">❌</span>')
    is_active_icon.short_description = 'Active'
    
    def is_visible_status(self, obj):
        """Affiche si l'annonce est visible sur le site"""
        if obj.is_visible:
            return format_html('<span style="color: #4caf50; font-weight: bold;">✓ Visible</span>')
        elif not obj.is_active:
            return format_html('<span style="color: #f44336;">✗ Désactivée</span>')
        elif obj.is_expired:
            return format_html('<span style="color: #f44336;">✗ Expirée</span>')
        return format_html('<span style="color: #9e9e9e;">-</span>')
    is_visible_status.short_description = 'Visibilité site'
    
    # ==========================================
    # ACTIONS GROUPÉES
    # ==========================================
    
    def activate_announcements(self, request, queryset):
        """Active les annonces sélectionnées"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} annonce(s) activée(s)')
    activate_announcements.short_description = 'Activer les annonces sélectionnées'
    
    def deactivate_announcements(self, request, queryset):
        """Désactive les annonces sélectionnées"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} annonce(s) désactivée(s)')
    deactivate_announcements.short_description = 'Désactiver les annonces sélectionnées'
    
    def feature_announcements(self, request, queryset):
        """Met les annonces sélectionnées à la une"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} annonce(s) mise(s) à la une')
    feature_announcements.short_description = 'Mettre à la une'