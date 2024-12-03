from rest_framework.permissions import BasePermission
from category.models import CategoryPermission, CategoryDetail, Category
from django.shortcuts import get_object_or_404


def get_category_and_check_user(category_detail_pk, user):

    category_detail = get_object_or_404(CategoryDetail, pk=category_detail_pk)
    if user.is_staff:
        return True, category_detail

    category_detail_root = category_detail.get_root() if not category_detail.is_root else category_detail
    category_object = get_object_or_404(Category, category_detail=category_detail_root)

    return category_object.user == user, category_detail





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


class CanModifyCategoryDetailOrAdmin(BasePermission):
    def has_permission(self, request, view):
        category_detail_pk = view.kwargs.get("pk")
        user = request.user

        is_owner_or_admin, _ = get_category_and_check_user(category_detail_pk, user)
        return is_owner_or_admin


class IsCategoryPermissionOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        category_permission_pk = view.kwargs.get("pk")
        user = request.user

        category_permission = get_object_or_404(
            CategoryPermission, pk=category_permission_pk
        )
        if user.is_staff:
            return True

        category = category_permission.User_access_category.all().first()
        return category.user == request.user


class CanViewCategoryDetailOrAdmin(BasePermission):
    def has_permission(self, request, view):
        category_detail_pk = view.kwargs.get("pk")
        keyword = request.data.get("keyword")
        user = request.user

        is_owner_or_admin, category_detail = get_category_and_check_user(category_detail_pk, user)
        if is_owner_or_admin:
            return True

        category_object = Category.objects.get(category_detail=category_detail.get_root())
        category_permission = category_object.User_access_category.first()

        if category_permission.permission_type == "None":
            return False
        if category_permission.permission_type == "Anyone":
            return True
        if category_permission.permission_type in ["Keyword", "Mix"] and category_permission.keyword == keyword:
            return True

        if category_permission.permission_type in ["User", "Mix"]:
            included_queryset = CategoryDetail.objects.filter(
                id__in=category_permission.included_childs
            ).get_descendants(include_self=True)

            excluded_queryset = CategoryDetail.objects.filter(
                id__in=category_permission.excluded_childs
            ).get_descendants(include_self=True)

            return category_detail_pk in included_queryset.exclude(id__in=excluded_queryset).values_list("id", flat=True)

        return False