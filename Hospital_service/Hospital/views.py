from rest_framework import views, response, generics, permissions
from api.models import *
from .serializers import *
class HospitalView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = HospitalIdSerializer
    queryset = Hospital.objects.all()
    
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
        return response.Response("Больница успешно добавлена")

class HospitaIdView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = HospitalIdSerializer
    queryset = Hospital.objects.all()
    
    def get(self, request, id):
        obj = Hospital.objects.get(id=id)
        rooms=[]        
        for room in obj.rooms.all().values_list('room'):
            rooms.append(room[0])
        return response.Response({
            "name": str(obj.name),
            "address": str(obj.address),
            "contactPhone": str(obj.contactPhone),
            "rooms": rooms
        })
    
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
 
class RoomsView(generics.GenericAPIView):   
    serializer_class = RoomsSerializer
    queryset = Hospital.objects.all()
    def get(self, request, id):
        obj = Hospital.objects.get(id=id)
        serializer = RoomsSerializer(obj)
        return response.Response(serializer.data)
        

