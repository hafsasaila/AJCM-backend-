from django.contrib import admin
from django.utils.html import format_html
from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les partenaires
    """
    
    # Colonnes affichées dans la liste
    list_display = (
        'id',
        'logo_preview',
        'name',
        'type_colored',
        'website_link',
        'is_active_icon',
        'order',
        'created_at'
    )
    
    # Filtres latéraux
    list_filter = ('type', 'is_active', 'created_at')
    
    # Champs recherchables
    search_fields = ('name', 'description', 'email', 'phone')
    
    # Champs éditable directement dans la liste
    list_editable = ('order',)  # ← Retiré 'is_active' de list_editable
    
    # Champs en lecture seule
    readonly_fields = ('created_at', 'updated_at', 'logo_preview_large')
    
    # Organisation du formulaire
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'type', 'logo', 'logo_preview_large')
        }),
        ('Contact', {
            'fields': ('website', 'email', 'phone'),
            'classes': ('wide',)
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Affichage', {
            'fields': ('is_active', 'order')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Actions personnalisées
    actions = ['activate_partners', 'deactivate_partners']
    
    # ==========================================
    # MÉTHODES D'AFFICHAGE
    # ==========================================
    
    def logo_preview(self, obj):
        """Aperçu du logo dans la liste"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />',
                obj.logo.url
            )
        return "Pas de logo"
    logo_preview.short_description = 'Logo'
    
    def logo_preview_large(self, obj):
        """Aperçu du logo agrandi dans le formulaire"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.logo.url
            )
        return "Pas de logo"
    logo_preview_large.short_description = 'Aperçu du logo'
    
    def type_colored(self, obj):
        """Affiche le type avec une couleur"""
        colors = {
            'SPONSOR': '#4caf50',
            'MEDIA': '#2196f3',
            'INSTITUTION': '#9c27b0',
            'ASSOCIATION': '#ff9800',
            'COMPANY': '#00bcd4',
            'OTHER': '#9e9e9e',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 11px;">{}</span>',
            colors.get(obj.type, '#9e9e9e'),
            obj.get_type_display()
        )
    type_colored.short_description = 'Type'
    
    def website_link(self, obj):
        """Lien cliquable vers le site web"""
        if obj.website:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.website,
                obj.website[:30] + '...' if len(obj.website) > 30 else obj.website
            )
        return '-'
    website_link.short_description = 'Site web'
    
    def is_active_icon(self, obj):
        """Icône pour l'état actif/inactif"""
        if obj.is_active:
            return format_html('<span style="color: #4caf50; font-size: 16px;">✅</span>')
        return format_html('<span style="color: #f44336; font-size: 16px;">❌</span>')
    is_active_icon.short_description = 'Actif'
    
    # ==========================================
    # ACTIONS GROUPÉES
    # ==========================================
    
    def activate_partners(self, request, queryset):
        """Active les partenaires sélectionnés"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} partenaire(s) activé(s)')
    activate_partners.short_description = 'Activer les partenaires sélectionnés'
    
    def deactivate_partners(self, request, queryset):
        """Désactive les partenaires sélectionnés"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} partenaire(s) désactivé(s)')
    deactivate_partners.short_description = 'Désactiver les partenaires sélectionnés'