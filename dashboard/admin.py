from django.contrib import admin


class DashboardSite(admin.AdminSite):
    """Personnalisation du site admin"""
    site_header = "Gestion de Garderie - Administration"
    site_title = "Admin Garderie"
    index_title = "Tableau de bord"
