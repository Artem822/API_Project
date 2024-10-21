from rest_framework import views, response, generics, permissions
from api.models import User, Role
from Authentication.serializers import *
from Account.serializers import *
from .serializers import *

# SECTION - Классы предстваления для Докторов

# LINK: GET /api/Doctors
class DoctrosView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = GetDoctorsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        """
        ### Получение списка докторов
        **body:**
        ```
        {
            "nameFilter": "string" 
            "from": "int" 
            "count": "int"
        }
        ```
        """
        role = Role.objects.filter(role='Doctor')
        filter_users = User.objects.filter(roles__in=role)
        user = filter_users[0]
        return response.Response({"nameFilter": f"{user.lastName} {user.firstName}",
                "from": user.pk,
                "count": len(filter_users)})

# LINK: GET /api/Doctors/{id}     
class DoctrosIdView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        """
        ### Получение информации о докторе по Id
        """
        user = User.objects.get(pk=id)
        serializer = MeSerializer(user)
        return response.Response(serializer.data)
