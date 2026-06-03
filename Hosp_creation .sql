/*CREATE DATABASE HospitalManagementSystem;
GO
USE HospitalManagementSystem;
GO
CREATE TABLE DEPARTMENTS(Department_ID varchar (10),
                         department_name VARCHAR(50) not null,
                         location VARCHAR(100) not null,
						 Dep_Head_ID int, 
						 D_Budget float not null,
						 D_Expenses float,
						 D_Revenue float,
						 constraint PK_Department_ID primary key (Department_ID));

create table EMPLOYEES(Emp_ID int not null, 
                      FirstName VARCHAR(50)not null,
					  LastName VARCHAR(50)not null,
					  FullName AS (FirstName + ' ' + LastName),
					  E_gender CHAR(1) CHECK (E_gender IN ('M', 'F')),
					  E_DOB date not null,
					  E_Age AS DATEDIFF(YEAR, E_DOB, GETDATE()),
					  Hire_Date date not null,
					  Emp_Email VARCHAR(100) not null,
					  Emp_Phone VARCHAR(20) not null,
					  Emp_Address VARCHAR(200),
					  ContactInfo AS (Emp_Email + ' | ' + Emp_Phone + ' | ' + Emp_Address),
					  Role_Type varchar(20) not null,
					  Dep_Id varchar (10),
					  No_Of_Shifts int not null  CHECK (No_Of_Shifts >= 0),
					  Salary DECIMAL(10,2) NOT NULL CHECK (Salary > 0),
					  Active bit,
					  constraint PK_Emp_ID primary key (Emp_ID),
					  constraint UQ_Emp_Email UNIQUE (Emp_Email),
					  constraint UQ_Emp_Phone UNIQUE (Emp_Phone),
					  constraint CHK_Hire_Date CHECK (Hire_Date > E_DOB),
					  constraint FK_Dep_Id foreign key (Dep_Id)references DEPARTMENTS (Department_ID) 
                      on delete set null on update cascade );


create table DOCTORS(Dr_ID int not null,
					 specialty VARCHAR(100) NOT NULL,
					 License_num int not null,
					 Years_of_Experience int not null check (Years_of_Experience>=0),
					 Consultation_fee float ,
					 available_schedule VARCHAR(200),
					 constraint PK_Dr_ID primary key(Dr_ID),
					 constraint FK_Dr_ID foreign key (Dr_ID) references EMPLOYEES (Emp_ID)
                     on delete cascade on update cascade);
create table NURSES (N_ID int not null,
                     available_schedule VARCHAR(200),
					 constraint PK_N_ID primary key (N_ID),
					 constraint FK_N_ID foreign key (N_ID) references EMPLOYEES (Emp_ID)
                      on delete cascade on update cascade);
CREATE table TECHNICIANS(T_ID INT NOT NULL,
                        lab_specialization VARCHAR(100),
						lab_access_level VARCHAR(50),
						available_schedule VARCHAR(200),
						constraint PK_T_ID primary key(T_ID),
					    constraint FK_T_ID foreign key (T_ID) references EMPLOYEES (Emp_ID)
                         on delete cascade on update cascade);
create table RECEPTIONIST(Recep_ID int not null,
                          available_schedule VARCHAR(200),
						  Years_of_experience float,
						  constraint PK_Recep_ID primary key(Recep_ID),
					      constraint FK_Recep_ID foreign key (Recep_ID) references EMPLOYEES (Emp_ID)
                           on delete cascade on update cascade);
create table BILLING_STAFF(B_Staff_ID int not null,
                           drawer_id INT,
						   available_schedule VARCHAR(200),
						   Authority_Limit decimal(10,2),
						   constraint PK_B_Staff_ID primary key(B_Staff_ID),
					       constraint FK_B_Staff_ID foreign key (B_Staff_ID) references EMPLOYEES (Emp_ID)
                            on delete cascade on update cascade);

CREATE TABLE ATTENDANCE(LogID int IDENTITY(1, 1),
                        Employee_ID int not null,
						CheckInTime datetime,
						CheckoutTime datetime,
						constraint PK_LogID primary key (LogID),
						constraint FK_Attendance_Employee FOREIGN KEY (Employee_ID) references EMPLOYEES(Emp_ID)
                         on delete cascade on update cascade);

create table PATIENTS(Patient_ID INT not null, 
					 First_name VARCHAR(50) NOT NULL,
					 Last_name VARCHAR(50) NOT NULL,
					 FullName AS (First_name + ' ' + Last_name),
					 P_DOB DATE NOT NULL,
					 P_Age AS DATEDIFF(YEAR, P_DOB, GETDATE()),
					 P_gender CHAR(1) CHECK (P_gender IN ('M', 'F')), 
					 P_phone VARCHAR(15),
					 P_Address NVARCHAR(255),
					 P_Email VARCHAR(100),
					 ContactInfo AS (P_Email + ' | ' + P_Phone + ' | ' + P_Address),
					 P_medical_history VARCHAR(200),
					 Family_medical_history VARCHAR(200),
					 insurance_num VARCHAR(50),
					 insurance_provider VARCHAR(100),
					 satisfaction_rate varchar(10),
					 created_at DATETIME DEFAULT GETDATE(),
					 constraint PK_Patient_ID primary key (Patient_ID));

create table APPOINTMENTS(Appointment_ID int identity (1,1),
                          PatientID int not null,
						  Doctor_ID int,
						  Receptionist_ID int,
						  Register_DateTime datetime,
						  Appointment_DateTime datetime,
						  Appointment_status varchar(50) check (Appointment_status in ('Scheduled', 'Completed', 'Cancelled', 'No_Show')),
						  CheckInTime datetime,
						  Visit_Reason varchar(50)
						 constraint PK_Appointment_ID primary key (Appointment_ID),
						 constraint FK_Appointment_Patient FOREIGN KEY (PatientID) REFERENCES PATIENTS(Patient_ID)
                         on delete cascade on update cascade,
						 constraint FK_Appointment_Doctor FOREIGN KEY (Doctor_ID) REFERENCES DOCTORS(Dr_ID),
						 constraint FK_Appointment_Receptionist FOREIGN KEY (Receptionist_ID) REFERENCES RECEPTIONIST(Recep_ID));

create table INVOICES (Invoice_ID int identity(1,1),
                      Patient_ID int,
					  Billingstaff_ID int,
					  App_ID int,
					  Invoice_date datetime,
					  Paymentmethod varchar(50),
					  Total_Amount decimal(12,2),
					  Insurance_Coverage decimal(10,2),
					  Paid_Amount decimal(12,2),
					  outstanding_Amount AS (Total_Amount - Insurance_Coverage - Paid_Amount),
					  Payment_status nvarchar(255),
					  Correctionlog BIT default 0,
					  constraint PK_Invoice_ID primary key (Invoice_ID),
					  constraint FK_Invoice_Patient FOREIGN KEY (Patient_ID) REFERENCES PATIENTS(Patient_ID)
                      on delete set null on update cascade,
					  constraint FK_Invoice_BillingStaff FOREIGN KEY (Billingstaff_ID) REFERENCES Billing_Staff(B_Staff_ID)
                      on delete set null on update cascade,
					  constraint FK_App_ID FOREIGN KEY(App_ID) REFERENCES APPOINTMENTS(Appointment_ID));

CREATE TABLE Medical_Records (RecordID int identity (1,1),	  
                              AppID int not null,
							  Diagnosis varchar(200),
							  Prescription varchar(200),
							  constraint PK_RecordID primary key (RecordID),
							  constraint FK_Record_App foreign key (AppID) references APPOINTMENTS (Appointment_ID)
                              on delete cascade on update cascade);

CREATE TABLE Lab_Tests (TestID int identity (1,1),
						Tech_ID int,
						AppID int not null,
						Test_Name varchar(100),
						order_date_time datetime default GetDate(),
						Result_date_Time datetime,
						Normal_range varchar(50),
						Test_Result varchar(50), 
						Re_test_Required BIT,
						constraint PK_TestID primary key (TestID),
						constraint FK_Test_Tech foreign key (Tech_ID) references TECHNICIANS(T_ID)
                        on delete set null on update cascade,
						constraint FK_Test_App foreign key (AppID) references APPOINTMENTS(Appointment_ID)
                        on delete cascade on update cascade);

create table TREATMENT (TTT_ID int IDENTITY(1,1) ,
						AppID int not null,
						TTT_Date date,
						TTT_type varchar(100),
						Descrip varchar (100),
						Cost decimal(10,2),
						constraint PK_TreatmentID primary key (TTT_ID),
						constraint FK_TTT_APP foreign key (AppID) references APPOINTMENTS(Appointment_ID));
CREATE TABLE Lab_Tests (TestID int identity (1,1),
						Tech_ID int,
						AppID int not null,
						Test_Name varchar(100),
						order_date_time datetime,
						Result_date_Time datetime,
						Normal_range varchar(50),
						Test_Result varchar(50), 
						Re_test_Required BIT,
						constraint PK_TestID primary key (TestID),
						constraint FK_Test_Tech foreign key (Tech_ID) references TECHNICIANS(T_ID)
                        on delete set null on update cascade,
						constraint FK_Test_App foreign key (AppID) references APPOINTMENTS(Appointment_ID)
                        on delete cascade on update cascade);

create table PATIENT_FEEDBACK(FeedbackID int IDENTITY(1, 1),
							  AppID int not null,
							  Satisfaction_rating int CHECK (Satisfaction_rating IN (1,2,3,4,5)),
							  Comments varchar(200),
							  constraint PK_Feedback primary key (FeedbackID,AppID));

CREATE TABLE ROOMS (
    Room_ID varchar(10),  
    Room_Type varchar(100) not null ,                       
    capacity INT,                             
    status VARCHAR(20) CHECK (status IN ('Available', 'Occupied', 'Under Maintenance')), 
    last_serviced DATE,  
	constraint PK_Room_ID primary key (Room_ID));

CREATE TABLE Room_Assignments (
    assignment_id INT IDENTITY(1,1),
    R_id varchar(10),
    Employee_ID INT,
    patient_id INT ,
    assignment_date DATETIME DEFAULT GETDATE(),
    end_date DATETIME                 
    constraint PK_assignment_id primary key (assignment_id),
    constraint FK_Ass_Room FOREIGN KEY(R_id) REFERENCES ROOMS(Room_ID)
    on delete cascade on update cascade,
    constraint FK_Ass_Emp FOREIGN KEY (Employee_ID) REFERENCES EMPLOYEES(Emp_ID) 
    on delete set null on update cascade,
    constraint FK_Ass_Patient FOREIGN KEY (patient_id) REFERENCES PATIENTS(Patient_ID) 
    on delete set null on update cascade,
	CONSTRAINT CHK_Dates CHECK (end_date >= assignment_date));

create table Hospital_Transactions_Log (transaction_id BIGINT  IDENTITY(1, 1),
										  transaction_type varchar(50),
										  PatientID int not null,
										  Room_ID varchar(10),
										  Employee_ID int not null,
										  Event_Timestamp datetime default GetDate(),
										  Details varchar(200),
										  constraint PK_transaction_id primary key (transaction_id),
										  constraint FK_Trans_patient foreign key (PatientID) references PATIENTS(Patient_ID),
										  constraint FK_Trans_Emp foreign key (Employee_ID) references EMPLOYEES(Emp_ID),
										  constraint FK_Trans_Room foreign key (Room_ID) references ROOMS(Room_ID));

CREATE TABLE MEDICINE (
    Medicine_ID INT IDENTITY(1,1),
    Med_name VARCHAR(100) NOT NULL,
    brand VARCHAR(50),
    type VARCHAR(20) CHECK (type IN ('Tablet', 'Capsule', 'Liquid', 'Injection', 'Ointment')),
    dosage VARCHAR(50),
    stock_quantity INT CHECK (stock_quantity >= 0),
    expiry_date DATE,
    created_at DATETIME DEFAULT GETDATE(),
	constraint PK_medicine primary key (Medicine_ID));

CREATE TABLE Prescription (
    prescription_id INT IDENTITY(1, 1),
    patient_id INT not null,
    doctor_id INT,
    prescription_date DATE DEFAULT GETDATE(),
    medication_name VARCHAR(100),
    dosage VARCHAR(100),
    frequency VARCHAR(50),
    duration VARCHAR(50),
    notes VARCHAR(255),
	constraint PK_Prescription primary key (prescription_id),
    constraint FK_Prescription_patient FOREIGN KEY (patient_id) REFERENCES PATIENTS(Patient_ID)
     on delete cascade on update cascade,
    constraint FK_Prescription_dr FOREIGN KEY (doctor_id) REFERENCES DOCTORS(Dr_ID)
     on delete set null on update cascade);

CREATE TABLE PHARMACY (
    pharmacy_id INT IDENTITY(1, 1),
    medicine_id INT,
    patient_id INT,
    quantity INT,
	Presc_Id int,
    prescription_date DATE,
	constraint PK_pharmacy primary key (pharmacy_id),
    constraint FK_PH_Medicine FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
    on update cascade,
    constraint FK_PH_Patient FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
    ON DELETE CASCADE on update cascade,
	constraint FK_PH_Prescription  FOREIGN KEY (Presc_Id) REFERENCES Prescription (prescription_id));

CREATE TABLE Blood_Bank (
    Blood_id INT IDENTITY(1,1),
    Blood_type VARCHAR(3) CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    Stock_quantity INT CHECK (stock_quantity >= 0),
    Last_updated DATE,
	constraint PK_Blood_Bank primary key (Blood_id));



CREATE TABLE AMBULANCE (
    ambulance_id INT IDENTITY(1, 1),
    ambulance_number VARCHAR(10) UNIQUE,
    availability VARCHAR(15) CHECK (availability IN ('Available', 'On Duty', 'Maintenance')),
    driver_id INT,  
    last_service_date DATE,
	constraint PK_Ambulance primary key (ambulance_id),
    constraint FK_driver_id FOREIGN KEY (driver_id) REFERENCES EMPLOYEES(Emp_ID) 
    ON DELETE set null on update cascade);

CREATE TABLE Ambulance_Log (
    Amb_log_id INT IDENTITY(1,1),
    ambulance_id INT,
    patient_id INT,
    pickup_location VARCHAR(100),
    dropoff_location VARCHAR(100),
    pickup_time DATETIME,
    dropoff_time DATETIME,
    status VARCHAR(15) CHECK (status IN ('Completed', 'In Progress', 'Canceled')),
	constraint PK_Amb_log primary key (Amb_log_id),
    constraint FK_Amb_LOG_Amb FOREIGN KEY (ambulance_id) REFERENCES AMBULANCE(ambulance_id)
    ON DELETE set null on update cascade,
    constraint FK_Amb_log_Pat FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) 
    ON DELETE set null on update cascade,
    CONSTRAINT CHK_Time_Order CHECK (dropoff_time IS NULL OR dropoff_time > pickup_time));


ALTER TABLE Medical_Records
DROP COLUMN Prescription;

ALTER TABLE Medical_Records
ADD presc_id INT;

ALTER TABLE Medical_Records
ADD CONSTRAINT FK_Record_Prescription FOREIGN KEY (presc_id)REFERENCES Prescription(prescription_id);

CREATE TABLE Roles (
    Role_ID   INT IDENTITY(1,1) PRIMARY KEY,
    Role_Name VARCHAR(50) NOT NULL UNIQUE);*/

CREATE TABLE Users(
    User_ID      INT IDENTITY(1,1) PRIMARY KEY,
    Username     VARCHAR(50)  UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Role_ID      INT NOT NULL,
    Employee_ID  INT NULL,
    Patient_ID   INT NULL,
    IsActive     BIT DEFAULT 1,
    Created_At   DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Users_Role     FOREIGN KEY (Role_ID)     REFERENCES Roles(Role_ID),
    CONSTRAINT FK_Users_Employee FOREIGN KEY (Employee_ID) REFERENCES EMPLOYEES(Emp_ID) ON DELETE SET NULL,
    CONSTRAINT FK_Users_Patient  FOREIGN KEY (Patient_ID)  REFERENCES PATIENTS(Patient_ID)ON DELETE CASCADE,
    CONSTRAINT CHK_User_Type CHECK (
        (Employee_ID IS NOT NULL AND Patient_ID IS NULL) OR
        (Patient_ID  IS NOT NULL AND Employee_ID IS NULL) OR
        (Employee_ID IS NULL     AND Patient_ID IS NULL)));




INSERT INTO Roles (Role_Name) VALUES
('Admin'),
('Doctor'),
('Nurse'),
('Receptionist'),
('Accountant'),
('Technician'),
('Pharmacist'),
('Worker'),
('Patient');					