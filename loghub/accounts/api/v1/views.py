from rest_framework.generics import GenericAPIView
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrAdminPermission, IsAdminOrUnAuthenticated

User = get_user_model()


class UserDetailView(mixins.RetrieveModelMixin, GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminPermission]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return serializers.BasicUserDetailSerializer
        return serializers.AdminUserDetailSerializer


class UserListView(mixins.ListModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.AdminUserListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BasicUserCreateView(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [IsAdminOrUnAuthenticated]
    serializer_class = serializers.BasicUserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdminUserCreateView(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.AdminUserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = serializers.BasicUserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
