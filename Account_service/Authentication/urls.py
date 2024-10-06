from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("SignUp/", SignUpView.as_view()),
    path('SignIn/', TokenObtainPairView.as_view()),
    path('SignOut/', ResetTokenAPIView.as_view()),
    path('Validate/', ValidateTokenAPIView.as_view()),
    path('Refresh/', TokenRefreshView.as_view()),
] 