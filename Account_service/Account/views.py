from rest_framework import views, response, generics, permissions
from api.models import User, Role
from .serializers import *
from Authentication.serializers import *

#SECTION - Классы предстваления для микросервиса Аккаунты


#LINK: GET /api/Accounts
#LINK: POST /api/Accounts
class AccountsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    
    def get(self, request):
        """
        ### Получение списка всех аккаунтов
        **body:**
        ```
        {
            "from": "int",
            "count": "int" 
        }
        ```
        """
        obj = User.objects.all()
        serializer = AccountsSerializer(obj)
        return response.Response(serializer.data)
    
    def post(self, request):
        """
        ### Создание администратором нового аккаунта
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string", 
            "password": "string", 
            "roles": [
                "string" 
            ]
        }
        ```
    """
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

# LINK: GET /api/Accounts/Me
class MeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    
    def get(self, request):
        """
        ### Получение данных о текущем аккаунте
        """
        obj = User.objects.get(username=request.user)
        serializer = MeSerializer(obj)
        return response.Response(serializer.data)

# LINK: PUT /api/Accounts/Update
class MeUpdateView(generics.GenericAPIView):
    """
    ### Обновление своего аккаунта
    **body:**
    ```
    {
        "lastName": "string",
        "firstName": "string",
        "password": "string"
    }
     ```
    """
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
    
# LINK: PUT /api/Accounts/{id}
# LINK: DELETE /api/Accounts/{id}
class UserIdView(generics.GenericAPIView):
    serializer_class = AccountsPostSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    def put(self, request, id):
        """
        ### Изменение администратором аккаунта по id
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string", //имя пользователя
            "password": "string", //пароль
            "roles": [
                "string" //массив ролей пользователя
            ]
        }
        ```
        """
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
        """ 
        ### Удаление аккаунта по id
        """
        obj = User.objects.get(id=id)
        obj.delete()
        return response.Response(f'Пользователь успешно удалён.')
    

        
            