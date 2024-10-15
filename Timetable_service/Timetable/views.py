from rest_framework import views, response, generics, permissions
from api.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers

class TimetableView(views.APIView):
    
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
    
class TimetableUpdateView(views.APIView): 
    
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
        timetable.id_room=Room.objects.get(room=request.data["room"])
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
    
class TimetableViewDoctor(views.APIView):
    def delete(self, request, id):
        timetable = TimeTable.objects.get(doctorId=id)
        timetable.delete()
        return response.Response({"Записи успешно удалены!"})
    
    def get(self, request, id):
        timetable = TimeTable.objects.get(doctorId=id)
        return response.Response({"from":timetable.date_from,
                                  "to":timetable.date_to})

class TimetableViewHospital(views.APIView):
    
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
        
class AppointmentView(views.APIView):

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

class AppointmentViewDelete(views.APIView):
    def delete(self, request, id):
        appointment = Appointment.objects.get(pk=id)
        appointment.delete()
        return response.Response("Запись успешно удалена")
            