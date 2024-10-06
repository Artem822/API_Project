from rest_framework import views, response, generics, permissions
from Authentication.models import User, Role
from Authentication.serializers import *
from Account.serializers import *

class DoctrosView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        role = Role.objects.filter(role='Doctor')
        filter_users = User.objects.filter(roles__in=role)
        user = filter_users[0]
        return response.Response({"nameFilter": f"{user.lastName} {user.firstName}",
                "from": user.pk,
                "count": len(filter_users)})
        
class DoctrosIdView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, id):
        user = User.objects.get(pk=id)
        serializer = MeSerializer(user)
        return response.Response(serializer.data)
