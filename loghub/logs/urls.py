from django.urls import path
from .views import *

urlpatterns = [
    path('', CreateLogView.as_view(), name='create-log'),
    path('update-end-time/', UpdateEndTimeIfNullView.as_view(), name='log-update-end-time'),

]
