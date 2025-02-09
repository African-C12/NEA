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
from .models import Patient, Doctor, Medicine, Appointment, Prescription, User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, PatientForm, DoctorForm
import logging

user = get_user_model()

logger = logging.getLogger(__name__)




@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        return redirect('login')
    return render(request, 'admin_dashboard.html')

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect('login')
    return render(request, 'doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    if not request.user.is_patient():
        return redirect('login')
    return render(request, 'patient_dashboard.html')





def custom_login(request):
    if request.method == 'POST':
        Username = request.POST.get('username')
        Password = request.POST.get('password')
        
        user = authenticate(request, username=Username, password=Password)
        if user is not None:
            login(request, user)
            
            # Role-based redirection
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
            elif user.role == 'patient':
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'Login.html')





def Add_Patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            patient = patient_form.save()
            messages.success(request, 'Patient added successfully')
            return redirect('patient_list')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        patient_form = PatientForm()
    
    return render(request, 'patients/add_patient.html', {'form': patient_form})





def Add_Doctor(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)
        if doctor_form.is_valid():
            doctor = doctor_form.save()
            messages.success(request, 'Doctor added successfully')
            return redirect('doctor_list')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        doctor_form = DoctorForm()
    
    return render(request, 'doctors/add_doctor.html', {'form': doctor_form})





def Add_Appointment(request):
    if request.method == 'POST':
        DoctorID = request.POST.get('doctor')
        PatientID = request.POST.get('patient')
        Date = request.POST.get('date')
        Time = request.POST.get('time')

        if not all([DoctorID, PatientID, Date, Time]):
            messages.error(request, 'All fields are required.')
            return redirect('add_appointment')

        try:
            doctor = Doctor.objects.get(DoctorID=DoctorID)
            patient = Patient.objects.get(PatientID=PatientID)

            appointment = Appointment.objects.create(
                DoctorID=doctor,
                PatientID=patient,
                Date=Date,
                Time=Time,
                Status='SCHEDULED'
            )
            messages.success(request, 'Appointment added successfully.')
            return redirect('appointments')

        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            messages.error(request, 'Invalid Doctor or Patient.')
            return redirect('add_appointment')

    # If it's a GET request or if there were errors, render the form
    return render(request, 'appointments/add_appointment.html')



def Add_Prescription(request):
    if request.method == 'POST':
        DoctorID = request.POST.get('doctor')
        PatientID = request.POST.get('patient')
        MedicineID = request.POST.get('medicine')
        Date = request.POST.get('date')
        Time = request.POST.get('time')
        Dosage = request.POST.get('dosage')
        Frequency = request.POST.get('frequency')
        Refills = request.POST.get('refills')

        if not all([DoctorID, PatientID, MedicineID, Date, Time, Dosage, Frequency, Refills]):
            messages.error(request, 'All fields are required.')
            return redirect('add_prescription')

        try:
            doctor = Doctor.objects.get(DoctorID=DoctorID)
            patient = Patient.objects.get(PatientID=PatientID)
            medicine = Medicine.objects.get(MedicineID=MedicineID)

            prescription = Prescription.objects.create(
                DoctorID=doctor,
                PatientID=patient,
                MedicineID=medicine,
                Date=Date,
                Time=Time,
                Dosage=Dosage,
                Frequency=Frequency,
                Refills=Refills
            )
            messages.success(request, 'Prescription added successfully.')
            return redirect('prescriptions')

        except (Doctor.DoesNotExist, Patient.DoesNotExist, Medicine.DoesNotExist):
            messages.error(request, 'Invalid Doctor, Patient, or Medicine.')
            return redirect('add_prescription')

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
def create_user(Username, Password, Role='patient'):
    form = UserCreationForm(data={
        'username': Username, 
        'role': Role, 
        'password1': Password, 
        'password2': Password
    })
    if form.is_valid():
        user = form.save()
        return user
    else:
        # Log form errors or handle validation failure
        return None

def verify_user(Username, Password):
    User = get_user_model()
    user = authenticate(request=None, username=Username, password=Password)
    if user is not None:
        return True
    else:
        return False


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Redirect to appropriate dashboard based on user role
    if request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')
    elif request.user.role == 'doctor':
        return render(request, 'doctor_dashboard.html')
    elif request.user.role == 'patient':
        return render(request, 'patient_dashboard.html')
    
    return redirect('login')

def login_view(request):
    logger.info(f"Login view accessed. Method: {request.method}")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        logger.info(f"Login attempt for username: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.Username}!')
            logger.info(f"User {username} logged in successfully")
            return redirect('home')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            messages.error(request, 'Invalid username or password')
    
    logger.info("Rendering login template")
    return render(request, 'The_Login.html')  # Updated template name

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')