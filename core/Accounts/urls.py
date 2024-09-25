from django.contrib import admin
from django.urls import include, path
from .views import MyUserIdAPIView, MyUserAPIView, MyUserMeAPIView, UpdateMeAPIView

urlpatterns = [
    path('Me/', MyUserMeAPIView.as_view()),
    path("Update/", UpdateMeAPIView.as_view()),
    path('<int:id>/', MyUserIdAPIView.as_view()),
    path('', MyUserAPIView.as_view()),
]
