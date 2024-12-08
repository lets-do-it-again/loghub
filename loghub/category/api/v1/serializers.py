from rest_framework import serializers
from category import models
import uuid
from django.contrib.auth import get_user_model
from django.db.models import Q
from . import validators

User = get_user_model()

class CategoryDetailSerializer(serializers.ModelSerializer):

    parent = serializers.PrimaryKeyRelatedField(
        required=False, queryset=models.CategoryDetail.objects.all()
    )

    class Meta:
        model = models.CategoryDetail
        fields = ["parent", "image", "title", "slug", "is_root", "description"]
        read_only_fields = ["is_root"]

    def create_category_with_permissions(self, user, category_detail_object):

        category_object = models.Category.objects.create(
            user=user, category_detail=category_detail_object
        )

        models.CategoryPermission.objects.create(category=category_object)

        return category_object

    def create(self, validated_data):

        parent = validated_data.get("parent")
        user = self.context.get("request").user
        validated_data["is_root"] = True if parent is None else False
        category_detail_object = super().create(validated_data)
        if parent is None:
            self.create_category_with_permissions(user, category_detail_object)

        return category_detail_object

    def update(self, instance, validated_data):

        parent = validated_data.get("parent")
        user = self.context.get("request").user
        if not parent and not instance.is_root:
            self.create_category_with_permissions(user, instance)
            validated_data["is_root"] = True
        return super().update(instance, validated_data)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["title", "description"]




class CategoryPermissionSerializer(serializers.ModelSerializer):
    generate_keyword = serializers.BooleanField(default=False)
    permission_type = serializers.ChoiceField(
        choices=models.CategoryPermission.PERMISSION_TYPE_CHOICES
    )
    user_identifiers = serializers.ListField(
        child=serializers.CharField(), default=[], write_only=True
    )  # phone,email,username

    included_childs = serializers.ListField(
        child=serializers.IntegerField(), default=[]
    )

    excluded_childs = serializers.ListField(
        child=serializers.IntegerField(), default=[]
    )

    class Meta:
        model = models.CategoryPermission
        fields = [
            "category",
            "included_childs",
            "excluded_childs",
            "keyword",
            "permission_type",
            "generate_keyword",
            "user_identifiers",
            "user_ids",
        ]
        read_only_fields = ["keyword", "user_ids"]
        write_only_fields = ["generate_keyword"]

    def validate(self, attrs):

        validators.validate_permission_type(attrs)

        return super().validate(attrs)

    def update(self, instance, validated_data):
        permission_type = validated_data.get("permission_type")
        generate_keyword = validated_data.pop("generate_keyword", False)

        if permission_type in ["Keyword", "Mix"] and generate_keyword:
            self._generate_new_keyword(validated_data)


        user_identifiers = validated_data.pop("user_identifiers", [])
        validated_data["user_ids"] = self._get_users_id_by_identifiers(user_identifiers)

        return super().update(instance, validated_data)

    def _generate_new_keyword(self, validated_data):
        validated_data["keyword"] = uuid.uuid4()

    def _get_users_id_by_identifiers(self, identifiers):

        users = []
        for identifier in identifiers:
            user = User.objects.filter(
                Q(phone=identifier) | Q(email=identifier) | Q(username=identifier)
            ).first()
            if user:
                if user.id not in users:
                    users.append(user.id)

            else:
                raise serializers.ValidationError(
                    f"User with identifier '{identifier}' not found."
                )

        return users