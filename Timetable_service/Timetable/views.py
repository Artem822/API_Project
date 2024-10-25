from rest_framework import views, response, generics, permissions
from api.models import *
from datetime import datetime
from .serializers import *
from .mypermissions import *

# SECTION - Классы представления для микросервиса Timetable

# LINK: POST /api/Timetable
class TimetableView(generics.GenericAPIView):
    """
    ### Создание новой записи в расписании
        **body:**
        ```
        {
            "hospitalId": int,
            "doctorId": int,
            "date_from": "dateTime(ISO8601)",
            "date_to": "dateTime(ISO8601)",
            "room": "string"
        }
        ```
        **Пример dateTime(ISO8601): "2024-04-25T11:30:00Z"** 
    """
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [AdminOrManagerPermission]
    def post(self, request):

        try:
            
            date_from = datetime.strptime(request.data["from"], '%Y-%m-%dT%H:%M:%SZ')
            date_to = datetime.strptime(request.data["to"], '%Y-%m-%dT%H:%M:%SZ')
            if not ((date_from.minute % 30 == 0) and (date_from.second == 0)):
                return response.Response("Время не подходит под образец.")
            if not ((date_to.minute % 30 == 0) and (date_to.second == 0)):
                return response.Response("Время не подходит под образец.")
    
            if date_from > date_to:
                return response.Response("Время не подходит под образец.")
    
            diff = date_to - date_from
            hours_diff = diff.total_seconds() / 60 ** 2

            if hours_diff >= 12:
                return  response.Response("Время не подходит под образец.")
        except:
            return response.Response("Время не подходит под образец.")
        
        timetable = TimeTable.objects.create(
            hospitalId=Hospital.objects.get(pk=request.data["hospitalId"]),
            doctorId=User.objects.get(pk=request.data["doctorId"]),
            date_from=date_from,
            date_to=date_to,
            id_room=Room.objects.get(room=request.data["room"])
        )
        timetable.save()
        
        hospital = Hospital.objects.get(pk=request.data["hospitalId"])
        hospital.timetables.add(timetable)
        hospital.save()
        room = Room.objects.get(room=request.data["room"])
        room.id_timetable.add(timetable)
        room.save()
        

        return response.Response("Рассписание создано")

# LINK: PUT /api/Timetable/{id}/
# LINK: DELETE /api/Timetable/{id}/
class TimetableUpdateView(generics.GenericAPIView): 
    """
    ### Обновление расписания по Id
        **body:**
        ```
        {
            "hospitalId": int,
            "doctorId": int,
            "from": "dateTime(ISO8601)",
            "to": "dateTime(ISO8601)",
            "room": "string"
        }
        ```
        **Пример dateTime(ISO8601): "2024-04-25T11:30:00Z"**
    
    ### Удаление расписания по Id
    """
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [AdminOrManagerPermission]
    def put(self, request, id):
        timetable = TimeTable.objects.get(pk=id)  
        hospital= Hospital.objects.get(name=timetable.hospitalId)
        hospital.timetables.set("")
        hospital.save()
        
        room = Room.objects.get(room=timetable.id_room)
        room.id_timetable.set("")
        room.save()
        try:  
            
            date_from = datetime.strptime(request.data["from"], '%Y-%m-%dT%H:%M:%SZ')
            date_to = datetime.strptime(request.data["to"], '%Y-%m-%dT%H:%M:%SZ')
            if not ((date_from.minute % 30 == 0) and (date_from.second == 0)):
                return response.Response("Время не подходит под образец.")
            if not ((date_to.minute % 30 == 0) and (date_to.second == 0)):
                return response.Response("Время не подходит под образец.")
    
            if date_from > date_to:
                return response.Response("Время не подходит под образец.")
    
            diff = date_to - date_from
            hours_diff = diff.total_seconds() / 60 ** 2

            if hours_diff >= 12:
                return  response.Response("Время не подходит под образец.")
        except:
            return response.Response("Время не подходит под образец.")

        
        timetable.hospitalId=Hospital.objects.get(pk=request.data["hospitalId"])
        timetable.doctorId=User.objects.get(pk=request.data["doctorId"])
        timetable.date_from=date_from
        timetable.date_to=date_to
        timetable.room=Room.objects.get(room=request.data["room"])
        timetable.save()
        
        hospital = Hospital.objects.get(pk=request.data["hospitalId"])
        hospital.timetables.add(timetable)
        hospital.save()
        
        room = Room.objects.get(room=request.data["room"])
        room.id_timetable.add(timetable)
        room.save()
        return response.Response("Рассписание изменено.")
    
    def delete(self, request, id):
        timetable = TimeTable.objects.get(pk=id)  
        timetable.delete()
        
        return response.Response("Рассписание удалено.")

# LINK - DELETE /api/Timetable/Doctor/{id}/
# LINK - GET /api/Timetable/Doctor/{id}
class TimetableViewDoctor(generics.GenericAPIView):
    """
    ### Получение расписания врача по Id
        **body:**
        {
            "from": "string(ISO8601)",
            "to": "string(ISO8601)"
        }
        **Пример dateTime(ISO8601): "2024-04-25T11:30:00Z"**
        
    ### Удаление записей расписания доктора
    """
    queryset = TimeTable.objects.all()
    serializer_class = MyUserTimeTableSerializer
    def despatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif request.method == 'DELETE':
            self.permission_classes = [AdminOrManagerPermission]
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, id):
        timetable = TimeTable.objects.get(doctorId=id)
        timetable.delete()
        return response.Response({"Записи успешно удалены!"})
    
    def get(self, request, id):
        timetable = TimeTable.objects.get(doctorId=id)
        return response.Response({"from":timetable.date_from,
                                  "to":timetable.date_to})
        
# LINK - DELETE /api/Timetable/Hospital/{id}/
# LINK - GET /api/Timetable/Hospital/{id}/
class TimetableViewHospital(views.APIView):
    """
    ### Удаление записей расписания больницы
    
    ### Получение расписания кабинета больницы
        **body:**
        ```
        {
            "from": "string(ISO8601)",
            "to": "string(ISO8601)"
        }
        ```
        **Пример dateTime(ISO8601): "2024-04-25T11:30:00Z"**
    """
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            self.permission_classes = [AdminOrManagerPermission]
        elif request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().dispatch(request, *args, **kwargs)
    def delete(self, request, id):
        hospital = Hospital.objects.get(pk=id)
        timetable = TimeTable.objects.get(hospitalId=hospital)
        timetable.delete()
        return response.Response("Записи успешно удалены!")
    
    def get(self, request, id):
        hospital = Hospital.objects.get(pk=id)
        timetable = TimeTable.objects.get(hospitalId=hospital)
        return response.Response({"from":timetable.date_from,
                                  "to":timetable.date_to})

#LINK - GET /api/Timetable/Room/{id}/{room}/
class TimeTableByRoomAPIView(views.APIView):
    """
    ### Получение расписания кабинета больницы
        **body:**
        ```
        {
            "from": "string(ISO8601)",
            "to": "string(ISO8601)"
        }
        ```
        **Пример dateTime(ISO8601): "2024-04-25T11:30:00Z"**
    """
    permission_classes = [AdminOrManagerOrDoctorPermission]
    def get(self, request, id, room):
        resp = {}
        room = Room.objects.get(room=room)
        hospital = Hospital.objects.get(pk=id)
        if  room not in hospital.rooms.all():
            return response.Response( f"Комната: {room} не найдена в данной больнице больнице!")
        resp["from:"] = " ".join(str(room.id_timetable).split()[1:3])
        resp["to:"] = " ".join(str(room.id_timetable).split()[4:])
        return response.Response(resp)

#LINK - GET /api/Timetable/{id}/Appointments/ 
#LINK - POST /api/Timetable/{id}/Appointments/    
class AppointmentView(generics.GenericAPIView):
    """ 
    ### Получение свободных талонов на приём
    
    ### Записаться на приём
        **body:**
        ```
        {
            "time": "dateTime(ISO8601)"
        }
        ```
        **Пример dateTime(ISO8601): "2024-04-25T11:30:00Z"**
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        appointments = []
        timetable = TimeTable.objects.get(pk=id)
        for i in range(len(timetable.appointments.all())):
            appointments.append(timetable.appointments.all()[i].time)
        talons = {"Талоны": appointments}
        
        return response.Response(talons)
    
    def post(self, request, id):
        
        timetable = TimeTable.objects.get(pk=id)
        
        appointment = Appointment.objects.create(
            time=request.data['time']
        )
        appointment.save()

        user = User.objects.get(username=request.user)
        user.appointments.add(appointment)
        user.save()

        timetable.appointments.add(appointment)
        timetable.save()
        return response.Response("Запись успешно добавлена")

# LINK: DELETE /api/Appointment/{id}/
class AppointmentViewDelete(views.APIView):
    """
    ### Удалить запись на приём
    """
    permission_classes = [AdminOrManagerOrPacientPermission]
    def delete(self, request, id):
        appointment = Appointment.objects.get(pk=id)
        appointment.delete()
        return response.Response("Запись успешно удалена")
            