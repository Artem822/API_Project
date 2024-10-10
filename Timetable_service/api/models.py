from django.db import models
from django.contrib.auth.models import AbstractUser


class Appointment(models.Model):
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.time}"


class Role(models.Model):
    role = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.role


class Room(models.Model):
    room = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.room

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contactPhone = models.CharField(max_length=11)
    rooms = models.ManyToManyField(Room, blank=True)
    timetables = models.ManyToManyField('TimeTable', blank=True)

    def __str__(self) -> str:
        return self.name
    

class User(AbstractUser):
    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    roles = models.ManyToManyField(Role, blank=True, serialize=True)
    appointments = models.ManyToManyField(Appointment, blank=True)

    def __str__(self) -> str:
        return self.username

    
class TimeTable(models.Model):
    hospitalId = models.ForeignKey(Hospital, blank=True, on_delete=models.CASCADE)
    doctorId = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    id_room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.CASCADE)
    appointments = models.ManyToManyField(Appointment, blank=True)

    def __str__(self) -> str:
        return f"from: {self.date_from} to: {self.date_to}"