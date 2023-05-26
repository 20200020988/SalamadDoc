from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Appointment(models.Model):
    patient_name=models.CharField(max_length=40,null=True)
    patient_id=models.CharField(max_length=40,null=True)
    doctor_name=models.CharField(max_length=40,null=True)
    doctor_id=models.CharField(max_length=40,null=True)
    patient_email=models.CharField(max_length=40,null=True)
    secretary_id = models.CharField(max_length=40, null=True)  # Add the secretary_id field
    secretary_name=models.CharField(max_length=40,null=True)

    
    # should be appointment_date=models.DateField()
    appointment_date=models.DateField()

    appointment_description=models.TextField(max_length=500)
    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None, editable=False, null=True)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Get the request object from kwargs
        if request:
            self.account = request.user
        super().save(*args, **kwargs)
        
def __str__(self):
    return self.patient_name

class DoctorLinksSecretary(models.Model):
    secretary_id=models.CharField(max_length=40,null=True)
    secretary_name=models.CharField(max_length=40,null=True)
    doctor_name=models.CharField(max_length=40,null=True)
    doctor_id=models.CharField(max_length=40,null=True)

    account = models.ForeignKey(User, on_delete=models.CASCADE, default=None, editable=False, null=True)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Get the request object from kwargs
        if request:
            self.account = request.user
        super().save(*args, **kwargs)
        
def __str__(self):
    return self.patient_name