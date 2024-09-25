from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .funcs.usefull_funcs import *

class SignUpAPIView(APIView):
    def post(self, request):

        response = add_users(request)

        return response


