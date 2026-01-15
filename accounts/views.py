from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)
from .models import UserProfile


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vue personnalisée pour obtenir les tokens JWT"""
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Enregistrer un nouvel utilisateur"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Obtenir les informations de l'utilisateur actuel"""
    user = request.user
    return Response(UserSerializer(user).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Changer le mot de passe de l'utilisateur"""
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'L\'ancien mot de passe est incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Mot de passe modifié avec succès'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Mettre à jour le profil de l'utilisateur"""
    user = request.user
    profile = user.profile
    
    # Mettre à jour les champs utilisateur
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    user.save()
    
    # Mettre à jour le profil
    profile.telephone = request.data.get('telephone', profile.telephone)
    profile.save()
    
    return Response({
        'message': 'Profil mis à jour avec succès',
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout - Blacklist le token (optionnel avec une base de données)"""
    return Response({'message': 'Logout réussi'})
