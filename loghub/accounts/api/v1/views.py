from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, get_object_or_404, UpdateAPIView, RetrieveAPIView
from rest_framework import mixins, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from utils.permissions import IsOwnerOrAdminPermission
from . import serializers
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .permissions import  IsAdminOrUnAuthenticated
User = get_user_model()


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'message': 'User registered successfully!',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            user_data = serializers.BasicUserDetailSerializer(user).data
            user_data.pop('phone', None)
        else:
            user_data = serializers.BasicUserDetailSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)


class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BasicUserDetailSerializer

    def get_user(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_user(), data=request.data, partial=True,
                                         context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.SearchUserSerializers

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        username = self.request.query_params.get('username', None)
        if not username:
            raise NotFound(detail="Username query parameter is required.")
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail="No user matches the given username.")