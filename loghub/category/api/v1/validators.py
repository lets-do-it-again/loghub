from rest_framework import serializers
from category.models import CategoryDetail
from django.shortcuts import get_object_or_404


def validate_none_or_anyone(user_identifiers, generate_keyword):
    if user_identifiers:
        raise serializers.ValidationError(
            {
                "user_identifier": "User identifiers should not be provided when permission_type is 'None' or 'Anyone'."
            }
        )
    if generate_keyword:
        raise serializers.ValidationError(
            {
                "regenerate_keyword": "'generate_keyword' should not be set when permission_type is 'None' or 'Anyone'."
            }
        )


def validate_user_or_mix(user_identifiers):
    if not user_identifiers:
        raise serializers.ValidationError(
            {
                "user_identifier": "User identifiers must be provided for 'User' or 'Mix' permission type."
            }
        )


def validate_category_detail_children(included_children=None, excluded_children=None):
    if included_children:
        for id in included_children:
            get_object_or_404(CategoryDetail, id=id)

    if excluded_children:
        for id in excluded_children:
            get_object_or_404(CategoryDetail, id=id)


def validate_permission_type(attrs):
    permission_type = attrs.get("permission_type")
    user_identifiers = attrs.get("user_identifiers")
   
    generate_keyword = attrs.get("generate_keyword")
    included_children = attrs.get("included_childs")
    excluded_children = attrs.get("excluded_childs")
    if permission_type in ["None", "Anyone"]:
        validate_none_or_anyone(user_identifiers, generate_keyword)
    elif permission_type in ["User", "Mix"]:
        validate_user_or_mix(user_identifiers)

    validate_category_detail_children(included_children, excluded_children)
