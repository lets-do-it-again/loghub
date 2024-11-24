from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.api.v1.views import UserDetailView, UserUpdateView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<str:username>/', UserDetailView.as_view(), name='user_profile'),
    path("update-user/", UserUpdateView.as_view(), name="update-user"),

]