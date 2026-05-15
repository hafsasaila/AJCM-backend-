from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name',
                  'phone', 'age', 'city', 'bio', 'photo', 'role', 'is_active', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'age', 'city', 'bio', 'photo']
        read_only_fields = ['id', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(validators=[validate_password])


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)