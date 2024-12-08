from rest_framework import permissions





class IsAdminOrUnAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return False
        
        return True