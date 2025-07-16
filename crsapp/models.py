from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Roles(models.TextChoices):
    Admin = 'Admin', _('Admin')
    Sheha = 'Sheha', _('Sheha')
    Doctor = 'Doctor', _('Doctor')
    HealthSupervisor = 'HealthSupervisor', _('HealthSupervisor')

class Conditions(models.TextChoices):
    Normal = 'Normal', _('Normal')
    Severe = 'Severe', _('Severe')  

class Status(models.TextChoices):
    Recovered = 'Recovered', _('Recovered')
    Dead = 'Dead', _('Dead')
    Alive = 'Alive', _('Alive')

class Gender(models.TextChoices):
    Male = 'Male', _('Male')
    Female = 'Female', _('Female')



class User(AbstractUser):
    email = models.EmailField(max_length=254,unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices)



    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"



class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'



class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'



class Street(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    location = models.PointField()

    def __str__(self):
        return f'{self.name}'
    


class Sheha(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": Roles.Sheha})   
    street = models.ForeignKey(Street, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'




class HealthCenter(models.Model):
    name = models.CharField(max_length=100)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
    



class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": Roles.Doctor})
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=8, choices=Gender.choices)
    condition = models.CharField(max_length=10, choices=Conditions.choices)
    status = models.CharField(max_length=10, choices=Status.choices)
    phone = models.CharField(max_length=15, null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    



class CaseReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='casereport')
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE, related_name='casereport')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='casereport')
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f' A report from {self.date} for {self.patient.first_name} {self.patient.last_name}'

    class Meta:
        unique_together = ('patient',)


    