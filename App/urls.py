from django.urls import path
from App import views

urlpatterns =[

      path('',views.index, name='index'),
       
      path('register',views.register, name='register'),

      path('loginUser',views.loginUser, name='loginUser'),

      path('contact',views.contact, name='contact'),

      path('addAppointment',views.addAppointment, name='addAppointment'),

      path('showAppointments',views.showAppointments, name='showAppointments'),

      path('deleteAppointment/<int:id>',views.deleteAppointment),

      path('logoutUser',views.logoutUser),

      path('update',views.update),

      path('updateAppointment/<int:id>',views.updateAppointment),

      path('update/<int:id>',views.update, name='update')
]