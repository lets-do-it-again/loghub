from django.urls import path
from . import views

app_name = "api-v1"


urlpatterns = [
    path(
        "detail/create/",
        views.CreateCategoryDetail.as_view(),
        name="create_category_detail",
    ),
    path(
        "detail/update/<int:pk>/",
        views.UpdateCategoryDetail.as_view(),
        name="update_category_detail",
    ),
    path(
        "update/<int:pk>/", views.UpdateCategoryView.as_view(), name="update_category"
    ),
    path(
        "permission/update/<int:pk>/",
        views.UpdateCategoryPermission.as_view(),
        name="update_category_permission",
    ),
    path(
        "detail/<int:pk>/",
        views.CategoryDetailReportView.as_view(),
        name="category_report",
    ),
]
