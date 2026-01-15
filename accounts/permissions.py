from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Permission pour permettre aux admins de modifier,
    les autres utilisateurs ne peuvent que lire.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsEducateur(BasePermission):
    """
    Permission pour les éducateurs uniquement.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'educateur'


class IsParent(BasePermission):
    """
    Permission pour les parents uniquement.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'parent'


class IsDirecteur(BasePermission):
    """
    Permission pour les directeurs uniquement.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'directeur'


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission pour permettre aux propriétaires d'objets
    de les éditer uniquement.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsActiveUser(BasePermission):
    """
    Permission pour les utilisateurs actifs uniquement.
    """
    def has_permission(self, request, view):
        return request.user and request.user.profile.is_active if hasattr(request.user, 'profile') else True
