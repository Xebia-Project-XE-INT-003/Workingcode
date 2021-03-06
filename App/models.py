from django.db import models
from AMS import settings
# Create your models here.
from datetime import date,datetime
import json



class Person(models.Model):
       name=models.CharField(max_length=122, unique=True)
       email=models.CharField(max_length=122, unique=True)
       occupation=models.CharField(max_length=122)
       password=models.CharField(max_length=122)
       is_active = models.BooleanField(default=True)
       is_loggedIn=models.BooleanField(default=False)
       def __str__(self):
            return self.name

       def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Appointment(models.Model):
   name=models.CharField(max_length=122)
   date=models.CharField(max_length=122, default='2000-12-30')
   time=models.CharField(max_length=122, default='9:00 AM')
   urgency=models.CharField(max_length=122)
   apptype=models.CharField(max_length=122,default='upcoming')
   description=models.CharField(max_length=400)
   created_by=models.CharField(default='admin',max_length=122)
   emails=models.CharField(max_length=400, default='admin@gmail.com')
   def __str__(self):
       return self.name

 
