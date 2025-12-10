from django.urls import path
from . import views

app_name = 'scanner'

urlpatterns = [
    path('api/process/', views.scan_receipt, name='scanner'),
]
