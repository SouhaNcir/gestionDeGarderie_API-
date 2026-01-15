from django.urls import path
from . import views

urlpatterns = [
    # Dashboard endpoints
    path('', views.dashboard_overview, name='dashboard_overview'),
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('enfants/', views.enfants_list_admin, name='enfants_list_admin'),
    path('parents/', views.parents_list_admin, name='parents_list_admin'),
    path('staff/', views.staff_list_admin, name='staff_list_admin'),
    path('users/', views.users_list_admin, name='users_list_admin'),
]
