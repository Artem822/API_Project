
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("Hospital/", include("Hospital.urls"))
]
