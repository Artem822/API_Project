from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("Account/<int:id>/", HistoryAccountView.as_view()),
    path("<int:id>/", HistoryByIdView.as_view()),
    path("", HistoryView.as_view())
]