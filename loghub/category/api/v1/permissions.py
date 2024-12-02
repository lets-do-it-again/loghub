from rest_framework.permissions import BasePermission
from category.models import CategoryPermission, CategoryDetail, Category
from django.shortcuts import get_object_or_404


class IsCategoryUser(BasePermission):
    """
    Custom permission to check if the user has access to a specific category.
    """

    def has_permission(self, request, view):
        category_id = request.data.get("category")
        if not category_id:
            return False

        try:
            permission = CategoryPermission.objects.get(category_id=category_id)

            if permission.permission_type == "None":
                return False
            elif permission.permission_type == "User":
                return request.user.id in permission.user_ids
            elif permission.permission_type == "Keyword":
                return request.data.get("Keyword") == permission.keyword
            # Check Mix permission
            else:
                return True

        except CategoryPermission.DoesNotExist:
            return False


class IsCategoryDetailOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        category_detail_pk = view.kwargs.get("pk")

        user = request.user


        category_detail = get_object_or_404(CategoryDetail, pk=category_detail_pk)


        if user.is_staff:
            return True

        category_detail_root = (
            category_detail.get_root()
            if not category_detail.is_root
            else category_detail
        )

        category_object = Category.objects.get(category_detail=category_detail_root)
        return category_object.user == user
