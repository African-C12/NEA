from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

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
    
    Patient_ID = models.CharField(max_length=10, unique=True, editable=False, default=generate_patient_id)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Date_of_Birth = models.DateField()
    Patient_Email = models.EmailField(max_length=100, unique=True)
    Patient_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Patient_Age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        help_text="Patient's age between 0 and 150 years"
    )
    Patient_Phone = models.CharField(
        verbose_name="Phone Number",
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    Address = models.TextField()

    class Meta:
        ordering = ['Last_Name', 'First_Name']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


    def __str__(self):
      return f"{self.First_Name} {self.Last_Name} ({self.Patient_ID})"


  
class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    Doctor_ID = models.CharField(max_length=10, unique=True, editable=False)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Doctor_Email = models.EmailField(max_length=100, unique=True)
    Doctor_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Doctor_Age = models.IntegerField(
        validators=[MinValueValidator(25), MaxValueValidator(80)]
    )
    Doctor_Phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    Doctor_Address = models.TextField()
    Specialization = models.CharField(max_length=100)
    Experience = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['Last_Name', 'First_Name']

    def __str__(self):
      return f"{self.First_Name} {self.Last_Name} ({self.Doctor_ID})"


class Department(models.Model):
  Department_ID = models.CharField(max_length=10, unique=True)
  Department_name = models.CharField(max_length=100)

  def __str__(self):
     return self.Department_ID


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    Appointment_ID = models.CharField(max_length=10, unique=True)
    Doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    Patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    Date = models.DateField()
    Time = models.TimeField()
    Created_at = models.DateTimeField(auto_now_add=True)
    Booked_on = models.DateField(auto_now=True)

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
  Prescription_ID = models.CharField(max_length=10, unique=True)
  Doctor_ID = models.ForeignKey('Doctor', on_delete=models.CASCADE)
  Patient_ID = models.ForeignKey('Patient', on_delete=models.CASCADE)
  Medicine_ID = models.ForeignKey('Medicine', on_delete=models.CASCADE)
  Date = models.DateField()
  Time = models.TimeField()
  Dosage = models.CharField(max_length=100)
  Frequency = models.CharField(max_length=100)
  Refills = models.IntegerField()
  Instructions = models.TextField()
  Created_At = models.DateTimeField(auto_now_add=True)
  Updated_At = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Prescription {self.Prescription_ID} - {self.Patient_ID}"



class Medicine(models.Model):
    Medicine_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Medical_Type = models.CharField(max_length=255)
    Buy_Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    Sell_Price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    Batch_No = models.CharField(max_length=255)
    Shelf_No = models.CharField(max_length=255)
    Expire_Date = models.DateField()
    Manufacturing_Date = models.DateField()
    Description = models.TextField(blank=True)
    In_Stock_Total = models.IntegerField(validators=[MinValueValidator(0)])
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Name} {self.Medicine_ID} ({self.Batch_No})"
    


class Billing(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    Bill_ID = models.AutoField(primary_key=True)
    Patient_ID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    Total_Cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total cost in dollars"
    )
    Payment_Status = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    Date_of_Bill = models.DateField()
    Due_Date = models.DateField()
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-Date_of_Bill']
        verbose_name = 'Billing'
        verbose_name_plural = 'Billings'

    def __str__(self):
        return f"Bill {self.Bill_ID} - {self.Patient_ID}"

  



