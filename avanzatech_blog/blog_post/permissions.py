
from rest_framework import permissions

class AllowPublicEdit(permissions.BasePermission):
    """
    Permite a usuarios no autenticados realizar acciones de edición.
    """
    
    def has_permission(self, request, view):
        # Permitir todas las acciones para usuarios no autenticados
        if request.user.is_anonymous:
            return True
        # Para usuarios autenticados, usar la lógica predeterminada
        if request.user.is_authenticated:
            return True 
    def has_object_permission(self, request, view, obj):
        # Permitir todas las acciones para usuarios no autenticados
        if request.user.is_anonymous:
            return True
        # Para usuarios autenticados, usar la lógica predeterminada
        if request.user.is_authenticated:
            return True 