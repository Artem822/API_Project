from rest_framework import serializers
from api.models import *


class HistorySerializer(serializers.ModelSerializer):

    room = serializers.CharField(max_length=100)

    class Meta:
        model = History
        fields = ['date', 'pacientId', 'hospitalId', 'doctorId', 'room', 'data']
        


class HistoryAccountByIdSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']
    
    def get_roles(self, obj):
        role_list = []
        user = obj
        try:
            for role in user.roles.all():
                role_list.append(role.role)
            return role_list

        except:
            return []
        