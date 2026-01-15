from rest_framework import serializers
from enfants.models import Enfant, Parent, Staff

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'nom', 'prenom', 'telephone', 'email', 'adresse']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'nom', 'prenom', 'role', 'telephone', 'email']

class EnfantSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all())
    educateur = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Enfant
        fields = [
            'id', 'nom', 'prenom', 'date_naissance', 'sexe', 
            'parent', 'educateur', 'groupe', 'date_inscription', 
            'allergies', 'remarques_medicales'
        ]