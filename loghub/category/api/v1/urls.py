from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path(
        "create/category/detail/",
        views.CreateCategoryDetailView.as_view(),
        name="create_category_detail",
    ),
    path(
        "update/category/<int:pk>/",
        views.UpdateCategoryView.as_view(),
        name="update-category",
    ),
]
