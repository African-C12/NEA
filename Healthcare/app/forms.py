from django import forms
from .models import Patient, Doctor, Appointment, Prescription, Medicine

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['First_Name', 'Last_Name', 'Date_of_Birth', 'Patient_Email', 
                 'Patient_Gender', 'Patient_Age', 'Patient_Phone', 'Address']
        widgets = {
            'Date_of_Birth': forms.DateInput(attrs={'type': 'date'}),
            'Email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'Address': forms.Textarea(attrs={'rows': 3})
        }

        


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['First_Name', 'Last_Name', 'Doctor_Email', 'Doctor_Gender',
                 'Doctor_Age', 'Doctor_Phone', 'Doctor_Address', 
                 'Specialization', 'Experience']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['Doctor', 'Patient', 'Date', 'Time']




class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['Doctor_ID', 'Patient_ID', 'Medicine_ID', 'Date', 'Time',
                 'Dosage', 'Frequency', 'Refills', 'Instructions']




class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'medical_type', 'buy_price', 'sell_price',
                 'Batch_No', 'Shelf_No', 'Expire_Date', 'Manufacturing_Date',
                 'Description', 'In_Stock_Total']