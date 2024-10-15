from rest_framework import views, response, generics, permissions
from api.models import *
from .serializers import *

class HistoryAccountView(generics.GenericAPIView):
    serializer_class = HistoryAccountByIdSerializer
    queryset = User.objects.all()
    
    def get(self, request, id):
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

class HistoryByIdView(generics.GenericAPIView):
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    
    def get(self,request, id):
        history = History.objects.get(pk=id)
        serializer = HistorySerializer(history)
        return response.Response(serializer.data)
    
    def put(self,request, id):
        history = History.objects.get(pk=id)
        history.pacientId=User.objects.get(pk=request.data['pacientId'])
        history.hospitalId=Hospital.objects.get(pk=request.data['hospitalId'])
        history.doctorId=User.objects.get(pk=request.data['doctorId'])
        history.room=Room.objects.get(room=request.data['room'])
        history.date=request.data['date']
        history.data=request.data['data']
        history.save()
        return response.Response("История обновлена")
        
    
class HistoryView(generics.GenericAPIView):
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    
    def post(self,request):
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
