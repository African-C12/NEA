from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Patient, Doctor, Appointment, Prescription, Medicine, Billing, Department
from django.contrib.auth import get_user_model
import json
from datetime import date, time

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'Username': 'testuser',
            'password': 'testpass123',
            'role': 'patient',
            'Email': 'test@example.com'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.Username, 'testuser')
        self.assertEqual(self.user.role, 'patient')
        self.assertTrue(self.user.is_active)

    def test_user_roles(self):
        self.assertTrue(self.user.is_patient())
        self.assertFalse(self.user.is_doctor())
        self.assertFalse(self.user.is_admin())

class PatientModelTests(TestCase):
    def setUp(self):
        self.patient_data = {
            'FirstName': 'John',
            'LastName': 'Doe',
            'DateOfBirth': date(1990, 1, 1),
            'PatientEmail': 'john@example.com',
            'PatientGender': 'M',
            'PatientAge': 33,
            'PatientPhone': '+1234567890',
            'Address': '123 Main St'
        }
        self.patient = Patient.objects.create(**self.patient_data)

    def test_patient_creation(self):
        self.assertEqual(self.patient.FirstName, 'John')
        self.assertEqual(self.patient.LastName, 'Doe')
        self.assertEqual(self.patient.PatientGender, 'M')

class DoctorModelTests(TestCase):
    def setUp(self):
        self.doctor_data = {
            'DoctorID': 'D123',  
            'FirstName': 'Jane',
            'LastName': 'Smith',
            'DoctorEmail': 'jane@example.com',
            'DoctorGender': 'F',
            'DoctorAge': 35,
            'DoctorPhone': '+1987654321',
            'DoctorAddress': '456 Oak St',
            'Specialization': 'Cardiology',
            'Experience': 10
        }
        self.doctor = Doctor.objects.create(**self.doctor_data)

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.FirstName, 'Jane')
        self.assertEqual(self.doctor.Specialization, 'Cardiology')
        self.assertEqual(self.doctor.Experience, 10)

class AppointmentModelTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            FirstName='John',
            LastName='Doe',
            DateOfBirth=date(1990, 1, 1),
            PatientEmail='john@example.com',
            PatientGender='M',
            PatientAge=33,
            PatientPhone='+1234567890',
            Address='123 Main St'
        )
        self.doctor = Doctor.objects.create(
            DoctorID='D123',
            FirstName='Jane',
            LastName='Smith',
            DoctorEmail='jane@example.com',
            DoctorGender='F',
            DoctorAge=35,
            DoctorPhone='+1987654321',
            DoctorAddress='456 Oak St',
            Specialization='Cardiology',
            Experience=10
        )
        self.appointment_data = {
            'AppointmentID': 'APP123',
            'Doctor': self.doctor,
            'Patient': self.patient,
            'Status': 'SCHEDULED',
            'Date': date.today(),
            'Time': time(10, 0)
        }
        self.appointment = Appointment.objects.create(**self.appointment_data)

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.Status, 'SCHEDULED')
        self.assertEqual(self.appointment.Doctor, self.doctor)
        self.assertEqual(self.appointment.Patient, self.patient)

class MedicineModelTests(TestCase):
    def setUp(self):
        self.medicine_data = {
            'Name': 'Aspirin',
            'MedicalType': 'Pain Reliever',
            'BuyPrice': 5.99,
            'SellPrice': 9.99,
            'BatchNo': 'B123',
            'ShelfNo': 'S1',
            'ExpireDate': date(2026, 2, 11),
            'ManufacturingDate': date(2025, 2, 11),
            'Description': 'Pain relief medication',
            'InStockTotal': 100
        }
        self.medicine = Medicine.objects.create(**self.medicine_data)

    def test_medicine_creation(self):
        self.assertEqual(self.medicine.Name, 'Aspirin')
        self.assertEqual(self.medicine.MedicalType, 'Pain Reliever')
        self.assertEqual(self.medicine.InStockTotal, 100)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test user
        self.user = get_user_model().objects.create_user(
            Username='testuser',
            password='testpass123',
            role='admin',
            Email='admin@example.com'
        )
        # Need to use Username field for login
        self.client.login(Username='testuser', password='testpass123')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_view(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_patient_list_view(self):
        # Create a test patient first
        patient = Patient.objects.create(
            FirstName='Test',
            LastName='Patient',
            DateOfBirth=date(1990, 1, 1),
            PatientEmail='test@example.com',
            PatientGender='M',
            PatientAge=33,
            PatientPhone='+1234567890',
            Address='123 Test St'
        )
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Patient_List.html')
        self.assertContains(response, 'Test Patient')

    def test_doctor_list_view(self):
        # Create a test doctor first
        doctor = Doctor.objects.create(
            DoctorID='D123',
            FirstName='Test',
            LastName='Doctor',
            DoctorEmail='doctor@example.com',
            DoctorGender='F',
            DoctorAge=35,
            DoctorPhone='+1987654321',
            DoctorAddress='456 Test St',
            Specialization='Test Specialty',
            Experience=5
        )
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Doctor_List.html')
        self.assertContains(response, 'Test Doctor')

    def test_add_patient_view(self):
        response = self.client.get(reverse('add_patient'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Add_Patient.html')

        # Test POST request
        patient_data = {
            'FirstName': 'New',
            'LastName': 'Patient',
            'DateOfBirth': '1990-01-01',
            'PatientEmail': 'new@example.com',
            'PatientGender': 'M',
            'PatientAge': 33,
            'PatientPhone': '+1234567890',
            'Address': '789 New St'
        }
        response = self.client.post(reverse('add_patient'), patient_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Patient.objects.filter(FirstName='New').exists())

    def test_add_doctor_view(self):
        response = self.client.get(reverse('add_doctor'))
        self.assertEqual(response.status_code, 200)
