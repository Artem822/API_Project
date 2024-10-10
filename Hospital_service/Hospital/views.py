from rest_framework import views, response, generics, permissions
from api.models import *
from .serializers import *
class HospitalView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):        
        obj = Hospital.objects.all()
        serializer = HospitalSerializer(obj)
        return response.Response(serializer.data)
    
    def post(self, request):
        hospital = Hospital.objects.create(
            name=request.data["name"],
            address=request.data["address"],
            contactPhone=request.data['contactPhone'],
        )
        for new_room in request.data["rooms"]:
            try:
                Room.objects.get(room=new_room)
            except:
                room = Room.objects.create(room=new_room)
                room.save()
        rooms = list(Room.objects.filter(room__in=request.data['rooms']))
        hospital.rooms.set(rooms)
        hospital.save()
        return response.Response("W")

class HospitaIdView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, id):
        obj = Hospital.objects.get(id=id)
        serializer = HospitalIdSerializer(obj)
        return response.Response(serializer.data)
    
    def put(self, request, id):
        obj = Hospital.objects.get(id=id)
        obj.name=request.data["name"]
        obj.address=request.data["address"]
        obj.contactPhone=request.data["contactPhone"]
        try:
            rooms = list(Room.objects.filter(room__in=request.data['rooms']))
            obj.rooms.set(rooms)
            
        except:
            pass
        obj.save()
        return response.Response(f'Больница {obj.name} успешна обновлена.')
    
    def delete(self, request, id):
        obj = Hospital.objects.get(id=id)
        obj.delete()
        return response.Response(f'Больница {obj.name} успешна удалена.')
 
class RoomsView(views.APIView):   
    def get(self, request, id):
        obj = Hospital.objects.get(id=id)
        serializer = RoomsSerializer(obj)
        return response.Response(serializer.data)
        

