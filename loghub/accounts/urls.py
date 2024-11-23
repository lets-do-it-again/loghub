from django.urls import path

from .api.v1.views import UpdateUserView, UserDetailView
from .views import ProfileView

urlpatterns = [
    path('user/<str:username>/', UserDetailView.as_view(), name='user_profile'),
    path("update-user/", UpdateUserView.as_view(), name="update-user"),
]
