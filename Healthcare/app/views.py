# from django.shortcuts import render, redirect
# from .models import Patient
# from django import forms



# def index(request):
#     return render(request, 'myapp/index.html')

# def add_patient(request):
#     if request.method == 'POST':
#         form = PatientForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the patient instance
#             return redirect('index')  # Redirect to a success page or index
#     else:
#         form = PatientForm()  # Create an empty form instance

#     return render(request, 'patients/add_patient.html', {'form': form})


# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ['Patient_Name', 'Date_of_Birth', 'Email', 'Gender', 'Age', 'Phone', 'Address']



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient
from django.core.exceptions import ValidationError
from datetime import datetime

def Add_Patient(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dob = request.POST.get('dob')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')

            # Validate required fields
            if not all([first_name, last_name, dob, email, gender, phone]):
                raise ValidationError("All fields are required.")

            # Create a new Patient object
            patient = Patient(
               Patient_First_Name=first_name,
               Patient_Last_Name=last_name,
               Date_of_Birth=datetime.strptime(dob, '%Y-%m-%d').date(),
               Email=email,
               Gender=gender,
               Phone=phone,
               Address=address
            )
            # Validate the patient object
            patient.full_clean()
            # Save the patient to the database
            patient.save()
            
            messages.success(request, 'Patient added successfully.')
            return redirect('patient_list')  # Assuming you have a patient list view
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    # If it's a GET request or if there were errors, render the form
    return render(request, 'patients/add_patient.html')

# ... existing code ...
