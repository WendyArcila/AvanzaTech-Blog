
from rest_framework import permissions


class AllowPublicEdit(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return True
        if request.user.is_authenticated:
            return True
