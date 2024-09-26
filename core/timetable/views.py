from rest_framework.views import APIView
from .funcs.usefull_funcs import *


# Create your views here.


class TimeTableAPIView(APIView):
    def post(self, request):
        response = create_time_table(request=request)
        return response
    
    def put(self, request, id: int):
        response = update_time_table(request=request, id=id)
        return response
    
    def delete(self, request, id):
        response = delete_time_table(id=id)
        return response
    

class TimeTableByDoctorAPIVIew(APIView):
    def delete(self, request, id):
        response = delete_time_table(id)
        return response