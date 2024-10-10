from rest_framework import serializers
from api.models import *

class HospitalSerializer(serializers.ModelSerializer):
    From = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    class Meta:
        model = Hospital
        fields = ["From", "count"]
    def get_From(self, obj):
        return Hospital.objects.all()[0].pk
    
    def get_count(self, obj):
        return len(Hospital.objects.all())

class HospitalIdSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()
    class Meta:
        model = Hospital
        fields = ["name", "address", "contactPhone", "rooms"]
    
    def get_rooms(self, obj):
        room_list = []
        hospital = Hospital.objects.get(name=obj)
        try:
            for room in hospital.rooms.all():
                room_list.append(room.room)
            return room_list

        except:
            return []

class RoomsSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()
    class Meta:
        model = Hospital
        fields = ["rooms"]
    
    def get_rooms(self, obj):
        room_list = []
        hospital = Hospital.objects.get(name=obj)
        try:
            for room in hospital.rooms.all():
                room_list.append(room.room)
            return room_list

        except:
            return []