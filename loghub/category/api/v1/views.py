from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from . import serializers
from rest_framework import permissions as drf_permissions
from . import permissions
from category import models
from utils.permissions import IsOwnerOrAdminPermission

class CreateCategoryDetail(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = serializers.CategoryDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateCategoryDetail(mixins.UpdateModelMixin, GenericAPIView):
    queryset = models.CategoryDetail.objects.all()
    serializer_class = serializers.CategoryDetailSerializer
    permission_classes = [
        drf_permissions.IsAuthenticated,
        permissions.IsCategoryDetailOwnerOrAdmin,
    ]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class UpdateCategoryView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [drf_permissions.IsAuthenticated, IsOwnerOrAdminPermission]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)