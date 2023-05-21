from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    patient_name=models.CharField(max_length=40,null=True)
    doctor_name=models.CharField(max_length=40,null=True)
    
    # should be appointment_date=models.DateField()
    appointment_date=models.DateField(auto_now=True)

    appointment_description=models.TextField(max_length=500)
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    
def __str__(self):
    return self.patient_name