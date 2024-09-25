from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .funcs.usefull_funcs import *
from .models import Hospital




class HospitalsAPIView(APIView):
    def get(self, request, id = False):

        if id:
            response = get_info_by_id(request=request, id=id)
            return response
        
        else:
            response = get_all(request=request)
            return response
        
    def put(self, request, id):

        response = update_hospital_by_id(request=request, id=id)

        return response

    def post(self, request):

        response = hospital_create(request=request)

        return response

    def delete(self, request, id):

        response = delete_hospital_by_id(request=request, id=id)

        return response


class RoomsByIdAPIVIew(APIView):
    def get(self, request, id):
        hospital = Hospital.objects.get(pk=id)
        rooms = get_rooms(hospital=hospital)

        return Response({
            "rooms": rooms
        })
    