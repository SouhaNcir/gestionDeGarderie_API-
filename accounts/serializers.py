from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'telephone', 'is_active', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='parent')
    telephone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'role', 'telephone']

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({
                'password': 'Les mots de passe ne correspondent pas.'
            })
        return data

    def create(self, validated_data):
        role = validated_data.pop('role', 'parent')
        telephone = validated_data.pop('telephone', '')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        
        # Créer le profil utilisateur
        UserProfile.objects.create(
            user=user,
            role=role,
            telephone=telephone
        )
        
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Personnaliser la réponse JWT avec les informations de l'utilisateur"""
    
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter les informations de l'utilisateur
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.profile.role if hasattr(user, 'profile') else 'user'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Ajouter les infos utilisateur à la réponse
        data['user'] = UserSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': 'Les mots de passe ne correspondent pas.'
            })
        return data
