from django.db import models


class Patient(models.Model):
  Patient_ID = models.CharField(max_length=10, unique=True)
  First_Name = models.CharField(max_length=100)
  Last_Name = models.CharField(max_length=100)
  Date_of_Birth = models.CharField(max_length=100)
  Email = models.EmailField(max_length=100)
  Gender = models.CharField(max_length=50)
  Age = models.IntegerField()
  Phone = models.IntegerField()
  Address = models.TextField()

  def __str__(self):
    return self.Patient_ID
  


