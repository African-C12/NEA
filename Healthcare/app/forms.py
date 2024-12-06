from django import forms
from .models import Patient
from .forms import PatientForm 

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['Patient_Name', 'Date_of_Birth', 'Email', 'Gender', 'Age', 'Phone', 'Address']