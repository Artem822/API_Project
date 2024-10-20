from rest_framework import serializers
from api.models import *

class GetDoctorsSerializer(serializers.Serializer):
    nameFilter = serializers.CharField(max_length=100)
    From = serializers.IntegerField()
    count = serializers.IntegerField()