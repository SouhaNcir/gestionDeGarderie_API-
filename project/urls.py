from django.contrib import admin
from django.urls import path, include
import enfants.views as views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('enfants', views.viwsets_enfant)
router.register('parents', views.viwsets_parent)
router.register('staffs', views.viwsets_staff)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentification
    path('auth/', include('accounts.urls')),
    
    # Dashboard API
    path('api/dashboard/', include('dashboard.urls')),
    
    # API REST
    path('api/', include(router.urls)),
    
    # Routes FBV (à conserver pour la compatibilité)
    path('rest/fbv/enfants/', views.FBV_list),
    path('rest/fbv/enfants/<int:pk>/', views.FBV_pk),
    path('rest/cbv/enfants/', views.CBV_List.as_view()),
    path('rest/cbv/enfants/<int:pk>/', views.CBV_Pk.as_view()),
    path('rest/mixins/enfants/', views.mixins_list.as_view()),
    path('rest/mixins/enfants/<int:pk>/', views.mixins_pk.as_view()),
    path('rest/generics/enfants/', views.generics_list.as_view()),
    path('rest/generics/enfants/<int:pk>/', views.generics_pk.as_view()),
    
    # Routes utilitaires
    path('fbv/findparent/', views.find_parent),
    path('fbv/newenfant/', views.new_enfant),
]

