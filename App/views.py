from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from App.models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.template import RequestContext
from django.contrib import messages
import time
import smtplib as s

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


def profile(request):
    return render(request, 'profile.html')

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
                    apptype=request.POST.get('apptype','')
                    email=request.POST.get('email','')
                    created_by=personname

                    emails=email.split(",",1)
                    print(emails)                   
                    try:
                        appointment=Appointment(name=name,date=meetdate,time=meettime, description=description, created_by=created_by, urgency=urgency,apptype=apptype)
                    
                        # if person.is_valid():

                        request.session['name']=appointment.name
                        request.session['time']=appointment.time
                        request.session['date']=appointment.date
                        request.session['owner']=appointment.created_by

                        appointment.save() 
                        request.session['emails']=emails
                        
                        doEmail(request,emails,1)
                        messages.success(request,"Appointment added!")
                        
                        return redirect("/showAppointments")   
                    except:
                        messages.warning(request,"Unable to add appointment, check the fields again!")
                        return redirect("/addAppointment")
      
    else:
        return redirect("/loginuser")
    return render(request, 'addAppointment.html')

def doEmail(request,emails,flag):
    person=request.session.get('owner')
    time=request.session.get('time')
    name=request.session.get('name')
    date=request.session.get('date')
    
    delperson=request.session.get('delowner')
    deltime=request.session.get('deltime')
    delname=request.session.get('delname')
    deldate=request.session.get('deldate')

    upperson=request.session.get('upowner')
    uptime=request.session.get('uptime')
    upname=request.session.get('upname')
    update=request.session.get('update')
   
    for email in emails:
        ob=s.SMTP("smtp.gmail.com",587)
        ob.connect("smtp.gmail.com",587)
        ob.starttls()

        ob.login("yourworkappointments@gmail.com","workapp123")

        if flag==1:
            subject="New appointment: "+name
            body ="You have a new appointment scheduled with "+ person+ " on "+ date+" at "+time+"."+" (according to 24-hour format) "
        
        elif flag==2:
            subject="Deleted appointment: "+name
            body ="Your appointment with "+ person+ " which was on "+ date+" at "+time+" has been cancelled."+" (according to 24-hour format) "

        else:
            subject="Updated appointment: "+name
            body ="The timing of your appointment with "+ person+ " which was on "+ date+" at "+time+" has been updated to "+update+" at "+uptime+". (according to 24-hour format) "

        
        message="Subject:{}\n\n{}".format(subject,body)
        ob.sendmail("yourworkappointments@gmail.com",email,message)
        ob.quit()

#delete appointments
def deleteAppointment(request,id):

    personLogin=request.session.get('loggedin')
    emails=request.session.get('emails')

    if personLogin:
    
        try:
            appointment=Appointment.objects.get(id=id)

            request.session['delname']=appointment.name
            request.session['deltime']=appointment.time
            request.session['deldate']=appointment.date
            request.session['delowner']=appointment.created_by


            appointment.delete()

            doEmail(request,emails,2)
            messages.success(request,"Appointment deleted!")
            return redirect('/showAppointments')
            
        except Appointment.DoesNotExist:
            # return redirect('index')
            return redirect('/showAppointments')

    return redirect('/showAppointments')


#update appointments
def updateAppointment(request, id):

    personLogin=request.session.get('loggedin')
    
    if personLogin:

        try:
            appointment = Appointment.objects.get(id = id)

            return render(request, 'updateAppointment.html',{
                'appointment':appointment
            })

        except Appointment.DoesNotExist:
            # return redirect('index')
            print("Not in db")
    
        
    return render(request,'showAppointments.html')

 
def update(request, id):

    personLogin=request.session.get('loggedin')
    emails=request.session.get('emails')

    if personLogin: 
        if request.method=="POST":

                try:
                    appointment = Appointment.objects.get(id = id)

                    name=request.POST.get('name','')
                    meetdate=request.POST.get('date','')
                    meettime=request.POST.get('time','')
                    urgency=request.POST.get('urgency','')
                    description=request.POST.get('description','')
                    apptype=request.POST.get('apptype','')
                    created_by=appointment.created_by

                    appointment.name=name
                    appointment.date=meetdate
                    appointment.time=meettime
                    appointment.urgency=urgency
                    appointment.description=description
                    appointment.apptype=apptype

                    request.session['upname']=appointment.name
                    request.session['uptime']=appointment.time
                    request.session['update']=appointment.date
                    request.session['upowner']=appointment.created_by


                    doEmail(request,emails,3)

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
            
            upcoming=Appointment.objects.all().filter(apptype="upcoming")

            completed=Appointment.objects.all().filter(apptype="completed")

            undecided=Appointment.objects.all().filter(apptype='undecided')

            appointments = Appointment.objects.all()

            # summary='<br><h4><b  id= "name">{{appointment.name}}</b></h4> <h6>Urgency: <b id= "urgency">{{appointment.urgency}}</b></h6><h6 class= "timedate"><b id= "date">{{appointment.date}}</b> | Timing: <b id= "time">{{appointment.time}}</b></h6>'

            return render(request, 'showAppointments.html', {
            'upcoming':upcoming,
            'completed':completed,
            'undecided':undecided,
            'appointments':appointments,
            # 'summary':summary
        })
    else:
        return redirect('/loginUser')
    return render(request,'showAppointments.html')
