from rest_framework import permissions


class IsOwnerOrAdminPermission(permissions.BasePermission):
    """
    Custom permission to grant access to object owners or admin users.

    Rules:
    - Admin users (`is_staff=True`) have access to all objects.
    - Active, non-admin users can only access objects they own.
    - Inactive users (`is_active=False`) are denied access.
    - Assumes the object has a `user` or `id` attribute to check ownership.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if not request.user.is_active:
            return False

        if hasattr(obj, "user"):
            return obj.user == request.user

        return obj.id == request.user.id
