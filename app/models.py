from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    def create_user(self, Username, password=None, **extra_fields):
        if not Username:
            raise ValueError('The Username field must be set')
        
        # Validate role
        role = extra_fields.get('role', '').lower()
        if role not in ['admin', 'doctor', 'patient']:
            raise ValueError('Invalid role. Must be admin, doctor, or patient.')
        
        # Generate unique user_id if not provided
        if 'user_id' not in extra_fields:
            extra_fields['user_id'] = str(uuid.uuid4())

        user = self.model(Username=Username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, Username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(Username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ]

    user_id = models.CharField(max_length=100, unique=True, primary_key=True)
    Username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    Email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = ['role']

    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def __str__(self):
        return f"{self.Username} ({self.role})"

    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role

    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'admin'

    def is_doctor(self):
        """Check if user is a doctor"""
        return self.role == 'doctor'

    def is_patient(self):
        """Check if user is a patient"""
        return self.role == 'patient'



def generate_patient_id():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))


  
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    PatientID = models.CharField(max_length=10, unique=True, editable=False, default=generate_patient_id)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    DateOfBirth = models.DateField()
    PatientEmail = models.EmailField(max_length=100, unique=True)
    PatientGender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    PatientAge = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        help_text="Patient's age between 0 and 150 years"
    )
    PatientPhone = models.CharField(
        verbose_name="Phone Number",
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    Address = models.TextField()

    class Meta:
        ordering = ['LastName', 'FirstName']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


    def __str__(self):
      return f"{self.FirstName} {self.LastName} ({self.PatientID})"


  
class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    DoctorID = models.CharField(max_length=10, unique=True, editable=False)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    DoctorEmail = models.EmailField(max_length=100, unique=True)
    DoctorGender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    DoctorAge = models.IntegerField(
        validators=[MinValueValidator(25), MaxValueValidator(80)]
    )
    DoctorPhone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    DoctorAddress = models.TextField()
    Specialization = models.CharField(max_length=100)
    Experience = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['LastName', 'FirstName']

    def __str__(self):
      return f"{self.FirstName} {self.LastName} ({self.DoctorID})"


class Department(models.Model):
  DepartmentID = models.CharField(max_length=10, unique=True)
  DepartmentName = models.CharField(max_length=100)

  def __str__(self):
     return self.DepartmentID


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    AppointmentID = models.CharField(max_length=10, unique=True)
    Doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    Patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    Date = models.DateField()
    Time = models.TimeField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    BookedOn = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-Date', '-Time']
        constraints = [
            models.UniqueConstraint(
                fields=['Doctor', 'Date', 'Time'], 
                name='Unique_Appointment'
            )
        ]

    def __str__(self):
        return f"{self.Doctor} - {self.Patient} ({self.Date})"


class Prescription(models.Model):
  PrescriptionID = models.CharField(max_length=10, unique=True)
  DoctorID = models.ForeignKey('Doctor', on_delete=models.CASCADE)
  PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
  MedicineID = models.ForeignKey('Medicine', on_delete=models.CASCADE)
  Date = models.DateField()
  Time = models.TimeField()
  Dosage = models.CharField(max_length=100)
  Frequency = models.CharField(max_length=100)
  Refills = models.IntegerField()
  Instructions = models.TextField()
  CreatedAt = models.DateTimeField(auto_now_add=True)
  UpdatedAt = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Prescription {self.PrescriptionID} - {self.PatientID}"



class Medicine(models.Model):
    MedicineID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    MedicalType = models.CharField(max_length=255)
    BuyPrice = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    SellPrice = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    BatchNo = models.CharField(max_length=255)
    ShelfNo = models.CharField(max_length=255)
    ExpireDate = models.DateField()
    ManufacturingDate = models.DateField()
    Description = models.TextField(blank=True)
    InStockTotal = models.IntegerField(validators=[MinValueValidator(0)])
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Name} {self.MedicineID} ({self.BatchNo})"
    


class Billing(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    BillID = models.AutoField(primary_key=True)
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    TotalCost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total cost in dollars"
    )
    PaymentStatus = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    DateOfBill = models.DateField()
    DueDate = models.DateField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-DateOfBill']
        verbose_name = 'Billing'
        verbose_name_plural = 'Billings'

    def __str__(self):
        return f"Bill {self.BillID} - {self.PatientID}"
