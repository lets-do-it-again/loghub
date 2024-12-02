from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.api.v1.views import UserUpdateView, UserProfileView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('api/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path("api/update/profile", UserUpdateView.as_view(), name="update-user"),
]
