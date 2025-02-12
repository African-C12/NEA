from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Patient, Doctor, Appointment, Prescription, Medicine, User, Billing

class BaseFormValidationMixin:
    def clean_phone_number(self, phone_field):
        """Validate phone number format"""
        phone = self.cleaned_data.get(phone_field)
        phone_validator = RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be in format: '+999999999'. Up to 15 digits allowed."
        )
        try:
            phone_validator(phone)
        except ValidationError:
            self.add_error(phone_field, "Invalid phone number format")
        return phone

    def clean_email(self, email_field, model):
        """Validate unique email across different models"""
        email = self.cleaned_data.get(email_field)
        if model.objects.filter(**{email_field: email}).exists():
            raise ValidationError(f"This email is already registered.")
        return email

class UserCreationForm(BaseFormValidationMixin, forms.ModelForm):
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter password'
        }),
        help_text="Password must be at least 8 characters long"
    )
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['Username', 'role']
        widgets = {
            'Username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Choose a username'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PatientForm(BaseFormValidationMixin, forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'FirstName', 'LastName', 
            'DateOfBirth', 'PatientEmail', 'PatientGender', 
            'PatientAge', 'PatientPhone', 'Address'
        ]
        widgets = {
            'DateOfBirth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'PatientEmail': forms.EmailInput(attrs={'class': 'form-control'}),
            'FirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'LastName': forms.TextInput(attrs={'class': 'form-control'}),
            'PatientGender': forms.Select(attrs={'class': 'form-control'}),
            'PatientAge': forms.NumberInput(attrs={'class': 'form-control'}),
            'PatientPhone': forms.TextInput(attrs={'class': 'form-control'}),
            'Address': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_PatientEmail(self):
        return self.clean_email('PatientEmail', Patient)

    def clean_PatientPhone(self):
        return self.clean_phone_number('PatientPhone')

class DoctorForm(BaseFormValidationMixin, forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'FirstName', 'LastName', 
            'DoctorEmail', 'DoctorGender', 'DoctorAge', 
            'DoctorPhone', 'DoctorAddress', 
            'Specialization', 'Experience'
        ]
        widgets = {
            'FirstName': forms.TextInput(attrs={'class': 'form-control'}),
            'LastName': forms.TextInput(attrs={'class': 'form-control'}),
            'DoctorEmail': forms.EmailInput(attrs={'class': 'form-control'}),
            'DoctorGender': forms.Select(attrs={'class': 'form-control'}),
            'DoctorAge': forms.NumberInput(attrs={'class': 'form-control'}),
            'DoctorPhone': forms.TextInput(attrs={'class': 'form-control'}),
            'DoctorAddress': forms.Textarea(attrs={'class': 'form-control'}),
            'Specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'Experience': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean_DoctorEmail(self):
        return self.clean_email('DoctorEmail', Doctor)

    def clean_DoctorPhone(self):
        return self.clean_phone_number('DoctorPhone')

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'Doctor', 'Patient', 
            'Date', 'Time', 
            'Status'
        ]
        widgets = {
            'Doctor': forms.Select(attrs={'class': 'form-control'}),
            'Patient': forms.Select(attrs={'class': 'form-control'}),
            'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'Status': forms.Select(attrs={'class': 'form-control'})
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'DoctorID', 'PatientID', 'MedicineID', 
            'Date', 'Time', 
            'Dosage', 'Frequency', 'Refills', 
            'Instructions'
        ]
        widgets = {
            'DoctorID': forms.Select(attrs={'class': 'form-control'}),
            'PatientID': forms.Select(attrs={'class': 'form-control'}),
            'MedicineID': forms.Select(attrs={'class': 'form-control'}),
            'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'Dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'Frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'Refills': forms.NumberInput(attrs={'class': 'form-control'}),
            'Instructions': forms.Textarea(attrs={'class': 'form-control'})
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'Name', 'MedicalType', 
            'BuyPrice', 'SellPrice', 
            'BatchNo', 'ShelfNo', 
            'ExpireDate', 'ManufacturingDate', 
            'Description', 'InStockTotal'
        ]
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'MedicalType': forms.TextInput(attrs={'class': 'form-control'}),
            'BuyPrice': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'SellPrice': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'BatchNo': forms.TextInput(attrs={'class': 'form-control'}),
            'ShelfNo': forms.TextInput(attrs={'class': 'form-control'}),
            'ExpireDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ManufacturingDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control'}),
            'InStockTotal': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean_ExpireDate(self):
        expire_date = self.cleaned_data.get('ExpireDate')
        manufacturing_date = self.cleaned_data.get('ManufacturingDate')
        
        if expire_date and manufacturing_date and expire_date <= manufacturing_date:
            raise ValidationError("Expiration date must be after manufacturing date.")
        
        return expire_date

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = [
            'PatientID', 'TotalCost', 
            'PaymentStatus', 
            'DateOfBill', 'DueDate'
        ]
        widgets = {
            'PatientID': forms.Select(attrs={'class': 'form-control'}),
            'TotalCost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'PaymentStatus': forms.Select(attrs={'class': 'form-control'}),
            'DateOfBill': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'DueDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }