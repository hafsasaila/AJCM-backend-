from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Configuration personnalisée de l'admin pour les utilisateurs
    """
    
    list_display = (
        'photo_preview',
        'email',
        'first_name',
        'last_name',
        'role',
        'phone',
        'age',
        'city',
        'is_active',
        'date_joined'
    )
    
    list_filter = ('role', 'is_active', 'city', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('email', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'phone', 'age', 'city', 'bio', 'photo')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )
    
    ordering = ('-date_joined',)
    actions = ['make_active', 'make_inactive', 'make_member', 'make_admin']
    
    def photo_preview(self, obj):
        """Affiche un aperçu de la photo de profil"""
        if obj.photo and obj.photo.url:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;" />',
                obj.photo.url
            )
        return "📷"
    photo_preview.short_description = 'Photo'
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} utilisateur(s) activé(s)')
    make_active.short_description = 'Activer'
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} utilisateur(s) désactivé(s)')
    make_inactive.short_description = 'Désactiver'
    
    def make_member(self, request, queryset):
        updated = queryset.update(role='MEMBER')
        self.message_user(request, f'{updated} utilisateur(s) deviennent membre(s)')
    make_member.short_description = 'Rôle MEMBER'
    
    def make_admin(self, request, queryset):
        updated = queryset.update(role='ADMIN')
        self.message_user(request, f'{updated} utilisateur(s) deviennent admin(s)')
    make_admin.short_description = 'Rôle ADMIN'