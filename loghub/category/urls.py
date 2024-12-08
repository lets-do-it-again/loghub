from django.urls import path, include

app_name = "category"
urlpatterns = [
    path("", include("category.api.v1.urls"))
    ]
