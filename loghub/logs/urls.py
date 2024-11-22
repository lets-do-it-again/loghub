from django.urls import path
from .views import CreateLogView

urlpatterns = [
    path('', CreateLogView.as_view(), name='create-log'),
]
