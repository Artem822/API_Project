from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('authentication/', include('Authentication.urls'))
]