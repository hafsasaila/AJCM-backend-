from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour AJCM
    """
    ROLE_CHOICES = [
        ('VISITOR', 'Visiteur'),
        ('MEMBER', 'Membre'),
        ('ADMIN', 'Administrateur'),
    ]
    
    # Champs principaux
    email = models.EmailField('Email', unique=True)
    username = models.CharField('Nom d\'utilisateur', max_length=150, unique=True, blank=True)
    first_name = models.CharField('Prénom', max_length=150)
    last_name = models.CharField('Nom', max_length=150)
    
    # Champs optionnels
    phone = models.CharField('Téléphone', max_length=20, blank=True)
    age = models.PositiveIntegerField('Âge', null=True, blank=True)
    city = models.CharField('Ville', max_length=100, blank=True)
    bio = models.TextField('Biographie', blank=True)
    photo = models.ImageField('Photo de profil', upload_to='profile_pics/', null=True, blank=True)
    
    # Métadonnées
    role = models.CharField('Rôle', max_length=10, choices=ROLE_CHOICES, default='VISITOR')
    is_active = models.BooleanField('Actif', default=True)
    must_change_password = models.BooleanField('Doit changer mot de passe', default=True)
    
    # Dates
    date_joined = models.DateTimeField('Date d\'inscription', auto_now_add=True)
    updated_at = models.DateTimeField('Date de modification', auto_now=True)
    
    # Configuration pour l'authentification par email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Normaliser l'email en minuscules
        if self.email:
            self.email = self.email.lower()
        
        # Générer un username si vide
        if not self.username:
            base_username = slugify(f"{self.first_name}.{self.last_name}")
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_member(self):
        return self.role == 'MEMBER'
    
    @property
    def is_visitor(self):
        return self.role == 'VISITOR'