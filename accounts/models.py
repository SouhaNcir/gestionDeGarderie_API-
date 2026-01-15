from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile"""
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('educateur', 'Éducateur'),
        ('parent', 'Parent'),
        ('directeur', 'Directeur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    telephone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
