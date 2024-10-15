from api.models import User
from rest_framework import serializers, response

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']
        
class SignUpSerializer(serializers.ModelSerializer):
    lastName = serializers.CharField()
    firstName = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'username', 'password']
    

        
class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
                