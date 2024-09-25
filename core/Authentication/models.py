from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
ROLES = ['Admin', 'Manager', 'Doctor', 'User']


class Role(models.Model):
    role = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.role


class User(AbstractUser):

    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    roles = models.ManyToManyField(Role, blank=True, serialize=True)

    def __str__(self) -> str:
        return self.username

