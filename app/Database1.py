# from sqlalchemy import create_engine
# from sqlalchemy import Boolean, Column, Float, Integer, String, Text, Date, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
# from django.conf import settings

# engine = create_engine(settings.DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# class User(Base):
#     __tablename__ = 'users'
#     UserID = Column(String, primary_key=True)
#     Username = Column(String, unique=True, nullable=False)
#     Password = Column(String, nullable=False)
#     Role = Column(String, nullable=False)
#     IsActive = Column(Boolean, default=False)
#     IsAuthenticated = Column(Boolean, default=False)
#     IsAnonymous = Column(Boolean, default=False)

#     def __init__(self, user_id, username, password, role):
#         self.UserID = user_id
#         self.Username = username
#         self.Password = password
#         self.Role = role

#     def get_id(self):
#         return str(self.UserID)

#     @property
#     def is_authenticated(self):
#         return self.IsAuthenticated

#     @property
#     def is_active(self):
#         return self.IsActive

#     @property
#     def is_anonymous(self):
#         return self.IsAnonymous

#     def __repr__(self):
#         return f"<User(Username={self.Username}, Role={self.Role})>"

#     def to_dict(self):
#         return {
#             'UserID': self.UserID,
#             'Username': self.Username,
#             'Password': self.Password,
#             'Role': self.Role
#         }


# class Patient(Base):
#     __tablename__ = 'patients'

#     PatientID = Column(String, ForeignKey('users.UserID'), primary_key=True)
#     First_Name = Column(String)
#     Last_Name = Column(String)
#     Date_Of_Birth = Column(Date)
#     Gender = Column(String)
#     Email = Column(String, unique=True)
#     PhoneNumber = Column(Integer, unique=True)
#     Address = Column(Text, unique=True)

#     appointments = relationship("Appointment", backref='patient')
#     prescriptions = relationship("Prescription", backref='patient')
#     billings = relationship("Billing", backref='patient')

#     def __init__(self, patient_id, first_name, last_name, date_of_birth, gender, email, phone_number, address):
#         self.PatientID = patient_id
#         self.First_Name = first_name
#         self.Last_Name = last_name
#         self.DateOfBirth = date_of_birth
#         self.Gender = gender
#         self.Email = email
#         self.PhoneNumber = phone_number
#         self.Address = address

#     def to_dict(self):
#         return {
#             'PatientID': self.PatientID,
#             'First_Name': self.First_Name,
#             'Last_Name': self.Last_Name,
#             'DateOfBirth': self.DateOfBirth.strftime('%Y-%m-%d'),
#             'Gender': self.Gender,
#             'Email': self.Email,
#             'PhoneNumber': self.PhoneNumber,
#             'Address': self.Address
#         }


# class Doctor(Base):
#     __tablename__ = 'doctors'

#     DoctorID = Column(String, ForeignKey('users.UserID'), primary_key=True)
#     First_Name = Column(String)
#     Last_Name = Column(String)
#     Specialization = Column(String)
#     Email = Column(String, unique=True)
#     PhoneNumber = Column(Integer, unique=True)
#     DepartmentID = Column(Integer, ForeignKey('departments.DepartmentID'))

#     appointments = relationship("Appointment", backref='doctor')
#     prescriptions = relationship("Prescription", backref='doctor')

#     def __init__(self, doctor_id, first_name, last_name, specialization, email, phone_number, department_id):
#         self.DoctorID = doctor_id
#         self.First_Name = first_name
#         self.Last_Name = last_name
#         self.Specialization = specialization
#         self.Email = email
#         self.PhoneNumber = phone_number
#         self.DepartmentID = department_id


# class Nurse(Base):
#     __tablename__ = 'nurses'

#     NurseID = Column(String, primary_key=True)
#     Name = Column(String)
#     PhoneNumber = Column(Integer, unique=True)
#     DepartmentID = Column(Integer, ForeignKey('departments.DepartmentID'))


# class Department(Base):
#     __tablename__ = 'departments'

#     DepartmentID = Column(Integer, primary_key=True)
#     DepartmentName = Column(String)

#     doctors = relationship("Doctor", backref='department')

# class Appointment(Base):
#     __tablename__ = 'appointments'

#     AppointmentID = Column(Integer, primary_key=True)
#     PatientID = Column(String, ForeignKey('patients.PatientID'))
#     DoctorID = Column(String, ForeignKey('doctors.DoctorID'))
#     AppointmentDateTime = Column(Date)
#     Purpose = Column(String)


# class Prescription(Base):
#     __tablename__ = 'prescriptions'

#     PrescriptionID = Column(Integer, primary_key=True)
#     PatientID = Column(String, ForeignKey('patients.PatientID'))
#     DoctorID = Column(String, ForeignKey('doctors.DoctorID'))
#     Medication = Column(String)
#     Dosage = Column(String)
#     Frequency = Column(String)
#     Refills = Column(Integer)
#     Instructions = Column(Text)

#     def __init__(self, patient_id, doctor_id, medication, dosage, frequency, refills, instructions):
#         self.PatientID = patient_id
#         self.DoctorID = doctor_id
#         self.Medication = medication
#         self.Dosage = dosage
#         self.Frequency = frequency
#         self.Refills = refills
#         self.Instructions = instructions


# class Billing(Base):
#     __tablename__ = 'billings'

#     BillingID = Column(Integer, primary_key=True)
#     PatientID = Column(String, ForeignKey('patients.PatientID'))
#     TotalCost = Column(Float)
#     PaymentStatus = Column(String)
#     DateOfBilling = Column(Date)
