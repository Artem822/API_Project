from django.db import models



class Room(models.Model):
    room = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.room
    


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contactPhone = models.CharField(max_length=11)
    rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self):
        return self.name
    