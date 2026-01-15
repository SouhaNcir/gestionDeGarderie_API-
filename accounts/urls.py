from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, register, get_current_user,
    change_password, update_profile, logout
)

urlpatterns = [
    # Authentification JWT
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Enregistrement et gestion du profil
    path('register/', register, name='register'),
    path('me/', get_current_user, name='get_current_user'),
    path('me/update/', update_profile, name='update_profile'),
    path('change-password/', change_password, name='change_password'),
    path('logout/', logout, name='logout'),
]
