from rest_framework.permissions import BasePermission
from .models import CategoryPermission

class IsCategoryUser(BasePermission):
    """
    Custom permission to check if the user has access to a specific category.
    """

    def has_permission(self, request, view):
        category_id = request.data.get('category')
        if not category_id:
            return False

        try:
            permission = CategoryPermission.objects.get(category_id=category_id)

            if permission.permission_type == "None":
                return False
            elif permission.permission_type == "User":
                return request.user.id in permission.user_ids
            elif permission.permission_type == "Keyword":
                return request.data.get('Keyword') == permission.keyword
            # Check Mix permission
            else:
                return True
            
        except CategoryPermission.DoesNotExist:
            return False
