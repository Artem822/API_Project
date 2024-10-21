from rest_framework import views, response, generics, permissions
from api.models import *
from .serializers import *
from .mypermissions import *

# SECTION - Классы предстваления для микросервиса Document

# LINK: GET /api/History/Account/{id}
class HistoryAccountView(generics.GenericAPIView):
    serializer_class = HistoryAccountByIdSerializer
    queryset = User.objects.all()
    permission_classes = [DoctorOrPacientPermission]
    
    def get(self, request, id):
        """
        ### Получение истории посещений и назначений аккаунта
        **body:**
        ```
        {
            "История(-и): username": []
                "id": int,
                "pacientId": int,
                "hospitalId": int,
                "doctorId": int,
                 "room": "string",
                "date": "dateTime(ISO8601)",
                "data": "string"        
            ]
        }
        ```
    """
        history = []
        user = User.objects.get(pk=id)
        historys = History.objects.filter(pacientId=user)
        for i in range(len(historys)):
            user_history = {
                "id": historys[i].pk,
                "pacientId": historys[i].pacientId.pk,
                "hospitalId": historys[i].hospitalId.pk,
                "doctorId": historys[i].doctorId.pk,
                "room": historys[i].room.room,
                "date": historys[i].date,
                "data": historys[i].data,
            }
            history.append(user_history)
        return response.Response({f"История(-и): {user.username}": history})

# LINK: GET /api/History/{id}
# LINK: PUT /api/History/{id} 
class HistoryByIdView(generics.GenericAPIView):
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [DoctorOrPacientPermission]
        elif request.method == "PUT":
            self.permission_classes = [AdminOrManagerOrDoctorPermission]
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request, id):
        """
        ### Получение подробной информации о посещении и назначениях
        """
        history = History.objects.get(pk=id)
        serializer = HistorySerializer(history)
        return response.Response(serializer.data)
    
    def put(self,request, id):
        """
        ### Обновление истории посещения и назначения
        **body:**
        ```
        {
            "date": "dateTime(ISO8601)",
            "pacientId": int,
            "hospitalId": int,
            "doctorId": int,
            "room": "string",
            "data": "string"
        }
        ```
        """
        history = History.objects.get(pk=id)
        history.pacientId=User.objects.get(pk=request.data['pacientId'])
        history.hospitalId=Hospital.objects.get(pk=request.data['hospitalId'])
        history.doctorId=User.objects.get(pk=request.data['doctorId'])
        history.room=Room.objects.get(room=request.data['room'])
        history.date=request.data['date']
        history.data=request.data['data']
        history.save()
        return response.Response("История обновлена")
        
# LINK: POST /api/History   
class HistoryView(generics.GenericAPIView):
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    permission_classes = [AdminOrManagerOrDoctorPermission]
    
    def post(self,request):
        """
        ### Создание истории посещения и назначения
        **body:**
        ```
        {
            "date": "dateTime(ISO8601)",
            "pacientId": int,
            "hospitalId": int,
            "doctorId": int,
            "room": "string",
            "data": "string"
        }
        ```
        """
        user = User.objects.get(pk=request.data['pacientId'])
        hospital = Hospital.objects.get(pk=request.data['hospitalId'])
        doctor = User.objects.get(pk=request.data['doctorId'])
        room = Room.objects.get(room=request.data['room'])

        history = History.objects.create(
            date=request.data.get('date'),
            pacientId=user,
            hospitalId=hospital,
            doctorId=doctor,
            room=room,
            data=request.data.get('data')
        )

        user.history.add(history)
        user.save()
        return response.Response("История успешно создана")
