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

   
   path('login.html', views.loginPage, name="login"),
   path('logout/', views.logoutUser, name="logout"),
]
