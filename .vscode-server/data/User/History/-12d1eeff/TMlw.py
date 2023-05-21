from django.db import models

# Create your models here.

class Appointment(models.Model):
    patient_name=models.CharField(max_length=40,null=True)
    doctor_name=models.CharField(max_length=40,null=True)
    appointment_date=models.DateField()
    appointment_description=models.TextField(max_length=500)
    
def __str__(self):
    return self.patient_name