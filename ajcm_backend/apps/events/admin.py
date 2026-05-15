from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventImage


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    
    list_display = (
        'Event_Name', 
        'type', 
        'status_colored',
        'start_date', 
        'location', 
        'city',
        'registrations_count_display',
        'places_remaining_display'
    )
    
    list_filter = ('type', 'status', 'city', 'start_date')
    search_fields = ('Event_Name', 'description', 'location', 'city')
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('Event_Name', 'type', 'description', 'status')
        }),
        ('Dates et durée', {
            'fields': ('start_date', 'end_date', 'Duration'),
            'classes': ('wide',)
        }),
        ('Lieu et capacité', {
            'fields': ('location', 'city', 'max_places', 'Volunteers', 'Cost')
        }),
        ('Métadonnées', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [EventImageInline]
    readonly_fields = ('created_by',)
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()
    
    def status_colored(self, obj):
        """Affiche le statut avec une couleur"""
        colors = {
            'DRAFT': '#ff9800',      # Orange
            'PUBLISHED': '#4caf50',  # Vert
            'CANCELLED': '#f44336',  # Rouge
            'COMPLET': '#9c27b0',    # Violet
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_colored.short_description = 'Statut'
    
    def registrations_count_display(self, obj):
        """Affiche le nombre d'inscrits"""
        count = obj.registrations_count
        if count == 0:
            return "0 inscrit"
        return f"{count} inscrit(s)"
    registrations_count_display.short_description = 'Inscrits'
    
    def places_remaining_display(self, obj):
        """Affiche les places restantes"""
        if obj.max_places == 0:
            return "Illimité"
        remaining = obj.places_remaining
        return f"{remaining}/{obj.max_places}"
    places_remaining_display.short_description = 'Places restantes'


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'order', 'uploaded_at', 'image_preview')
    list_filter = ('event', 'uploaded_at')
    list_editable = ('order',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'