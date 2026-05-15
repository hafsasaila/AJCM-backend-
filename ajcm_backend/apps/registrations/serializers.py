from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    event_name = serializers.CharField(source='event.Event_Name', read_only=True)
    
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'cancelled_at']