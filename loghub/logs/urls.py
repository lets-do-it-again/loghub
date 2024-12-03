from django.urls import path
from .views import *

urlpatterns = [
    path('', CreateLogView.as_view(), name='create-log'),
    path('update-end-time/', UpdateEndTimeView.as_view(), name='log-update-end-time'),
    path('search/', LogSearchView.as_view(), name='log-search'),
    path('<int:log_id>/add-source/', AddSourceToLogView.as_view(), name='add-source-to-log'),
]
