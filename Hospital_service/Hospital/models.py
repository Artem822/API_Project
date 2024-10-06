from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.role


class User(AbstractUser):
    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    roles = models.ManyToManyField(Role, blank=True, serialize=True)
    
    def __str__(self):
        return self.username
    
class Room(models.Model):
    room = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.room)
    


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contactPhone = models.CharField(max_length=11)
    rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self) -> str:
        return str(self.name)