from django.shortcuts import render
from rest_framework import views, response, generics, permissions
from api.models import User
from .serializers import *
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    def post(self, request):

        user = User.objects.create(
            lastName=request.data['lastName'],
             firstName=request.data['firstName'],
             username=request.data['username']
            )
        user.set_password(request.data['password'])
        user.save()
        
        return response.Response("Пользователь успешно создан")
    
class ValidateTokenAPIView(views.APIView):
    def get(self, request):
        return response.Response({"accessToken": f"{request.user.access_token}"})    

class ResetTokenAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request):
        
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        user = request.user
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return response.Response(data={
            f"{user}": "Успешно вышел"
        })