from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from App.models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.template import RequestContext
from django.contrib import messages
import time

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
                    
                    
                    temp=i
                    messages.success(request,"Registration Successful!")
                    return render(request,'register.html')
                    # return redirect('/loginUser')     
                except:
                    temp=i
                    messages.error(request,"User already exists, Try to login!")
                    return render(request, 'login.html')
                

        if email_handle!=temp:
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

            # time.sleep(1)
            messages.success(request,"Login successful!")
            return redirect("/addAppointment")
                
        except Person.DoesNotExist:
                messages.warning(request,"User not available!")
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
                        messages.success(request,"Appointment added!")
                        
                        return redirect("/showAppointments")   
                    except:
                        messages.warning(request,"Unable to add appointment, check the fields again!")
                        return redirect(request, "/addAppointment")
                    
    else:
        return redirect("/loginuser")
    return render(request, 'addAppointment.html')

#delete appointments
def deleteAppointment(request,id):
    
    try:
        appointment=Appointment.objects.get(id=id)
        print(appointment)
        appointment.delete()

        messages.success(request,"Appointment deleted!")
        return redirect('/showAppointments')
        
    except Appointment.DoesNotExist:
        # return redirect('index')
        return redirect('/showAppointments')
    
    return redirect('/showAppointments')


#update appointments
def updateAppointment(request, id):

    try:
        appointment = Appointment.objects.get(id = id)

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
                # time.sleep(2)
                return redirect('/showAppointments')

            except:
                messages.warning(request,"Unable to update appointment")
                return redirect('/showAppointments')
            
            

    else: 

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
