from django.shortcuts import render, HttpResponse
from App.models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.template import RequestContext

# def check():


def register(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        passw=request.POST.get('password','')
        reenter=request.POST.get('reenter','')
        occupation=request.POST.get('occupation','')

        if reenter!=passw:
            return render(request, 'register.html')
        
        try:
            person=Person(name=name,email=email,password=passw,occupation=occupation)
           
            # if person.is_valid():
            person.save() 
            return redirect("/loginUser")   
            

        except:
            return render(request, 'register.html')

    return render(request, 'register.html')

def loginUser(request):
    if request.method=="POST":
        email=request.POST.get('email','')
        passw=request.POST.get('password','')

        try:
            person = Person.objects.get(email=email, password=passw)
            person.is_loggedIn=True
            person.is_active=False
            # person.save()
            return redirect("/contact")
            
        except Appointment.DoesNotExist:
                return render(request, 'login.html')

    return render(request, 'login.html')

# def logoutUser(request):
#     logout(request)
#     return redirect("/login")

def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')


#add appointments
def addAppointment(request):
    
    if request.method == 'POST':
        
        name=str(request.POST.get('name')),
        meetdate=str(request.POST.get('date')),
        meettime=str(request.POST.get('time')),
        urgency=str(request.POST.get('urgency')),
        description=str(request.POST.get('description'))

        appointment=Appointment(name=name,date=meetdate,time=meettime,urgency=urgency,description=description)

        print(name)
        print(meetdate)
        print(description)
        print(meettime)
        print(urgency)
        print(appointment)

        print("save")
        appointment.save()
        return redirect('index.html')
        
    else:
        return render(request, 'addAppointment.html')


#delete appointments
def deleteAppointment(request, app_id):
    app_id = int(app_id)
    try:
        appointment = Appointment.objects.get(id = app_id)
    except Appointment.DoesNotExist:
        # return redirect('index')
        appointment.delete()
    # return redirect('index')


#update appointments
def updateAppointment(request, app_id):
    app_id = int(app_id)
    try:
        app_sel = Appointment.objects.get(id = app_id)
    except Appointment.DoesNotExist:
        # return redirect('index')
        print("Not in db")
    
    name=request.POST.get('name'),
    date=request.POST.get('date'),
    time=request.POST.get('time'),
    urgency=request.POST.get('urgency'),
    description=request.POST.get('description')

    appointment=Appointment(name=name,date=date,time=time,urgency=urgency,description=description)

    if appointment.is_valid():
        appointment.save()
        # return redirect('index')
    return render(request,'meetings.html')


#show appointments
def showAppointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'meetings.html')


#show appointments
# def showAppointments(request, time):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments.html')

