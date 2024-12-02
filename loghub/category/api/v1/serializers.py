from rest_framework import serializers
from category import models


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