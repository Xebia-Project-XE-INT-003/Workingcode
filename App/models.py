from django.db import models

# Create your models here.


class Appointment(models.Model):
   name=models.CharField(max_length=122)
   date=models.DateField
   createdby=models.CharField(max_length=122)
   description=models.CharField(max_length=400) 