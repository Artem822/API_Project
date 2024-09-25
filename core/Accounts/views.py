from rest_framework.views import APIView
from rest_framework import  permissions
from rest_framework.response import Response
from Authentication.models import User
from Authentication.funcs.usefull_funcs import *



class MyUserIdAPIView(APIView):

    permission_classes = [permissions.IsAdminUser, ]

    def put(self, request, id):

        response = update_user(request=request, id=id)

        return response
    

    def delete(self, request, id):

        response = delete(request=request, id=id)

        return response

class MyUserAPIView(APIView):

    permission_classes = [permissions.IsAdminUser,]

    def get(self, request):

        if User.objects.all():
            return Response({
                "from": User.objects.all()[0].pk,
                "count": len(User.objects.all())
                })
        
        else:
            return Response(data={
                "warning": "Пользователей еще нет"
                })
        


    def post(self, request):   
        response = add_users(request=request)
        return response
    


class MyUserMeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user

        response = get_info(user=user)

        return response
    

class UpdateMeAPIView(APIView):
    def put(self, request):

        response = update_user(request)

        return response