from rest_framework import serializers
from api.models import *


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['time']
        


class MyUserTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['date_from', 'date_to']
        


class TimeTableSerializer(serializers.ModelSerializer):

    room = serializers.CharField(max_length=100)

    class Meta:
        model = TimeTable
        fields = ['hospitalId', 'doctorId', 'date_from', 'date_to', 'room']
        