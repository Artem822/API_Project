from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('Authentication/', include('Authentication.urls')),
    path('Accounts/', include('Accounts.urls'))
]