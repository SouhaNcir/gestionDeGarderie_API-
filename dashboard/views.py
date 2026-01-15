from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.contrib.auth.models import User
from enfants.models import Enfant, Parent, Staff
from accounts.models import UserProfile
from .serializers import (
    DashboardStatsSerializer, EnfantSummarySerializer, 
    ParentSummarySerializer, StaffSummarySerializer, UserSummarySerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_stats(request):
    """
    Retourner toutes les statistiques du dashboard
    """
    # Compter les éléments
    total_enfants = Enfant.objects.count()
    total_parents = Parent.objects.count()
    total_staff = Staff.objects.count()
    total_users = User.objects.count()
    
    # Enfants par groupe
    enfants_by_groupe = dict(
        Enfant.objects.values('groupe')
        .annotate(count=Count('id'))
        .values_list('groupe', 'count')
    )
    
    # Enfants par sexe
    enfants_by_sexe = dict(
        Enfant.objects.values('sexe')
        .annotate(count=Count('id'))
        .values_list('sexe', 'count')
    )
    
    # Staff par rôle
    staff_by_role = dict(
        Staff.objects.values('role')
        .annotate(count=Count('id'))
        .values_list('role', 'count')
    )
    
    # Utilisateurs par rôle
    users_by_role = dict(
        UserProfile.objects.values('role')
        .annotate(count=Count('id'))
        .values_list('role', 'count')
    )
    
    # 5 derniers enfants enregistrés
    enfants_recents = EnfantSummarySerializer(
        Enfant.objects.all().order_by('-date_inscription')[:5],
        many=True
    ).data
    
    data = {
        'total_enfants': total_enfants,
        'total_parents': total_parents,
        'total_staff': total_staff,
        'total_users': total_users,
        'enfants_by_groupe': enfants_by_groupe,
        'enfants_by_sexe': enfants_by_sexe,
        'staff_by_role': staff_by_role,
        'users_by_role': users_by_role,
        'enfants_recents': enfants_recents,
    }
    
    serializer = DashboardStatsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def enfants_list_admin(request):
    """
    Liste complète des enfants pour l'admin
    """
    queryset = Enfant.objects.select_related('parent', 'educateur').all()
    
    # Filtres optionnels
    groupe = request.query_params.get('groupe')
    sexe = request.query_params.get('sexe')
    parent_id = request.query_params.get('parent_id')
    
    if groupe:
        queryset = queryset.filter(groupe=groupe)
    if sexe:
        queryset = queryset.filter(sexe=sexe)
    if parent_id:
        queryset = queryset.filter(parent_id=parent_id)
    
    serializer = EnfantSummarySerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def parents_list_admin(request):
    """
    Liste complète des parents pour l'admin
    """
    queryset = Parent.objects.annotate(
        total_enfants=Count('enfant')
    ).all()
    
    # Filtres optionnels
    nom = request.query_params.get('nom')
    email = request.query_params.get('email')
    
    if nom:
        queryset = queryset.filter(nom__icontains=nom)
    if email:
        queryset = queryset.filter(email__icontains=email)
    
    serializer = ParentSummarySerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def staff_list_admin(request):
    """
    Liste complète du staff pour l'admin
    """
    queryset = Staff.objects.all()
    
    # Filtres optionnels
    role = request.query_params.get('role')
    nom = request.query_params.get('nom')
    
    if role:
        queryset = queryset.filter(role__icontains=role)
    if nom:
        queryset = queryset.filter(nom__icontains=nom)
    
    serializer = StaffSummarySerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def users_list_admin(request):
    """
    Liste complète des utilisateurs pour l'admin
    """
    queryset = User.objects.select_related('profile').all()
    
    # Filtres optionnels
    role = request.query_params.get('role')
    username = request.query_params.get('username')
    is_active = request.query_params.get('is_active')
    
    if role:
        queryset = queryset.filter(profile__role=role)
    if username:
        queryset = queryset.filter(username__icontains=username)
    if is_active:
        queryset = queryset.filter(profile__is_active=is_active.lower() == 'true')
    
    serializer = UserSummarySerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_overview(request):
    """
    Aperçu global du dashboard avec informations clés
    """
    return Response({
        'message': 'Bienvenue dans le tableau de bord administrateur',
        'endpoints': {
            'stats': '/api/dashboard/stats/',
            'enfants': '/api/dashboard/enfants/',
            'parents': '/api/dashboard/parents/',
            'staff': '/api/dashboard/staff/',
            'users': '/api/dashboard/users/',
        }
    })
