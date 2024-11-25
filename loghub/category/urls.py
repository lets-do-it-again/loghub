from django.urls import path, include

app_name = "category"


urlpatterns = [
    path("api/v1/", include("category.api.v1.urls"))
    ]
