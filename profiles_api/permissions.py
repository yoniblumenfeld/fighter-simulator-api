from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile or admin"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id == obj.id or request.user.is_staff

class UpdateOwnFighter(permissions.BasePermission):
    """Allow users to edit their own fighter"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own fighter or admin"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id == obj.user_profile.id or request.user.is_staff