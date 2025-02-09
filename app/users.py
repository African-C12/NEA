from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Inherits default fields: username, password, email, first_name, last_name
    ROLES = (
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    phone_number = models.CharField(max_length=15, blank=True) 