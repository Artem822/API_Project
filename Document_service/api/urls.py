from drf_spectacular.views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("Documents/", include("Documents.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]