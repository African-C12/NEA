from django.shortcuts import render, redirect
from .models import Patient
from django import forms



def index(request):
    return render(request, 'myapp/index.html')

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Save the patient instance
            return redirect('index')  # Redirect to a success page or index
    else:
        form = PatientForm()  # Create an empty form instance

    return render(request, 'patients/add_patient.html', {'form': form})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['Patient_Name', 'Date_of_Birth', 'Email', 'Gender', 'Age', 'Phone', 'Address']



