"""
URL configuration for Healthcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('base', views.Index, name='Index'),
    path('Patient/Add', views.Add_Patient, name='add_patient'),
    path('Doctor/Add', views.Add_Doctor, name='add_doctor'),
    path('Appointment/Add', views.Add_Appointment, name='add_appointment'),
    path('Prescription/Add', views.Add_Prescription, name='add_prescription'),
    path('Medicine/Add', views.Add_Medicine, name='add_medicine'),
    path('Patient/List', views.Patient_List, name='patient_list'),
    path('Doctor/List', views.Doctor_List, name='doctor_list'),
    path('Appointment/List', views.Appointment_List, name='appointment_list'),
    path('Prescription/List', views.Prescription_List, name='prescription_list'),
    path('Medicine/List', views.Medicine_List, name='medicine_list'),
]
