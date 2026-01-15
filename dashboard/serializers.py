from rest_framework import serializers
from django.contrib.auth.models import User
from enfants.models import Enfant, Parent, Staff
from accounts.models import UserProfile


class DashboardStatsSerializer(serializers.Serializer):
    """Sérializer pour les statistiques du dashboard"""
    total_enfants = serializers.IntegerField()
    total_parents = serializers.IntegerField()
    total_staff = serializers.IntegerField()
    total_users = serializers.IntegerField()
    enfants_by_groupe = serializers.DictField()
    enfants_by_sexe = serializers.DictField()
    staff_by_role = serializers.DictField()
    users_by_role = serializers.DictField()
    enfants_recents = serializers.ListField()
    

class EnfantSummarySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.nom', read_only=True)
    educateur_name = serializers.CharField(source='educateur.nom', read_only=True)
    
    class Meta:
        model = Enfant
        fields = ['id', 'nom', 'prenom', 'parent_name', 'educateur_name', 'groupe', 'date_inscription']


class ParentSummarySerializer(serializers.ModelSerializer):
    total_enfants = serializers.SerializerMethodField()
    
    class Meta:
        model = Parent
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'total_enfants']
    
    def get_total_enfants(self, obj):
        return obj.enfant_set.count()


class StaffSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'nom', 'prenom', 'role', 'email', 'telephone']


class UserSummarySerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    is_active = serializers.CharField(source='profile.is_active', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active']
