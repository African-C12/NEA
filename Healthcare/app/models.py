from django.db import models


class Patient(models.Model):
  Patient_ID = models.CharField(max_length=10, unique=True)
  First_Name = models.CharField(max_length=100)
  Last_Name = models.CharField(max_length=100)
  Date_of_Birth = models.CharField(max_length=100)
  Patient_Email = models.EmailField(max_length=100)
  Patient_Gender = models.CharField(max_length=50)
  Patient_Age = models.IntegerField()
  Patient_Phone = models.IntegerField()
  Address = models.TextField()

  class Meta:
        ordering = ['Last_Name', 'First_Name']


  def __str__(self):
    return f"{self.first_name} {self.last_name} ({self.Patient_ID})"


class Doctor(models.Model):
  Doctor_ID = models.CharField(max_length=10, unique=True)
  First_Name = models.CharField(max_length=100)
  Last_Name = models.CharField(max_length=100)
  Doctor_Email = models.EmailField(max_length=100)
  Doctor_Gender = models.CharField(max_length=50)
  Doctor_Age = models.IntegerField()
  Doctor_Phone = models.IntegerField()
  Doctor_Address = models.TextField()
  Specialization = models.CharField(max_length=100)
  Experience = models.IntegerField()

  class Meta:
        ordering = ['Last_Name', 'First_Name']

  def __str__(self):
    return f"{self.first_name} {self.last_name} ({self.Doctor_ID})"


class Department(models.Model):
  Department_ID = models.CharField(max_length=10, unique=True)
  Department_name = models.CharField(max_length=100)

  def __str__(self):
     return self.Department_ID


class Appointment(models.Model):
  Appointment_ID = models.CharField(max_length=10, unique=True)
  Doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
  Patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
  Patient_number = models.ForeignKey('Patient', on_delete=models.CASCADE)
  Patient_email = models.ForeignKey('Patient', on_delete=models.CASCADE)
  Date = models.DateField()
  Time = models.TimeField()
  Created_at = models.DateTimeField(auto_now_add=True)
  Booked_on = models.DateField(auto_now=True)

  class Meta:
        ordering = ['-date', '-time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time'], 
                name='unique_appointment'
            )
        ]

  def __str__(self):
        return f"{self.Doctor.Last_Name} - {self.Patient.Last_Name} ({self.Date})"


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

  def __str__(self):
    return self.Prescription_ID



class Medicine(models.Model):
  medicine_ID = models.AutoField(primary_key=True)
  name = models.CharField(max_length=255)
  medical_type = models.CharField(max_length=255)
  buy_price = models.DecimalField(max_digits=10, decimal_places=1)
  sell_price = models.DecimalField(max_digits=10, decimal_places=1)
  Batch_No = models.CharField(max_length=255)
  Shelf_No = models.CharField(max_length=255)
  Expire_Date = models.DateField()
  Manufacturing_Date = models.DateField()
  Description = models.CharField(max_length=255)
  In_Stock_Total = models.IntegerField()

  def __str__(self):
     return self.Medicine_ID


class Billing(models.Model):
  Bill_ID = models.AutoField(primary_key=True)
  Patient_ID = models.ForeignKey('Patient', on_delete=models.CASCADE)
  Total_Cost = models.CharField(max_length=255)
  Payment_Status  = models.CharField(max_length=100)
  Date_of_Bill = models.DateField()

  def __str__(self):
    return self.Bill_ID

  