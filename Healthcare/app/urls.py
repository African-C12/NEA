from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Index, name='Index'),
    path('patient/add/', views.Add_Patient, name='add_patient'),
    path('doctor/add/', views.Add_Doctor, name='add_doctor'),
    path('appointment/add/', views.Add_Appointment, name='add_appointment'),
    path('prescription/add/', views.Add_Prescription, name='add_prescription'),
    path('medicine/add/', views.Add_Medicine, name='add_medicine'),
    path('patient/list/', views.Patient_List, name='patient_list'),
    path('doctor/list/', views.Doctor_List, name='doctor_list'),
    path('appointment/list/', views.Appointment_List, name='appointment_list'),
    path('prescription/list/', views.Prescription_List, name='prescription_list'),
    path('medicine/list/', views.Medicine_List, name='medicine_list'),
]