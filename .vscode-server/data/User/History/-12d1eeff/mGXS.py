from django.db import models

# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name=models.CharField(max_length=40,null=True)
    appointment_date=models.DateField(auto_now=True)
    appointment_description=models.TextField(max_length=500)
    
def __str__(self):
    return self.patient.username