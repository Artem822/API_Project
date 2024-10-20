from django.shortcuts import render
from rest_framework import views, response, generics, permissions
from api.models import User
from .serializers import *
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

#SECTION - Регистрация пользователей и получение токенов

class SignUpView(generics.CreateAPIView):
    """
    #LINK: POST /api/Authentication/SignUp/
    """
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    def post(self, request):

        user = User.objects.create(
            lastName=request.data['lastName'],
             firstName=request.data['firstName'],
             username=request.data['username']
            )
        user.set_password(request.data['password'])
        user.save()
        
        return response.Response("Пользователь успешно создан")
    
class ValidateTokenAPIView(generics.GenericAPIView):
    """
    #LINK: Get /api/Authentication/Validate/
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get(self, request):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            return response.Response({"accessToken": f"{token}"})
        except Exception as e:
            return response.Response(f"Токен не активен: {str(e)}")  

class ResetTokenAPIView(generics.GenericAPIView):
    """
    #LINK: POST /api/Authentication/Refresh/
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request):
        
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        user = request.user
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return response.Response(data={
            f"{user}": "Успешно вышел"
        })