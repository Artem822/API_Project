from rest_framework import views, response, generics, permissions
from api.models import *
from .serializers import *

# SECTION - Классы предстваления для микросервиса Hospital

# LINK: GET /api/Hospitals
# LINK: POST /api/Hospitals
class HospitalView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = HospitalIdSerializer
    queryset = Hospital.objects.all()
    
    def get(self, request):    
        """
        ### Получение списка больниц
        **body:**
        ```
        {
            "from": "int", 
            "count": "int" 
        }
        ```
        """    
        obj = Hospital.objects.all()
        serializer = HospitalSerializer(obj)
        return response.Response(serializer.data)
    
    def post(self, request):
        """
        ### Создание записи о новой больнице
        **body:**
        ```
        {
            "name": "string",
            "address": "string",
            "contactPhone": "string",
            "rooms": [
                "string"
            ]
        }
        ```
        """
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
    
#LINK - GET /api/Hospitals/{id}
#LINK - Update /api/Hospitals/{id}
#LINK - DELETE /api/Hospitals/{id}
class HospitaIdView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = HospitalIdSerializer
    queryset = Hospital.objects.all()
    
    def get(self, request, id):
        """
        ### Получение информации о больнице по Id
        """
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
        """     
        ### Изменение информации о больнице по Id
        **body:**
        ```
        {
            "name": "string",
            "address": "string",
            "contactPhone": "string",
            "rooms": [
                "string"
            ]
        }
        ```
    """
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
        """
        ### Удаление записи о больнице
        """
        obj = Hospital.objects.get(id=id)
        obj.delete()
        return response.Response(f'Больница {obj.name} успешна удалена.')
    
# LINK: GET /api/Hospitals/{id}/Rooms
class RoomsView(generics.GenericAPIView): 
    serializer_class = RoomsSerializer
    queryset = Hospital.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        """
        ### Получение списка помещений в больнице по Id
        """
        obj = Hospital.objects.get(id=id)
        serializer = RoomsSerializer(obj)
        return response.Response(serializer.data)
        

