from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('contact.html', views.contact, name="contact"),
   path('about.html', views.about, name="about"),
   path('services.html', views.services, name="services"),
   path('doctors.html', views.doctors, name="doctors"),
   path('register.html', views.register, name="register"),
   path('dashboard.html', views.dashboard, name="dashboard"),
   path('alldoctors.html', views.alldoctors, name="alldoctors"),
   path('mybooking.html', views.mybooking, name="mybooking"),
   path('scheduledsession.html', views.scheduledsession, name="scheduledsession"),
   path('appointmentbook.html', views.appointmentbook, name="appointmentbook"),
   path('dashboardForDoctor.html', views.dashboardForDoctor, name="dashboardForDoctor"),
   path('allPatients.html', views.your_view_function, name="allPatients"),
   path('dashboardsecretary.html', views.dashboardsecretary, name="dashboardsecretary"),
   path('patientsecretary.html', views.patientsecretary, name="patientsecretary"),
   path('appointmentspagesecretary.html', views.appointmentspagesecretary, name="appointmentspagesecretary"),
   #APPOINTMENT LIST
   path('appointmentspagedoctors.html', views.appointment_list, name="appointmentspagedoctors"),

   
   path('login.html', views.loginPage, name="login"),
   path('logout/', views.logoutUser, name="logout"),
   
   path('appointment_bookingDetails/', views.appointment_bookingDetails, name='appointment_bookingDetails'),
   path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment',),
   
   path('delete_appointmentDoctors/<int:appointment_id>/', views.delete_appointmentDoctors, name='delete_appointmentDoctors',),

   
   
]
