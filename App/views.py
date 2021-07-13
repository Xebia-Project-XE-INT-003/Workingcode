from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from App.models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.template import RequestContext
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import time
from .forms import *


# def check():


def register(request):
    if request.method=="POST":

        emails=['@iCloud.com','@outlook.com','@zoho.con','@aol.com','@yandex.com','@yahoo.com ','@gmail.com','@hotmail.com','@redif.com','@live.com']
        
        name=request.POST.get('name','')
        email=str(request.POST.get('email',''))
        passw=request.POST.get('password','')
        reenter=request.POST.get('reenter','')
        occupation=request.POST.get('occupation','')

        email_handle=str("@"+email.split("@",1)[1])
        temp=None
        for i in emails:
        
            if email_handle==i:

                if reenter!=passw:
                    return render(request, 'register.html')
                
                try:
                    person=Person(name=name,email=email,password=passw,occupation=occupation)
                
                    # if person.is_valid():
                    person.save() 
                    
                    messages.success(request,"Registration Successful!")
                    temp=i
                    #return render(request,'register.html')
                    return render(request,'login.html')   
                    
                except:
                    print("EXCEPT")
                    temp=i
                    messages.error(request,"Wrong email format!")
                    return render(request, 'register.html')

        if email_handle!=temp:
            print("WRONG")
            messages.error(request,"Wrong email format!")
            return render(request, 'register.html')
            
    return render(request, 'register.html')

def loginUser(request):
    if request.method=="POST":
        email=str(request.POST.get('email',''))
        passw=str(request.POST.get('password',''))


        try:
            person = Person.objects.get(email=email, password=passw)

            person.is_loggedIn=True
            person.is_active=False
            person.save()
            person.toJSON()
            request.session['personName']=person.name
            request.session['loggedin']=person.is_loggedIn
            request.session['person']=person.toJSON()
                    # messages.success(request,"Login successful!")
            return redirect("/addAppointment")
                
        except Person.DoesNotExist:
                messages.success(request,"User not available!")
                return render(request, 'register.html')

    return render(request, 'login.html')

def logoutUser(request):
   personname=request.session.get('personName')

   try:
       person=Person.objects.get(name=personname)

       person.is_loggedIn=False

       person.save()

   except:
       return redirect("/loginUser")
   return redirect("/loginUser")

def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')


def addAppointment(request):
    personLogin=request.session.get('loggedin')
    personname=request.session.get('personName')

    if personLogin:

                if request.method=="POST":

                    name=request.POST.get('name','')
                    description=request.POST.get('description','')
                    meetdate=request.POST.get('date','')
                    meettime=request.POST.get('time','')
                    urgency=request.POST.get('urgency','')
                    created_by=personname
                    
                    try:
                        appointment=Appointment(name=name,date=meetdate,time=meettime, description=description, created_by=created_by, urgency=urgency)
                    
                        # if person.is_valid():
                        appointment.save() 
                        return redirect("/showAppointments")   
                        

                    except:
                        return render(request, 'addAppointment.html')

    else:
        return redirect("/loginuser")
    return render(request, 'addAppointment.html')


#add appointments
#  def addAppointment(request):
    
#     personLogin=request.session.get('loggedin')

#     if personLogin:
#         personname=request.session.get('personName')

#         print(personname)

#         if request.method == 'POST':
                    
#                 name=request.POST.get('name',''),
#                 meetdate=request.POST.get('date',''),
#                 meettime=request.POST.get('time',''),
#                 urgency=request.POST.get('urgency',''),
#                 description=request.POST.get('description',''),
#                 created_by=personname

#                 appointment=Appointment(name=name,date=meetdate,time=meettime,urgency=urgency,description=description,created_by=created_by)

#                 print("save")
#                 appointment.save()
#                 print(appointment.id)
#                 request.session['createdby']=appointment.created_by
#                 request.session['urgency']=appointment.urgency
#                 return redirect('showAppointments')
                    
#         else:
#                 return render(request, 'addAppointment.html')

#     else:
#         return redirect('/loginUser')


#delete appointments
def deleteAppointment(request,id):
    # appointment=Appointment.objects.get(id=id)
    # print(appID)
    try:
        appointment=Appointment.objects.get(id=id)
        print(appointment)
        appointment.delete()
    except Appointment.DoesNotExist:
        # return redirect('index')
        return redirect('showAppointments')
    return redirect('showAppointments')


#update appointments
def updateAppointment(request, id):

    try:
        appointment = Appointment.objects.get(id = id)

        # app_form = AppointmentUpdate(request.POST or None, instance =appointment)
        # if app_form.is_valid():
        #     app_form.save()
        #     return redirect('index')
        # return render(request, 'addAppointment.html', {'upload_form':app_form})

        return render(request, 'updateAppointment.html',{
            'appointment':appointment
        })

        name=request.POST.get('name','')
        meetdate=request.POST.get('date',''),
        meettime=request.POST.get('time','')
        urgency=request.POST.get('urgency','')
        description=request.POST.get('description','')

        appointment=Appointment(name=name,date=meetdate,time=meettime, description=description, created_by=created_by, urgency=urgency)

        appointment.save()
        return redirect('/showAppointments')

    except Appointment.DoesNotExist:
        # return redirect('index')
        print("Not in db")
    
    # name=request.POST.get('name'),
    # date=request.POST.get('date'),
    # time=request.POST.get('time'),
    # urgency=request.POST.get('urgency'),
    # description=request.POST.get('description')

    # appointment=Appointment(name=name,date=date,time=time,urgency=urgency,description=description)

    # if appointment.is_valid():
    #     appointment.save()
        # return redirect('index')
    return render(request,'showAppointments.html')

 
def update(request, id):

    if request.method=="POST":

            try:
                appointment = Appointment.objects.get(id = id)

                name=request.POST.get('name','')
                meetdate=request.POST.get('date','')
                meettime=request.POST.get('time','')
                urgency=request.POST.get('urgency','')
                description=request.POST.get('description','')
                created_by=appointment.created_by

                appointment.name=name
                appointment.date=meetdate
                appointment.time=meettime
                appointment.urgency=urgency
                appointment.description=description

                appointment.save()
                
                messages.success(request,"Appointment updated!")
                return redirect('/showAppointments')

            except:
                print("OUT")
                return redirect('/showAppointments')

    else: 
        print("Else")
    print("OUTEST")
    return redirect('/showAppointments')



#show appointments
def showAppointments(request):

    personLogin=request.session.get('loggedin')
    personname=request.session.get('personName')
    appowner=request.session.get('createdby')
    urgency=request.session.get('urgency')

    if personLogin:
        
        # if personname ==appowner:
            print('same owner')

            lows=Appointment.objects.all().filter(urgency="low")

            highs=Appointment.objects.all().filter(urgency="high")

            highnum=highs.count()

            print(highnum)

            lownum=lows.count()
            print(lownum)

            meds=Appointment.objects.all().filter(urgency='medium')

            mednum=meds.count()
            print(mednum)
            # database.collection.find( { qty: { $gt: 4 } } )

            

            appointments = Appointment.objects.all()

            num=appointments.count()
            print(num)
            return render(request, 'showAppointments.html', {
            'lows':lows,
            'highs':highs,
            'meds':meds,
            'appointments':appointments
        })
    else:
        return redirect('/loginUser')
    return render(request,'showAppointments.html')
#show appointments
# def showAppointments(request, time):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments.html')

