from django.urls import path
from . import views


app_name = "api-v1"
urlpatterns = [
    path("list/", views.UserListView.as_view(), name="users-list")
    ]
