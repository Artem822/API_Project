from django.shortcuts import render
from rest_framework import views, response, generics, permissions
from api.models import User
from .serializers import *
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

#SECTION - Регистрация пользователей и получение токенов

#LINK: POST /api/Authentication/SignUp/
class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    def post(self, request):
        """
        ### Регистрация нового аккаунта
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string",
            "password": "string"
        }
        ```
    """   
        user = User.objects.create(
            lastName=request.data['lastName'],
             firstName=request.data['firstName'],
             username=request.data['username']
            )
        user.set_password(request.data['password'])
        user.save()
        
        return response.Response("Пользователь успешно создан")

#LINK: Get /api/Authentication/Validate/    
class ValidateTokenAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get(self, request):
        """
        ### Интроспекция токена
        **body:**
        ```
        {
            "accessToken": "string"
        }
        ```
        """
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            return response.Response({"accessToken": f"{token}"})
        except Exception as e:
            return response.Response(f"Токен не активен: {str(e)}")  

#LINK: POST /api/Authentication/Refresh/
class ResetTokenAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        """
        ### Выход из аккаунта
        """
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        user = request.user
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return response.Response(data={
            f"{user}": "Успешно вышел"
        })