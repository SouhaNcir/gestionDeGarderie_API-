from django.contrib import admin
from django.utils.html import format_html
from .models import Enfant, Parent, Staff


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Admin pour les parents avec filtrage avancé"""
    list_display = ['nom_complet', 'telephone', 'email', 'total_enfants', 'date_registered']
    list_filter = ['nom', 'prenom']
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'telephone', 'email')
        }),
        ('Adresse', {
            'fields': ('adresse',)
        }),
    )
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet.short_description = "Nom complet"
    
    def total_enfants(self, obj):
        count = obj.enfant_set.count()
        color = 'green' if count > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            count
        )
    total_enfants.short_description = "Enfants"
    
    def date_registered(self, obj):
        # Afficher la date du premier enfant enregistré
        first_child = obj.enfant_set.first()
        return first_child.date_inscription if first_child else "Aucun enfant"
    date_registered.short_description = "Depuis"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """Admin pour le personnel avec filtrage par rôle"""
    list_display = ['nom_complet', 'role_badge', 'telephone', 'email', 'enfants_assignes']
    list_filter = ['role', 'nom', 'prenom']
    search_fields = ['nom', 'prenom', 'email', 'telephone', 'role']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Rôle', {
            'fields': ('role',)
        }),
    )
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet.short_description = "Nom complet"
    
    def role_badge(self, obj):
        colors = {
            'Directeur': '#FF6B6B',
            'Éducateur': '#4ECDC4',
            'Assistant': '#45B7D1',
            'Autre': '#95A5A6'
        }
        color = colors.get(obj.role, '#95A5A6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.role
        )
    role_badge.short_description = "Rôle"
    
    def enfants_assignes(self, obj):
        count = obj.enfant_set.count()
        return format_html(
            '<span style="background-color: #E8F8F5; color: #27AE60; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            count
        )
    enfants_assignes.short_description = "Enfants assignés"


@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    """Admin pour les enfants avec informations détaillées"""
    list_display = ['nom_complet', 'sexe_badge', 'groupe_badge', 'parent_link', 'educateur_link', 'date_inscription', 'actions_button']
    list_filter = ['sexe', 'groupe', 'date_inscription', 'parent']
    search_fields = ['nom', 'prenom', 'parent__nom', 'parent__prenom']
    date_hierarchy = 'date_inscription'
    readonly_fields = ['date_inscription', 'parent_link', 'educateur_link']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'sexe')
        }),
        ('Inscription', {
            'fields': ('groupe', 'parent', 'educateur', 'date_inscription')
        }),
        ('Santé', {
            'fields': ('allergies', 'remarques_medicales'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_enfants_action', 'marquer_allergies']
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet.short_description = "Nom complet"
    
    def sexe_badge(self, obj):
        if obj.sexe == 'M':
            return format_html('<span style="color: #3498DB;">♂ Masculin</span>')
        else:
            return format_html('<span style="color: #E74C3C;">♀ Féminin</span>')
    sexe_badge.short_description = "Sexe"
    
    def groupe_badge(self, obj):
        colors = {
            'Groupe A': '#3498DB',
            'Groupe B': '#2ECC71',
            'Groupe C': '#F39C12',
            'Groupe D': '#E74C3C',
        }
        color = colors.get(obj.groupe, '#95A5A6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.groupe
        )
    groupe_badge.short_description = "Groupe"
    
    def parent_link(self, obj):
        if obj.parent:
            return format_html(
                '<a href="/admin/enfants/parent/{}/change/">{} {}</a>',
                obj.parent.id,
                obj.parent.prenom,
                obj.parent.nom
            )
        return "Non assigné"
    parent_link.short_description = "Parent"
    
    def educateur_link(self, obj):
        if obj.educateur:
            return format_html(
                '<a href="/admin/enfants/staff/{}/change/">{} {}</a>',
                obj.educateur.id,
                obj.educateur.prenom,
                obj.educateur.nom
            )
        return "Non assigné"
    educateur_link.short_description = "Éducateur"
    
    def actions_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/enfants/enfant/{}/change/">Voir</a>',
            obj.id
        )
    actions_button.short_description = "Actions"
    
    def export_enfants_action(self, request, queryset):
        """Action pour exporter les enfants sélectionnés"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enfants_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Nom', 'Prénom', 'Date de naissance', 'Sexe', 'Groupe', 'Parent', 'Éducateur'])
        
        for enfant in queryset:
            writer.writerow([
                enfant.nom,
                enfant.prenom,
                enfant.date_naissance,
                enfant.get_sexe_display(),
                enfant.groupe,
                f"{enfant.parent.prenom} {enfant.parent.nom}" if enfant.parent else "N/A",
                f"{enfant.educateur.prenom} {enfant.educateur.nom}" if enfant.educateur else "N/A",
            ])
        
        return response
    export_enfants_action.short_description = "Exporter les enfants sélectionnés en CSV"
    
    def marquer_allergies(self, request, queryset):
        """Action pour marquer les enfants avec allergies"""
        updated = queryset.filter(allergies__isnull=False).exclude(allergies='').count()
        self.message_user(request, f'{updated} enfant(s) avec allergies')
    marquer_allergies.short_description = "Afficher les enfants avec allergies"

