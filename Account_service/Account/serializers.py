from api.models import User
from rest_framework import serializers

class AccountsSerializer(serializers.ModelSerializer):
    From = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["From", "count"]
    def get_From(self, obj):
        return User.objects.all()[0].pk
    
    def get_count(self, obj):
        return len(User.objects.all())

class AccountsPostSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']
class MeSerializer(serializers.ModelSerializer):
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

class UpdateMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['lastName', 'firstName', 'password']