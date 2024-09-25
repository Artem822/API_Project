from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('Authentication/', include('Authentication.urls')),
    path('Accounts/', include('Accounts.urls')),
    path('Hospital/', include("hospital.urls")),
    path("Timetable/", include("timetable.urls"))
]