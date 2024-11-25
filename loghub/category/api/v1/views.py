from . import serializers
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from utils.permissions import IsOwnerOrAdminPermission
from category import models


class CreateCategoryDetailView(mixins.CreateModelMixin, GenericAPIView):

    serializer_class = serializers.CreateCategoryDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateCategoryView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.UpdateCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminPermission]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
