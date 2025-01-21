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
from .models import Patient, Doctor, Medicine, Appointment, Prescription, users
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth import get_user_model
from .custom_hash import CustomHasher

User = get_user_model()

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





def Add_Doctor(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            specialization = request.POST.get('specialization')
            experience = request.POST.get('experience')

            # Validate required fields
            if not all([first_name, last_name, email, gender, phone, specialization, experience]):
                raise ValidationError("All fields are required.")

            # Create a new Doctor object
            doctor = Doctor(
                First_Name=first_name,
                Last_Name=last_name,
                Doctor_Email=email,
                Doctor_Gender=gender,
                Doctor_Phone=phone,
                Doctor_Address=address,
                Specialization=specialization,
                Experience=int(experience)
            )
            # Validate the doctor object
            doctor.full_clean()
            # Save the doctor to the database
            doctor.save()
            
            messages.success(request, 'Doctor added successfully.')
            return redirect('doctor_list')  # Assuming you have a doctor list view
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    # If it's a GET request or if there were errors, render the form
    return render(request, 'doctors/add_doctor.html')




def Add_Appointment(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            doctor_id = request.POST.get('doctor')
            patient_id = request.POST.get('patient')
            date = request.POST.get('date')
            time = request.POST.get('time')
            status = request.POST.get('status', 'SCHEDULED')  # Default to SCHEDULED if not provided

            # Validate required fields
            if not all([doctor_id, patient_id, date, time]):
                raise ValidationError("All fields are required.")

            # Get the Doctor and Patient instances
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)

            # Create a new Appointment object
            appointment = Appointment(
                Doctor=doctor,
                Patient=patient,
                Patient_number=patient,  # Using same patient instance for the ForeignKey
                Patient_email=patient,   # Using same patient instance for the ForeignKey
                Status=status,
                Date=date,
                Time=time
            )

            # Validate the appointment object
            appointment.full_clean()
            # Save the appointment to the database
            appointment.save()
            
            messages.success(request, 'Appointment scheduled successfully.')
            return redirect('appointment_list')  # Redirect to appointment list view
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
        except Patient.DoesNotExist:
            messages.error(request, 'Selected patient does not exist.')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    # If it's a GET request or if there were errors, render the form
    return render(request, 'appointments/add_appointment.html')



def Add_Prescription(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            doctor_id = request.POST.get('doctor')
            patient_id = request.POST.get('patient')
            medicine_id = request.POST.get('medicine')
            date = request.POST.get('date')
            time = request.POST.get('time')
            dosage = request.POST.get('dosage')
            frequency = request.POST.get('frequency')
            refills = request.POST.get('refills')
            instructions = request.POST.get('instructions')

            # Validate required fields
            if not all([doctor_id, patient_id, medicine_id, date, time, dosage, frequency, refills]):
                raise ValidationError("All fields are required.")

            # Get the Doctor, Patient and Medicine instances
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
            medicine = Medicine.objects.get(Medicine_ID=medicine_id)

            # Create a new Prescription object
            prescription = Prescription(
                Doctor_ID=doctor,
                Patient_ID=patient,
                Medicine_ID=medicine,
                Date=date,
                Time=time,
                Dosage=dosage,
                Frequency=frequency,
                Refills=refills,
                Instructions=instructions
            )

            # Validate the prescription object
            prescription.full_clean()
            # Save the prescription to the database
            prescription.save()
            
            messages.success(request, 'Prescription created successfully.')
            return redirect('prescription_list')  # Redirect to prescription list view
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
        except Patient.DoesNotExist:
            messages.error(request, 'Selected patient does not exist.')
        except Medicine.DoesNotExist:
            messages.error(request, 'Selected medicine does not exist.')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    # If it's a GET request or if there were errors, render the form
    return render(request, 'prescriptions/add_prescription.html')




def Add_Medicine(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            medical_type = request.POST.get('medical_type')
            buy_price = request.POST.get('buy_price')
            sell_price = request.POST.get('sell_price')
            batch_no = request.POST.get('batch_no')
            shelf_no = request.POST.get('shelf_no')
            expire_date = request.POST.get('expire_date')
            manufacturing_date = request.POST.get('manufacturing_date')
            description = request.POST.get('description')
            in_stock_total = request.POST.get('in_stock_total')

            # Validate required fields
            if not all([name, medical_type, buy_price, sell_price, batch_no, shelf_no, 
                       expire_date, manufacturing_date, in_stock_total]):
                raise ValidationError("All fields except description are required.")

            # Create a new Medicine object
            medicine = Medicine(
                Name=name,
                Medical_Type=medical_type,
                Buy_Price=buy_price,
                Sell_Price=sell_price,
                Batch_No=batch_no,
                Shelf_No=shelf_no,
                Expire_Date=expire_date,
                Manufacturing_Date=manufacturing_date,
                Description=description,
                In_Stock_Total=in_stock_total
            )

            # Validate the medicine object
            medicine.full_clean()
            # Save the medicine to the database
            medicine.save()
            
            messages.success(request, 'Medicine added successfully.')
            return redirect('medicine_list')  # Redirect to medicine list view
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    # If it's a GET request or if there were errors, render the form
    return render(request, 'medicines/add_medicine.html')



def Patient_List(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

def Doctor_List(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

def Appointment_List(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

def Prescription_List(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})

def Medicine_List(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicines/medicine_list.html', {'medicines': medicines})





# In your views or wherever you need to hash passwords
def create_user(username, password):
    hasher = CustomHasher()
    hashed_password = hasher.custom_hash(password)
    
    return User.objects.create(
        username=username,
        password=hashed_password
    )

def verify_user(username, password):
    hasher = CustomHasher()
    User = User.objects.get(username=username)
    return hasher.verify(password, users.password)