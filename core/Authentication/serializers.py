from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'username', 'password']