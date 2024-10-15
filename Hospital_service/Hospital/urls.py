from django.urls import path
from .views import *

urlpatterns = [
    path('', HospitalView.as_view()),
    path("<int:id>/", HospitaIdView.as_view()),
    path("<int:id>/Rooms/", RoomsView.as_view()),
]
