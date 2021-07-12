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
            person.save()
            request.session['personName']=person.name
            request.session['loggedin']=person.is_loggedIn
            return redirect("/addAppointment")

            
        except Appointment.DoesNotExist:
                return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
   loggedin=request.session.get('loggedin')
   loggedin=False
   return redirect("/login")

def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')


#add appointments
def addAppointment(request):
    
    personLogin=request.session.get('loggedin')

    if personLogin:
        personname=request.session.get('personName')

        print(personname)

        if request.method == 'POST':
                    
                name=request.POST.get('name'),
                meetdate=request.POST.get('date'),
                meettime=request.POST.get('time'),
                urgency=request.POST.get('urgency'),
                description=request.POST.get('description'),
                created_by=personname

                appointment=Appointment(name=name,date=meetdate,time=meettime,urgency=urgency,description=description,created_by=created_by)

               

                print("save")
                appointment.save()
                print(appointment.id)
                request.session['createdby']=appointment.created_by
                request.session['urgency']=appointment.urgency
                return redirect('showAppointments')
                    
        else:
                return render(request, 'addAppointment.html')

    else:
        return redirect('/loginUser')


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

    print(id)

    try:
        appointment = Appointment.objects.get(id = id)

        print(appointment)

        return render(request, 'updateAppointment.html')

        meetdate=request.POST.get('date'),
        meettime=request.POST.get('time')

        appointment =Appointment(meetdate,meettime)

        appointment.save()

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

# def update(request):


#show appointments
def showAppointments(request):

    personLogin=request.session.get('loggedin')
    personname=request.session.get('personName')
    appowner=request.session.get('createdby')
    urgency=request.session.get('urgency')

    print(urgency)

    if personLogin:
        
        if personname ==appowner:
            print('same owner')

            lows=Appointment.objects.all().filter(urgency="['low']")

            print(lows)

            appointments = Appointment.objects.all()
        return render(request, 'showAppointments.html', {
            'appointments':appointments
        })
    else:
        return redirect('/loginUser')

#show appointments
# def showAppointments(request, time):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments.html')

