from rest_framework import permissions


class IsOwnerOrAdminPermission(permissions.BasePermission):
    """
    Object-level permission to allow access only to the owner of the object
    or admin users. Assumes the model instance has an 'id' attribute.

    - Admin users (is_staff) can always access any object.
    - Active non-admin users can only access their own object.
    - Inactive users are denied access to any object.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if not request.user.is_active:
            return False

        return obj.id == request.user.id
