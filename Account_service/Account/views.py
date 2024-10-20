from rest_framework import views, response, generics, permissions
from api.models import User, Role
from .serializers import *
from Authentication.serializers import *



class AccountsView(generics.GenericAPIView):

    permission_classes = (permissions.IsAdminUser, )
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    
    def get(self, request):
        obj = User.objects.all()
        serializer = AccountsSerializer(obj)
        return response.Response(serializer.data)
    
    def post(self, request):
        user = User.objects.create(
             lastName=request.data['lastName'],
             firstName=request.data['firstName'],
             username=request.data['username']
             )
        user.set_password(request.data['password'])
        try:
            roles = list(Role.objects.filter(role__in=request.data['roles']))
            user.roles.set(roles)
            if "Admin" in request.data['roles']:
                user.is_staff = True
                user.is_superuser = True
                user.save()
        except:
            pass
        user.save()
        return response.Response(f"{user.username} успешно создан.")


class MeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    
    def get(self, request):
        obj = User.objects.get(username=request.user)
        serializer = MeSerializer(obj)
        return response.Response(serializer.data)

class MeUpdateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    def put(self, request):
        obj = User.objects.get(username=request.user)
        obj.lastName=request.data['lastName']
        obj.firstName=request.data['firstName']
        obj.set_password(request.data["password"])
        obj.save()
        return response.Response(f'{obj.username} успешно обновлён.')

class UserIdView(generics.GenericAPIView):
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    def put(self, request, id):
        obj = User.objects.get(id=id)
        obj.lastName=request.data['lastName']
        obj.firstName=request.data['firstName']
        obj.set_password(request.data["password"])
        try:
            roles = list(Role.objects.filter(role__in=request.data['roles']))
            obj.roles.set(roles)
            if "Admin" in request.data['roles']:
                obj.is_staff = True
                obj.is_superuser = True
        except:
            pass
        obj.save()
        return response.Response(f'{obj.username} успешно обновлён.')
    
    def delete(self, request, id):
        obj = User.objects.get(id=id)
        obj.delete()
        return response.Response(f'Пользователь успешно удалён.')
    

        
            