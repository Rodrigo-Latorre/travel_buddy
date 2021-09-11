import datetime
from datetime import date
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombreporfavor"

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres"

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors
class TravelsManager(models.Manager):
    def validador_viaje(self, postData):
        errors = {}

        if len(postData['destination']) < 2:
            errors['destination_len'] = "Destino debe tener al menos 2 caracteres de largo"
        if datetime.datetime.strptime(postData['starttrip'], "%Y-%m-%d").date() <= datetime.date.today():
            errors['wrong_starttrip'] = "Fecha de inicio debe ser futura"
        if datetime.datetime.strptime(postData['endtrip'], "%Y-%m-%d").date() <= datetime.datetime.strptime(postData['starttrip'], "%Y-%m-%d").date():
            errors['wrong_endtrip'] = "Fecha término de viaje no puede ser anterior a la de inicio"
        if len(postData['plantrip']) < 2:
            errors['plan_len'] = "Debe tener un plan para el viaje"

        return errors

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Travels(models.Model):
    destination = models.CharField(max_length=100)
    starttrip = models.DateField()
    endtrip = models.DateField()
    plan = models.TextField()
    planner = models.ForeignKey(User, related_name="travel", on_delete = models.CASCADE)
    joined = models.ManyToManyField(User, related_name="other_travel")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelsManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
