import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Healthcare.settings')
django.setup()

from app.models import User

def create_test_users():
    # Create an admin user
    User.objects.create_user(
        Username='Admin', 
        password='password123$', 
        role='admin', 
        Email='admin@hospital.com'
    )

    # Create a doctor user
    User.objects.create_user(
        Username='dr_smith', 
        password='DoctorPass123$', 
        role='doctor', 
        Email='drsmith@hospital.com'
    )

    # Create a patient user
    User.objects.create_user(
        Username='john_patient', 
        password='PatientPass123$', 
        role='patient', 
        Email='john@patient.com'
    )

    print("Test users created successfully!")

if __name__ == '__main__':
    create_test_users()