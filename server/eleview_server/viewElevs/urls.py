from django.urls import path, include
from rest_framework import urls

app_name = 'viewElevs'
urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]