from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Index, name='Index'),
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
     # Add placeholders for dashboard routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
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