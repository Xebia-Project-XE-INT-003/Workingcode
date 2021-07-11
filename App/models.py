from django.db import models

# Create your models here.


class Appointment(models.Model):
   name=models.CharField(max_length=122)
   date=models.DateField
   time=models.TimeField
   urgency=models.CharField(max_length=122)
   description=models.CharField(max_length=400)
   def __str__(self):
        return self.name

 
class Person(models.Model):
       name=models.CharField(max_length=122)
       email=models.CharField(max_length=122)
       occupation=models.CharField(max_length=122)
       password=models.CharField(max_length=122)
       is_active = models.BooleanField(default=True)
       is_loggedIn=models.BooleanField(default=False)
       def __str__(self):
            return self.name

