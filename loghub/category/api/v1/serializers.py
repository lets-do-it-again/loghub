from rest_framework import serializers
from category import models


class CreateCategoryDetailSerializer(serializers.ModelSerializer):

    parent = serializers.PrimaryKeyRelatedField(
        required=False, queryset=models.CategoryDetail.objects.all()
    )

    class Meta:
        model = models.CategoryDetail
        fields = ["parent", "image", "title", "slug", "description"]

    def create(self, validated_data):
        parent = validated_data.get("parent")
        is_root = True
        user = self.context.get("request").user

        if parent:
            is_root = False

        # create category detail and handle the is_root
        category_detail_object = super().create(validated_data)
        category_detail_object.is_root = is_root
        category_detail_object.save()

        # create category
        category_object = models.Category.objects.create(
            user=user, category_detail=category_detail_object
        )

        # create category permission
        models.CategoryPermission.objects.create(category=category_object)

        return category_detail_object




class UpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["title","description"]
    

