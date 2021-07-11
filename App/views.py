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

        print(passw)
        print(reenter)

        if reenter!=passw:
            print("Hello")
            return render(request, 'register.html')
        
        try:
            person=Person(name=name,email=email,password=passw,occupation=occupation)
            print("person")
            print(person)

            # if person.is_valid():
            print("Save")
            person.save() 
            return redirect("/loginUser")   
            

        except:
            print("Except")
            return render(request, 'register.html')

    return render(request, 'register.html')

def loginUser(request):
    if request.method=="POST":
        email=request.POST.get('email','')
        passw=request.POST.get('password','')

        try:
            person = Person.objects.get(email=email, password=passw)
            print(email)
            print(passw)
            print(person)
            return redirect("/contact")
            person.is_loggedIn=True
            person.save()
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
        
        name=request.POST.get('name'),
        date=request.POST.get('date'),
        time=request.POST.get('time'),
        urgency=request.POST.get('urgency'),
        description=request.POST.get('description')

        appointment=Appointment(name=name,date=date,time=time,urgency=urgency,description=description)

        if appointment.is_valid():
            appointment.save()
            # return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
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
        book_sel = Appointment.objects.get(id = app_id)
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
    return render(request,'appointments.html')


#show appointments
def showAppointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html')


#show appointments
# def showAppointments(request, time):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments.html')

