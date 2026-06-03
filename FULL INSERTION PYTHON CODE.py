import pyodbc
import random
from datetime import date, timedelta

# ==================== CONNECTION ====================
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== HELPERS ====================
def get_random_date(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date   = date(end_year, 12, 31)
    days_between = (end_date - start_date).days
    return start_date + timedelta(days=random.randrange(days_between))

# ==================== ADDRESS DATA ====================
EGYPTIAN_STREETS = [
    "El Tahrir St", "El Haram St", "Mostafa El Nahas St", "El Bahr El Azam St",
    "El Gomhoreya St", "El Nil St", "Abbas El Akkad St", "El Salam St",
    "El Fardous St", "El Malek Faisal St", "El Moez St", "Ramses St",
    "Port Said St", "Alexandria Desert Rd", "El Musheer Tantawy St",
    "Salah Salem St", "Mohamed Naguib St", "El Nasr St",
    "Al Madinah Al Munawwarah St", "Corniche St",
]

EGYPTIAN_CITIES = [
    "Cairo", "Alexandria", "Giza", "Mansoura", "Tanta",
    "Assiut", "Zagazig", "Ismailia", "Sohag", "Luxor",
    "Aswan", "Fayoum", "Benha", "Minya", "Damietta",
    "Port Said", "Suez", "Sharm El Sheikh", "Hurghada", "Marsa Matrouh",
]

def get_random_address():
    return f"{random.randint(1, 200)} {random.choice(EGYPTIAN_STREETS)}, {random.choice(EGYPTIAN_CITIES)}"

# ==================== DEPARTMENT / SPECIALTY DATA ====================
DEPARTMENT_SPECIALTIES = [
    ("Emergency",        "Emergency Medicine",      600),
    ("Surgery",          "General Surgery",         1200),
    ("Cardiology",       "Cardiology",              1500),
    ("Oncology",         "Oncology",                2500),
    ("ICU",              "Intensive Care",          15000),
    ("Radiology",        "Radiology",               700),
    ("Obstetrics",       "Obstetrics & Gynecology", 1300),
    ("Pharmacy",         "Pharmacy",                400),
    ("Laboratory",       "Laboratory Medicine",     500),
    ("Rehabilitation",   "Rehabilitation",          700),
    ("IT",               "Information Technology",  300),
    ("Maintenance",      "Maintenance",             300),
    ("HR",               "Human Resources",         300),
    ("Billing",          "Billing & Finance",       300),
    ("Neurology",        "Neurology",               1400),
    ("Gastroenterology", "Gastroenterology",        1100),
    ("Nephrology",       "Nephrology",              1400),
    ("Pulmonology",      "Pulmonology",             1000),
    ("Pediatrics",       "Pediatrics",              700),
]

EXCLUDED_DOCTOR_DEPTS = {
    "Billing & Finance", "Information Technology",
    "Rehabilitation", "Maintenance", "Human Resources"
}

SPECIALTY_FEE_RANGES = {
    "Oncology":                (1200, 2500),
    "Neurology":               (1000, 1800),
    "Cardiology":              (800,  1500),
    "Obstetrics & Gynecology": (700,  1300),
    "Gastroenterology":        (600,  1100),
    "Pulmonology":             (600,  1000),
    "Pediatrics":              (400,   800),
    "General Surgery":         (700,  1200),
    "Nephrology":              (800,  1400),
    "ICU":                     (5000, 15000),
    "Emergency Medicine":      (400,   600),
    "Radiology":               (500,   700),
    "Pharmacy":                (300,   400),
    "Laboratory Medicine":     (300,   500),
}

def get_specialty_and_fee(dept_id):
    idx = int(dept_id) - 1
    if 0 <= idx < len(DEPARTMENT_SPECIALTIES):
        _, specialty, base_fee = DEPARTMENT_SPECIALTIES[idx]

        if specialty in EXCLUDED_DOCTOR_DEPTS:
            return None, None

        if specialty in SPECIALTY_FEE_RANGES:
            low, high = SPECIALTY_FEE_RANGES[specialty]
            fee = round(random.uniform(low, high), 2)
        else:
            # fallback ±15% من السعر الأساسي
            fee = round(random.uniform(base_fee * 0.85, base_fee * 1.15), 2)

        return specialty, fee
    return "General", 500.0

# ==================== SCHEDULE DATA ====================
SCHEDULE_GROUPS_DOCTORS = ["Sat & Sun", "Mon & Tue", "Wed & Thu"]
SCHEDULE_FULL_WEEK      = "Sat - Thu"
NURSE_SCHEDULES         = ["Sat & Sun", "Mon & Tue", "Wed & Thu", "Sat, Mon & Wed", "Sun, Tue & Thu"]
RECEPTIONIST_SCHEDULES  = ["Sat & Sun", "Mon & Tue", "Wed & Thu", "Sat, Mon & Wed", "Sun, Tue & Thu"]
BILLING_SCHEDULES       = ["Sat & Sun", "Mon & Tue", "Wed & Thu", "Sat, Mon & Wed", "Sun, Tue & Thu"]
TECH_SCHEDULES          = ["Sat & Sun", "Mon & Tue", "Wed & Thu", "Sat, Mon & Wed", "Sun, Tue & Thu", SCHEDULE_FULL_WEEK]

LAB_SPECIALIZATIONS = [
    "Biochemistry", "Hematology", "Microbiology",
    "Immunology", "Molecular Biology", "Histopathology", "Toxicology",
]
LAB_ACCESS_LEVELS = ["Junior", "Senior", "Consultant", "Specialist"]

# ==================== NAME DATA ====================
FIRST_NAMES = [
    "Ahmed", "Sara", "Mohamed", "Mona", "Omar", "Layla",
    "Khaled", "Hoda", "Youssef", "Nour", "Ali", "Dina",
    "Hassan", "Rana", "Karim", "Yasmin",
]
LAST_NAMES = [
    "Zaki", "Salem", "Ali", "Mansour", "Fayed", "Hassan",
    "Radwan", "Ibrahim", "Mostafa", "Gamal", "Nasser",
    "Farouk", "Saber", "Younes",
]

# في الأعلى مع باقي المتغيرات العامة
used_email_numbers = set()

def make_email(fname):
    while True:
        num = random.randint(100, 9999)
        if num not in used_email_numbers:
            used_email_numbers.add(num)
            return f"{fname.lower()}{num}@gmail.com"

# ==================== MAIN ====================
def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ---------- Employee distribution ----------
        active_dist = {
            "Doctor": 30, "Nurse": 90, "Technician": 10,
            "Pharmacist": 5, "Receptionist": 10, "Accountant": 5, "Worker": 40,
        }
        inactive_dist = {
            "Doctor": 30, "Nurse": 55, "Technician": 15,
            "Pharmacist": 10, "Receptionist": 15, "Accountant": 12, "Worker": 33,
        }

        current_id = 1001

        def generate_data(dist, is_active_target):
            nonlocal current_id
            temp = []
            for role, count in dist.items():
                for _ in range(count):
                    dob    = get_random_date(1960, 2003)
                    age    = date.today().year - dob.year
                    status = 0 if age >= 60 else (1 if is_active_target else 0)

                    hire_year = max(2006, dob.year + 22)
                    hire_date = get_random_date(hire_year, 2026)
                    fname     = random.choice(FIRST_NAMES)
                    lname     = random.choice(LAST_NAMES)

                    temp.append({
                        "id":      current_id,
                        "fname":   fname,
                        "lname":   lname,
                        "gender":  random.choice(["M", "F"]),
                        "dob":     dob,
                        "hire":    hire_date,
                        "email":   make_email(fname),
                        "phone":   f"02{random.randint(0,2)}{random.randint(10000000,99999999)}",
                        "address": get_random_address(),
                        "role":    role,
                        "dept_id": str(random.randint(1, 19)),
                        "shifts":  random.randint(10, 20),
                        "salary":  round(random.uniform(5000, 40000), 2),
                        "active":  status,
                    })
                    current_id += 1
            return temp

        all_employees = generate_data(active_dist, True) + generate_data(inactive_dist, False)
        random.shuffle(all_employees)

        # ---------- INSERT: Departments ----------
        for i, (dept_name, _, _) in enumerate(DEPARTMENT_SPECIALTIES, 1):
            budget   = random.randint(500_000, 10_000_000)
            expenses = random.randint(500_000, budget)           # أقل من أو يساوي Budget
            revenue  = random.randint(budget, budget + 5_000_000) # أكبر من أو يساوي Budget
    
            cursor.execute(
                """INSERT INTO DEPARTMENTS
                (Department_ID, department_name, location, D_Budget, D_Expenses, D_Revenue)
                VALUES (?, ?, ?, ?, ?, ?)""",
            (str(i), dept_name,
            f"Building {random.choice(['A','B'])}",
            budget, expenses, revenue),
            )

        # ---------- INSERT: Employees + sub-tables ----------
        drawer_counter = 1

        for e in all_employees:
    # 1. تجهيز البيانات الخاصة بكل دور (Role)
            if e["role"] == "Doctor":
                specialty, fee = get_specialty_and_fee(e["dept_id"])
        
        # التأكد من استبعاد كل الأقسام الإدارية (11, 12, 13, 14)
                while specialty is None or e["dept_id"] in ('11', '12', '13', '14'):
                    e["dept_id"] = str(random.choice([i for i in range(1, 20) if i not in (11, 12, 13, 14)]))
                    specialty, fee = get_specialty_and_fee(e["dept_id"])
            
                schedule = (SCHEDULE_FULL_WEEK if specialty == "Emergency Medicine" 
                    else random.choice(SCHEDULE_GROUPS_DOCTORS))

    # 2. الآن نقوم بالإدخال في جدول EMPLOYEES (لكل الموظفين بلا استثناء)
    # نستخدم الـ e["dept_id"] الذي قد يكون تم تحديثه في خطوة الدكتور أعلاه
            cursor.execute(
                """INSERT INTO EMPLOYEES 
                (Emp_ID, FirstName, LastName, E_gender, E_DOB, Hire_Date, 
                 Emp_Email, Emp_Phone, Emp_Address, Role_Type, Dep_Id, 
                 No_Of_Shifts, Salary, Active) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (e["id"], e["fname"], e["lname"], e["gender"], e["dob"], e["hire"],
                 e["email"], e["phone"], e["address"], e["role"], e["dept_id"],
                 e["shifts"], e["salary"], e["active"])
            )

    # 3. الإدخال في الجداول الفرعية بناءً على الدور
            if e["role"] == "Doctor":
                cursor.execute(
                    """INSERT INTO DOCTORS (Dr_ID, specialty, License_num, Years_of_Experience, 
                    Consultation_fee, available_schedule) VALUES (?, ?, ?, ?, ?, ?)""",
                    (e["id"], specialty, random.randint(1000, 9999),
                    max(0, date.today().year - e["hire"].year), fee, schedule)
                )
            
            # NURSES
            elif e["role"] == "Nurse":
                cursor.execute(
                    "INSERT INTO NURSES (N_ID, available_schedule) VALUES (?, ?)",
                    (e["id"], random.choice(NURSE_SCHEDULES))
                )

            # TECHNICIANS
            elif e["role"] == "Technician":
                cursor.execute(
                    """INSERT INTO TECHNICIANS
                       (T_ID, lab_specialization, lab_access_level, available_schedule)
                       VALUES (?, ?, ?, ?)""",
                    (e["id"],
                     random.choice(LAB_SPECIALIZATIONS),
                     random.choice(LAB_ACCESS_LEVELS),
                     random.choice(TECH_SCHEDULES))
                )

            # RECEPTIONIST
            elif e["role"] == "Receptionist":
                cursor.execute(
                    """INSERT INTO RECEPTIONIST
                       (Recep_ID, available_schedule, Years_of_experience)
                       VALUES (?, ?, ?)""",
                    (e["id"],
                     random.choice(RECEPTIONIST_SCHEDULES),
                     random.randint(1, 10))
                )

            # BILLING STAFF (Accountant)
            elif e["role"] == "Accountant":
                cursor.execute(
                    """INSERT INTO BILLING_STAFF
                       (B_Staff_ID, drawer_id, available_schedule, Authority_Limit)
                       VALUES (?, ?, ?, ?)""",
                    (e["id"],
                     drawer_counter,
                     random.choice(BILLING_SCHEDULES),
                     5000)
                )
                drawer_counter += 1

        # ---------- UPDATE: Department heads ----------
        active_docs = [e["id"] for e in all_employees if e["role"] == "Doctor" and e["active"] == 1]
        for i in range(1, 20):
            if i <= len(active_docs):
                cursor.execute(
                    "UPDATE DEPARTMENTS SET Dep_Head_ID = ? WHERE Department_ID = ?",
                    (active_docs[i - 1], str(i))
                )

        conn.commit()
        print(f"✅ Done! Total inserted: {len(all_employees)} employees.")

    except Exception as ex:
        print(f"❌ Error: {ex}")
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()







import pyodbc
import random
from datetime import date, datetime, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

SHIFT_TIMES = [
    (7,  0,  15, 0),   # صباحي   07:00 → 15:00
    (15, 0,  23, 0),   # مسائي   15:00 → 23:00
    (23, 0,  7,  0),   # ليلي    23:00 → 07:00 (اليوم التالي)
]

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("SELECT Emp_ID, Active, Hire_Date FROM EMPLOYEES")
        employees = cursor.fetchall()

        START_DATE = date(2005, 1, 1)
        END_DATE   = date(2025, 12, 31)

        ACTIVE_DAYS   = 1700
        INACTIVE_DAYS = 300
        BATCH_SIZE    = 10_000

        records      = []
        total_inserted = 0

        for emp_id, active, hire_date in employees:

            emp_start = max(START_DATE,
                            hire_date.date() if hasattr(hire_date, 'date') else hire_date)
            emp_total_days = (END_DATE - emp_start).days
            if emp_total_days <= 0:
                continue

            num_days = ACTIVE_DAYS if active == 1 else INACTIVE_DAYS
            num_days = min(num_days, emp_total_days)

            # أيام عمل عشوائية فريدة (بدون تكرار نفس اليوم)
            chosen_offsets = random.sample(range(emp_total_days), num_days)

            for day_offset in chosen_offsets:
                work_date = emp_start + timedelta(days=day_offset)

                sh_in_h, sh_in_m, sh_out_h, sh_out_m = random.choice(SHIFT_TIMES)

                # تذبذب طبيعي ±15 دقيقة على الدخول
                checkin = datetime(
                    work_date.year, work_date.month, work_date.day,
                    sh_in_h, sh_in_m
                ) + timedelta(minutes=random.randint(-5, 15))

                # الشيفت الليلي ينتهي صبح اليوم التالي
                out_date = (work_date + timedelta(days=1)
                            if sh_out_h < sh_in_h else work_date)

                # تذبذب طبيعي ±15 دقيقة على الخروج
                checkout = datetime(
                    out_date.year, out_date.month, out_date.day,
                    sh_out_h, sh_out_m
                ) + timedelta(minutes=random.randint(-5, 15))

                records.append((emp_id, checkin, checkout))

                if len(records) >= BATCH_SIZE:
                    cursor.executemany(
                        """INSERT INTO ATTENDANCE (Employee_ID, CheckInTime, CheckoutTime)
                           VALUES (?, ?, ?)""",
                        records
                    )
                    conn.commit()
                    total_inserted += len(records)
                    print(f"   ↳ إجمالي مُدخَل حتى الآن: {total_inserted:,} سجل")
                    records = []

        # ── إدخال المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO ATTENDANCE (Employee_ID, CheckInTime, CheckoutTime)
                   VALUES (?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM ATTENDANCE")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي في DB: {total:,} سجل حضور.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()





import pyodbc
import random
from datetime import date, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== NAME DATA ====================
FIRST_NAMES_M = ["Ahmed", "Mohamed", "Omar", "Khaled", "Youssef", "Ali",
                 "Hassan", "Karim", "Tarek", "Mahmoud", "Ibrahim", "Mostafa",
                 "Amr", "Sherif", "Adel", "Sameh", "Wael", "Tamer"]

FIRST_NAMES_F = ["Sara", "Mona", "Layla", "Hoda", "Nour", "Dina", "Rana",
                 "Yasmin", "Rania", "Mariam", "Fatma", "Eman", "Noha",
                 "Heba", "Ghada", "Samar", "Amira", "Sherine"]

LAST_NAMES = ["Zaki", "Salem", "Ali", "Mansour", "Fayed", "Hassan", "Radwan",
              "Ibrahim", "Mostafa", "Gamal", "Nasser", "Farouk", "Saber",
              "Younes", "Khalil", "Ragab", "Shehata", "Abdallah", "Othman",
              "Tawfik", "Barakat", "Ezz", "Fouad", "Naguib", "Selim"]

# ==================== ADDRESS DATA ====================
EGYPTIAN_STREETS = [
    "El Tahrir St", "El Haram St", "Mostafa El Nahas St", "El Nil St",
    "Abbas El Akkad St", "El Gomhoreya St", "Ramses St", "Salah Salem St",
    "Mohamed Naguib St", "El Nasr St", "Corniche St", "Port Said St",
    "El Moez St", "El Malek Faisal St", "El Fardous St",
]

EGYPTIAN_CITIES = [
    "Cairo", "Alexandria", "Giza", "Mansoura", "Tanta", "Assiut",
    "Zagazig", "Ismailia", "Sohag", "Luxor", "Aswan", "Fayoum",
    "Benha", "Minya", "Damietta", "Port Said", "Suez",
]

def get_random_address():
    return f"{random.randint(1, 200)} {random.choice(EGYPTIAN_STREETS)}, {random.choice(EGYPTIAN_CITIES)}"

# ==================== MEDICAL DATA ====================
MEDICAL_CONDITIONS = [
    "Hypertension", "Type 2 Diabetes", "Asthma", "Chronic Back Pain",
    "Thyroid Disorder", "Anemia", "Migraine", "Gastric Ulcer",
    "Kidney Stones", "Osteoporosis", "Heart Disease", "Arthritis",
    "Depression", "Anxiety Disorder", "None", "None", "None",  # None أكثر شيوعاً
]

FAMILY_CONDITIONS = [
    "Diabetes", "Hypertension", "Heart Disease", "Cancer", "Stroke",
    "Kidney Disease", "Thyroid Disorder", "Osteoporosis", "None", "None", "None",
]

INSURANCE_PROVIDERS = [
    "GIG Insurance", "AXA Egypt", "Allianz Egypt",
    "MetLife Egypt", "Bupa Egypt", "Egypt Insurance",
    "Delta Insurance", "Misr Insurance", None, None,  # بعضهم مش عندهم تأمين
]

SATISFACTION_RATES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
# توزيع أكثر واقعية: معظم الناس راضية (7-10)
SATISFACTION_WEIGHTS = [0.02, 0.03, 0.05, 0.07, 0.08, 0.10, 0.15, 0.20, 0.15, 0.15]

# ==================== HELPERS ====================
def get_random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randrange((end - start).days))

used_email_numbers = set()
def make_email(fname):
    while True:
        num = random.randint(100, 9999)
        if num not in used_email_numbers:
            used_email_numbers.add(num)
            return f"{fname.lower()}{num}@gmail.com"

def make_phone():
    prefix = random.choice(["010", "011", "012", "015"])
    return f"{prefix}{random.randint(10000000, 99999999)}"

def make_insurance(provider):
    if provider is None:
        return None
    return f"INS-{random.randint(100000, 999999)}"

def pick_satisfaction():
    return random.choices(SATISFACTION_RATES, weights=SATISFACTION_WEIGHTS, k=1)[0]

def pick_medical_history():
    conditions = random.sample(MEDICAL_CONDITIONS, k=random.randint(1, 3))
    conditions = [c for c in conditions if c != "None"]
    return ", ".join(conditions) if conditions else "None"

def pick_family_history():
    conditions = random.sample(FAMILY_CONDITIONS, k=random.randint(1, 2))
    conditions = [c for c in conditions if c != "None"]
    return ", ".join(conditions) if conditions else "None"

# ==================== MAIN ====================
def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        TARGET     = 10_000
        BATCH_SIZE = 1_000
        records    = []
        patient_id = 1

        for _ in range(TARGET):
            gender = random.choice(["M", "F"])
            fname  = random.choice(FIRST_NAMES_M if gender == "M" else FIRST_NAMES_F)
            lname  = random.choice(LAST_NAMES)
            dob    = get_random_date(1940, 2020)

            provider     = random.choice(INSURANCE_PROVIDERS)
            insurance_num = make_insurance(provider)

            created_at = get_random_date(2005, 2025)

            records.append((
                patient_id,
                fname,
                lname,
                dob,
                gender,
                make_phone(),
                get_random_address(),
                make_email(fname),
                pick_medical_history(),
                pick_family_history(),
                insurance_num,
                provider,
                pick_satisfaction(),
                created_at,
            ))

            patient_id += 1

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO PATIENTS
                       (Patient_ID, First_name, Last_name, P_DOB, P_gender,
                        P_phone, P_Address, P_Email, P_medical_history,
                        Family_medical_history, insurance_num, insurance_provider,
                        satisfaction_rate, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                print(f"   ↳ تم إدخال {patient_id - 1:,} مريض حتى الآن...")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO PATIENTS
                   (Patient_ID, First_name, Last_name, P_DOB, P_gender,
                    P_phone, P_Address, P_Email, P_medical_history,
                    Family_medical_history, insurance_num, insurance_provider,
                    satisfaction_rate, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()

        cursor.execute("SELECT COUNT(*) FROM PATIENTS")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي: {total:,} مريض.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()






import pyodbc
import random
from datetime import date, datetime, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

VISIT_REASONS = [
    "Routine Checkup", "Follow-up", "Emergency", "Consultation",
    "Lab Results Review", "Vaccination", "Surgery Consultation",
    "Chronic Disease Management", "Second Opinion", "Pre-operative Assessment",
    "Post-operative Follow-up", "Pain Management", "Mental Health Consultation",
    "Pediatric Checkup", "Prenatal Care", "Cardiac Evaluation",
    "Respiratory Issues", "Digestive Problems", "Neurological Assessment",
    "Orthopedic Consultation",
]

APPOINTMENT_STATUS_WEIGHTS = [
    ("Completed",  0.65),
    ("Cancelled",  0.15),
    ("No_Show",    0.10),
    ("Scheduled",  0.10),   # المواعيد المستقبلية فقط
]

def pick_status(app_datetime):
    """المواعيد المستقبلية = Scheduled فقط، الماضية = باقي الحالات"""
    if app_datetime > datetime.now():
        return "Scheduled"
    statuses = [s for s, _ in APPOINTMENT_STATUS_WEIGHTS if s != "Scheduled"]
    weights  = [w for s, w in APPOINTMENT_STATUS_WEIGHTS if s != "Scheduled"]
    # إعادة تطبيع الأوزان
    total    = sum(weights)
    weights  = [w / total for w in weights]
    return random.choices(statuses, weights=weights, k=1)[0]

def random_datetime(start_date, end_date):
    delta = (end_date - start_date).days
    rand_day  = start_date + timedelta(days=random.randint(0, delta))
    rand_hour = random.randint(8, 17)   # مواعيد من 8 صباحاً لـ 5 مساءً
    rand_min  = random.choice([0, 15, 30, 45])
    return datetime(rand_day.year, rand_day.month, rand_day.day, rand_hour, rand_min)

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب الـ IDs من الجداول الموجودة ──
        cursor.execute("SELECT Patient_ID FROM PATIENTS")
        patient_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT Dr_ID FROM DOCTORS")
        doctor_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT Recep_ID FROM RECEPTIONIST")
        receptionist_ids = [r[0] for r in cursor.fetchall()]

        if not patient_ids or not doctor_ids or not receptionist_ids:
            print("❌ تأكد إن جداول PATIENTS و DOCTORS و RECEPTIONIST فيها بيانات.")
            return

        START_DATE = date(2005, 1, 1)
        END_DATE   = date(2026, 6, 30)   # بعض المواعيد مستقبلية = Scheduled
        TARGET     = 500_000
        BATCH_SIZE = 10_000

        records       = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} موعد...")

        for _ in range(TARGET):

            app_datetime = random_datetime(START_DATE, END_DATE)

            # Register قبل الموعد بـ 1 لـ 30 يوم
            register_dt  = app_datetime - timedelta(days=random.randint(1, 30),
                                                     hours=random.randint(0, 23))

            status = pick_status(app_datetime)

            # CheckInTime: بس لو Completed أو No_Show (حضر ودخل)
            if status == "Completed":
                checkin = app_datetime + timedelta(minutes=random.randint(-10, 20))
            elif status == "No_Show":
                checkin = None   # ما جاش أصلاً
            else:
                checkin = None   # Cancelled / Scheduled

            records.append((
                random.choice(patient_ids),
                random.choice(doctor_ids),
                random.choice(receptionist_ids),
                register_dt,
                app_datetime,
                status,
                checkin,
                random.choice(VISIT_REASONS),
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO APPOINTMENTS
                       (PatientID, Doctor_ID, Receptionist_ID, Register_DateTime,
                        Appointment_DateTime, Appointment_status, CheckInTime, Visit_Reason)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} موعد")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO APPOINTMENTS
                   (PatientID, Doctor_ID, Receptionist_ID, Register_DateTime,
                    Appointment_DateTime, Appointment_status, CheckInTime, Visit_Reason)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM APPOINTMENTS")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} موعد.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()



import pyodbc
import random
from datetime import datetime, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

PAYMENT_METHODS = ["Cash", "Credit Card", "Insurance", "Bank Transfer"]

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب الـ IDs المطلوبة ──
        cursor.execute("SELECT Appointment_ID, PatientID FROM APPOINTMENTS WHERE Appointment_status = 'Completed'")
        appointments = cursor.fetchall()

        cursor.execute("SELECT B_Staff_ID FROM BILLING_STAFF")
        billing_ids = [r[0] for r in cursor.fetchall()]

        if not appointments or not billing_ids:
            print("❌ تأكد إن APPOINTMENTS و BILLING_STAFF فيهم بيانات.")
            return

        # لو المواعيد أكتر من 500,000 نعمل sample
        TARGET     = 500_000
        BATCH_SIZE = 10_000

        if len(appointments) > TARGET:
            appointments = random.sample(appointments, TARGET)
        
        # لو أقل من TARGET نكرر حتى نوصل
        while len(appointments) < TARGET:
            appointments += random.sample(appointments, min(TARGET - len(appointments), len(appointments)))

        appointments = appointments[:TARGET]

        records       = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} فاتورة...")

        for app_id, patient_id in appointments:

            total_amount = round(random.uniform(5000, 15000), 2)

            # Insurance Coverage بين 15% و 20%
            insurance_rate     = round(random.uniform(0.15, 0.20), 4)
            insurance_coverage = round(insurance_rate * total_amount, 2)

            # المبلغ المطلوب بعد التأمين
            outstanding_amount = round(total_amount - insurance_coverage, 2)

            # Paid Amount: 3 سيناريوهات
            scenario = random.choices(
                ["paid", "unpaid", "partial"],
                weights=[0.60, 0.15, 0.25],
                k=1
            )[0]

            if scenario == "paid":
                paid_amount    = outstanding_amount
                payment_status = "Paid"

            elif scenario == "unpaid":
                paid_amount    = round(insurance_coverage, 2)
                payment_status = "Unpaid"

            else:  # partial
                # أقل من outstanding وأكبر من insurance فقط
                paid_amount = round(
                    random.uniform(insurance_coverage, outstanding_amount - 0.01), 2
                )
                payment_status = "Partial Paid"

            # Correction log: 5% فيهم تصحيح
            correction_log = 1 if random.random() < 0.05 else 0

            # Invoice date بعد الموعد بـ 0 لـ 2 يوم
            invoice_date = datetime.now() - timedelta(
                days=random.randint(0, 7300),
                hours=random.randint(0, 8)
            )

            records.append((
                patient_id,
                random.choice(billing_ids),
                app_id,
                invoice_date,
                random.choice(PAYMENT_METHODS),
                total_amount,
                insurance_coverage,
                paid_amount,
                outstanding_amount,
                payment_status,
                correction_log,
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO INVOICES
                       (Patient_ID, Billingstaff_ID, App_ID, Invoice_date,
                        Paymentmethod, Total_Amount, Insurance_Coverage,
                        Paid_Amount, outstanding_Amount, Payment_status, Correctionlog)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} فاتورة")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO INVOICES
                   (Patient_ID, Billingstaff_ID, App_ID, Invoice_date,
                    Paymentmethod, Total_Amount, Insurance_Coverage,
                    Paid_Amount, outstanding_Amount, Payment_status, Correctionlog)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM INVOICES")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} فاتورة.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()




import pyodbc
import random
from datetime import date, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== MEDICATION DATA ====================

MEDICATION_DATA = {
    "Cardiology": [
        ("Amlodipine",       "5mg",    "Once daily",       "3 months",  "Take in the morning"),
        ("Amlodipine",       "10mg",   "Once daily",       "6 months",  "Monitor blood pressure weekly"),
        ("Lisinopril",       "5mg",    "Once daily",       "3 months",  "Monitor kidney function"),
        ("Lisinopril",       "10mg",   "Once daily",       "6 months",  "Avoid potassium supplements"),
        ("Metoprolol",       "50mg",   "Twice daily",      "3 months",  "Do not stop suddenly"),
        ("Bisoprolol",       "5mg",    "Once daily",       "6 months",  "Take at the same time daily"),
        ("Atorvastatin",     "20mg",   "Once at night",    "6 months",  "Avoid grapefruit juice"),
        ("Atorvastatin",     "40mg",   "Once at night",    "6 months",  "Report muscle pain immediately"),
        ("Aspirin",          "100mg",  "Once daily",       "Ongoing",   "Take after meals"),
        ("Warfarin",         "5mg",    "Once daily",       "Ongoing",   "Regular INR monitoring required"),
        ("Furosemide",       "40mg",   "Once daily",       "1 month",   "Monitor electrolytes"),
        ("Carvedilol",       "6.25mg", "Twice daily",      "3 months",  "Take with food"),
        ("Spironolactone",   "25mg",   "Once daily",       "3 months",  "Monitor potassium levels"),
        ("Apixaban",         "5mg",    "Twice daily",      "6 months",  "Do not crush tablet"),
        ("Digoxin",          "0.125mg","Once daily",       "Ongoing",   "Monitor heart rate daily"),
    ],
    "Neurology": [
        ("Sumatriptan",      "50mg",   "As needed",        "As needed", "Max 2 doses per 24 hours"),
        ("Topiramate",       "25mg",   "Twice daily",      "6 months",  "Stay well hydrated"),
        ("Levetiracetam",    "500mg",  "Twice daily",      "1 year",    "Do not stop without doctor advice"),
        ("Valproate",        "500mg",  "Twice daily",      "1 year",    "Regular liver function tests needed"),
        ("Amitriptyline",    "25mg",   "Once at night",    "3 months",  "May cause drowsiness"),
        ("Gabapentin",       "300mg",  "Three times daily","6 months",  "Avoid driving initially"),
        ("Pregabalin",       "75mg",   "Twice daily",      "3 months",  "Do not stop suddenly"),
        ("Donepezil",        "10mg",   "Once daily",       "Ongoing",   "Take at bedtime"),
        ("Memantine",        "10mg",   "Twice daily",      "Ongoing",   "Can be taken with or without food"),
        ("Betahistine",      "16mg",   "Three times daily","2 months",  "Take with food"),
        ("Propranolol",      "40mg",   "Twice daily",      "3 months",  "Monitor pulse rate"),
        ("Carbidopa-Levodopa","25/100mg","Three times daily","Ongoing",  "Take 30 min before meals"),
    ],
    "Oncology": [
        ("Tamoxifen",        "20mg",   "Once daily",       "5 years",   "Regular gynecological check-ups"),
        ("Anastrozole",      "1mg",    "Once daily",       "5 years",   "Bone density monitoring required"),
        ("Imatinib",         "400mg",  "Once daily",       "Ongoing",   "Take with large glass of water"),
        ("Methotrexate",     "15mg",   "Once weekly",      "6 months",  "Avoid alcohol completely"),
        ("Dexamethasone",    "8mg",    "Once daily",       "2 weeks",   "Take with food, taper dose"),
        ("Ondansetron",      "8mg",    "As needed",        "During chemo","Take 30 min before chemotherapy"),
        ("Capecitabine",     "1500mg", "Twice daily",      "6 months",  "Take within 30 min after meals"),
    ],
    "Gastroenterology": [
        ("Omeprazole",       "20mg",   "Twice daily",      "4 weeks",   "Take 30 min before meals"),
        ("Pantoprazole",     "40mg",   "Once daily",       "4 weeks",   "Swallow whole, do not crush"),
        ("Mesalazine",       "800mg",  "Three times daily","3 months",  "Regular blood tests needed"),
        ("Lactulose",        "15ml",   "Twice daily",      "1 month",   "Mix with water or juice"),
        ("Domperidone",      "10mg",   "Three times daily","2 weeks",   "Take 15-30 min before meals"),
        ("Mebeverine",       "135mg",  "Three times daily","2 months",  "Take 20 min before meals"),
        ("Ursodeoxycholic Acid","300mg","Twice daily",     "6 months",  "Take with food"),
        ("Rifaximin",        "550mg",  "Twice daily",      "2 weeks",   "Complete full course"),
        ("Prednisolone",     "40mg",   "Once daily",       "6 weeks",   "Taper dose gradually"),
    ],
    "Pulmonology": [
        ("Salbutamol",       "100mcg", "As needed",        "Ongoing",   "Shake inhaler before use"),
        ("Budesonide",       "200mcg", "Twice daily",      "3 months",  "Rinse mouth after use"),
        ("Tiotropium",       "18mcg",  "Once daily",       "Ongoing",   "Use at same time each day"),
        ("Montelukast",      "10mg",   "Once daily",       "3 months",  "Take in the evening"),
        ("Amoxicillin",      "500mg",  "Three times daily","7 days",    "Complete full course"),
        ("Azithromycin",     "500mg",  "Once daily",       "5 days",    "Take on empty stomach"),
        ("Prednisolone",     "30mg",   "Once daily",       "5 days",    "Take with food in morning"),
        ("Salmeterol",       "50mcg",  "Twice daily",      "3 months",  "Not for acute attacks"),
    ],
    "Nephrology": [
        ("Amlodipine",       "10mg",   "Once daily",       "Ongoing",   "Monitor blood pressure daily"),
        ("Furosemide",       "80mg",   "Twice daily",      "Ongoing",   "Monitor electrolytes weekly"),
        ("Sodium Bicarbonate","650mg", "Twice daily",      "3 months",  "Take between meals"),
        ("Calcium Carbonate","500mg",  "With meals",       "Ongoing",   "Take with each main meal"),
        ("Allopurinol",      "100mg",  "Once daily",       "Ongoing",   "Take after meals"),
        ("Enalapril",        "5mg",    "Once daily",       "Ongoing",   "Monitor potassium levels"),
        ("Ciprofloxacin",    "500mg",  "Twice daily",      "7 days",    "Complete full course, stay hydrated"),
    ],
    "Obstetrics & Gynecology": [
        ("Folic Acid",       "5mg",    "Once daily",       "3 months",  "Take before and during pregnancy"),
        ("Metformin",        "500mg",  "Twice daily",      "3 months",  "Take with meals"),
        ("Progesterone",     "200mg",  "Once daily",       "12 weeks",  "Take at bedtime"),
        ("Labetalol",        "100mg",  "Twice daily",      "Until delivery","Monitor blood pressure"),
        ("Clomiphene",       "50mg",   "Once daily",       "5 days",    "Take days 2-6 of cycle"),
        ("Dienogest",        "2mg",    "Once daily",       "6 months",  "Take at same time daily"),
        ("Iron Supplement",  "325mg",  "Once daily",       "3 months",  "Take on empty stomach with vitamin C"),
    ],
    "Pediatrics": [
        ("Amoxicillin",      "250mg/5ml","Three times daily","10 days", "Complete full course"),
        ("Paracetamol",      "15mg/kg","Every 6 hours",    "As needed", "Do not exceed 4 doses per day"),
        ("Ibuprofen",        "10mg/kg","Every 8 hours",    "As needed", "Take with food"),
        ("Cetirizine",       "5mg",    "Once daily",       "2 weeks",   "Take at bedtime"),
        ("Salbutamol",       "2.5mg",  "As needed",        "As needed", "Via nebulizer"),
        ("Vitamin D",        "400 IU", "Once daily",       "3 months",  "Can be given with milk"),
        ("Ferrous Sulfate",  "3mg/kg", "Once daily",       "3 months",  "Take with orange juice"),
        ("Acyclovir",        "20mg/kg","Four times daily", "5 days",    "Stay well hydrated"),
    ],
    "General Surgery": [
        ("Cefazolin",        "1g",     "Pre-operatively",  "Single dose","IV administration"),
        ("Metronidazole",    "500mg",  "Three times daily","7 days",    "Avoid alcohol completely"),
        ("Tramadol",         "50mg",   "Every 8 hours",    "5 days",    "May cause drowsiness"),
        ("Ibuprofen",        "400mg",  "Three times daily","5 days",    "Take with food"),
        ("Enoxaparin",       "40mg",   "Once daily",       "10 days",   "Subcutaneous injection"),
        ("Omeprazole",       "20mg",   "Once daily",       "4 weeks",   "Take before breakfast"),
    ],
    "Emergency Medicine": [
        ("Aspirin",          "300mg",  "Stat",             "Single dose","Chew tablet"),
        ("Morphine",         "5mg",    "As needed",        "Short term", "IV administration only"),
        ("Adrenaline",       "0.5mg",  "Stat",             "Single dose","IM injection"),
        ("Paracetamol",      "1g",     "Every 6 hours",    "As needed",  "IV administration"),
        ("Lorazepam",        "4mg",    "Stat",             "Single dose","IV administration"),
        ("Labetalol",        "20mg",   "Stat",             "Single dose","IV slow injection"),
    ],
    "Intensive Care": [
        ("Norepinephrine",   "Titrated","Continuous infusion","ICU stay", "Monitor BP continuously"),
        ("Propofol",         "Titrated","Continuous infusion","ICU stay", "For sedation only"),
        ("Vancomycin",       "1g",     "Every 12 hours",   "7-14 days", "Monitor renal function"),
        ("Piperacillin-Tazobactam","4.5g","Every 8 hours", "7 days",    "IV administration"),
        ("Insulin",          "Per scale","Continuous",     "ICU stay",  "Monitor glucose hourly"),
        ("Dexamethasone",    "6mg",    "Once daily",       "10 days",   "IV administration"),
    ],
    "Radiology": [
        ("Ibuprofen",        "400mg",  "Three times daily","5 days",    "Take with food"),
        ("Gabapentin",       "300mg",  "Three times daily","3 months",  "For neuropathic pain"),
        ("Dexamethasone",    "4mg",    "Three times daily","2 weeks",   "Taper dose gradually"),
        ("Calcium + Vit D",  "1000mg/800IU","Once daily", "3 months",  "Take with main meal"),
    ],
    "Rehabilitation": [
        ("Ibuprofen",        "400mg",  "Three times daily","2 weeks",   "Take with food"),
        ("Baclofen",         "10mg",   "Three times daily","3 months",  "Do not stop suddenly"),
        ("Diclofenac gel",   "1%",     "Twice daily",      "2 weeks",   "Apply to affected area"),
        ("Paracetamol",      "500mg",  "Every 6 hours",    "As needed", "Max 4 doses per day"),
        ("Enoxaparin",       "40mg",   "Once daily",       "10 days",   "Subcutaneous injection"),
        ("Calcium + Vit D",  "1000mg/800IU","Once daily", "3 months",  "Take with main meal"),
    ],
    "General": [
        ("Metformin",        "500mg",  "Twice daily",      "3 months",  "Take with meals"),
        ("Levothyroxine",    "50mcg",  "Once daily",       "Ongoing",   "Take on empty stomach"),
        ("Vitamin D3",       "1000 IU","Once daily",       "3 months",  "Take with fatty meal"),
        ("Ferrous Sulfate",  "325mg",  "Once daily",       "3 months",  "Take with vitamin C"),
        ("Paracetamol",      "500mg",  "As needed",        "As needed", "Max 4 doses per day"),
        ("Cetirizine",       "10mg",   "Once daily",       "2 weeks",   "Take at bedtime"),
        ("Fluoxetine",       "20mg",   "Once daily",       "6 months",  "May take 4 weeks to work"),
        ("Sertraline",       "50mg",   "Once daily",       "6 months",  "Take with food"),
        ("Multivitamin",     "1 tablet","Once daily",      "3 months",  "Take with breakfast"),
        ("Omeprazole",       "20mg",   "Once daily",       "4 weeks",   "Take 30 min before breakfast"),
    ],
}

def get_random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randrange((end - start).days))

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب المواعيد الـ Completed مع Patient و Doctor و التخصص ──
        cursor.execute("""
            SELECT A.PatientID, A.Doctor_ID, A.Appointment_DateTime, D.specialty
            FROM APPOINTMENTS A
            JOIN DOCTORS D ON A.Doctor_ID = D.Dr_ID
            WHERE A.Appointment_status = 'Completed'
        """)
        appointments = cursor.fetchall()

        if not appointments:
            print("❌ مفيش مواعيد Completed.")
            return

        TARGET     = min(500_000, len(appointments))
        BATCH_SIZE = 10_000

        if len(appointments) > TARGET:
            appointments = random.sample(appointments, TARGET)

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} وصفة طبية...")

        for patient_id, doctor_id, app_datetime, specialty in appointments:

            key      = specialty if specialty in MEDICATION_DATA else "General"
            med      = random.choice(MEDICATION_DATA[key])
            med_name, dosage, frequency, duration, notes = med

            # تاريخ الوصفة = تاريخ الموعد
            presc_date = (app_datetime.date()
                          if hasattr(app_datetime, 'date')
                          else app_datetime)

            records.append((
                patient_id,
                doctor_id,
                presc_date,
                med_name,
                dosage,
                frequency,
                duration,
                notes,
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO Prescription
                       (patient_id, doctor_id, prescription_date, medication_name,
                        dosage, frequency, duration, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} وصفة")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO Prescription
                   (patient_id, doctor_id, prescription_date, medication_name,
                    dosage, frequency, duration, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM Prescription")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} وصفة طبية.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()




import pyodbc
import random

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

SPECIALTY_DIAGNOSES = {
    "Cardiology":              ["Hypertension Stage 1", "Hypertension Stage 2", "Atrial Fibrillation", "Coronary Artery Disease", "Heart Failure", "Angina Pectoris", "Myocardial Infarction", "Arrhythmia", "Mitral Valve Regurgitation"],
    "Neurology":               ["Migraine", "Tension Headache", "Epilepsy", "Parkinson's Disease", "Multiple Sclerosis", "Stroke", "Peripheral Neuropathy", "Alzheimer's Disease", "Vertigo"],
    "Oncology":                ["Breast Cancer Stage I", "Breast Cancer Stage II", "Lung Cancer", "Colorectal Cancer", "Lymphoma", "Leukemia", "Prostate Cancer", "Thyroid Cancer", "Skin Melanoma"],
    "Gastroenterology":        ["Gastric Ulcer", "GERD", "Irritable Bowel Syndrome", "Crohn's Disease", "Ulcerative Colitis", "Liver Cirrhosis", "Hepatitis B", "Hepatitis C", "Gallstones"],
    "Pulmonology":             ["Asthma", "COPD", "Pneumonia", "Pulmonary Embolism", "Bronchitis", "Tuberculosis", "Sleep Apnea", "Pleural Effusion"],
    "Nephrology":              ["Chronic Kidney Disease Stage 3", "Chronic Kidney Disease Stage 4", "Acute Kidney Injury", "Nephrotic Syndrome", "Kidney Stones", "Urinary Tract Infection", "Polycystic Kidney Disease"],
    "Obstetrics & Gynecology": ["Gestational Diabetes", "Preeclampsia", "Polycystic Ovary Syndrome", "Endometriosis", "Uterine Fibroids", "Cervical Dysplasia", "Ectopic Pregnancy", "Ovarian Cyst"],
    "Pediatrics":              ["Acute Otitis Media", "Tonsillitis", "Childhood Asthma", "Iron Deficiency Anemia", "Febrile Seizure", "Chickenpox", "RSV Bronchiolitis", "Developmental Delay"],
    "General Surgery":         ["Appendicitis", "Inguinal Hernia", "Cholecystitis", "Bowel Obstruction", "Pilonidal Cyst", "Varicose Veins", "Hemorrhoids", "Abdominal Adhesions"],
    "Emergency Medicine":      ["Acute Chest Pain", "Severe Allergic Reaction", "Fracture", "Head Trauma", "Sepsis", "Hypertensive Crisis", "Diabetic Ketoacidosis", "Acute Abdomen"],
    "Intensive Care":          ["Multi-organ Failure", "Respiratory Failure", "Septic Shock", "Post-cardiac Arrest", "Severe Traumatic Brain Injury", "Acute Respiratory Distress Syndrome"],
    "Radiology":               ["Lung Nodule Detected", "Bone Fracture Confirmed", "Liver Mass Detected", "Spinal Stenosis", "Brain Lesion", "Pulmonary Infiltrate"],
    "Rehabilitation":          ["Post-stroke Rehabilitation", "Post-fracture Rehabilitation", "Chronic Lower Back Pain", "Knee Replacement Recovery", "Sports Injury Recovery", "Neurological Rehabilitation"],
    "General":                 ["Type 2 Diabetes", "Hypothyroidism", "Vitamin D Deficiency", "Anemia", "Obesity", "Anxiety Disorder", "Depression", "Routine Checkup - Normal", "Upper Respiratory Infection"],
}

def get_diagnosis(specialty):
    key = specialty if specialty in SPECIALTY_DIAGNOSES else "General"
    return random.choice(SPECIALTY_DIAGNOSES[key])

# ==================== MAIN ====================
def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب المواعيد الـ Completed مع تخصص الدكتور ──
        cursor.execute("""
            SELECT A.Appointment_ID, D.specialty
            FROM APPOINTMENTS A
            JOIN DOCTORS D ON A.Doctor_ID = D.Dr_ID
            WHERE A.Appointment_status = 'Completed'
        """)
        appointments = cursor.fetchall()

        if not appointments:
            print("❌ مفيش مواعيد Completed.")
            return

        # ── جيب كل الـ IDs من جدول Prescription ──
        cursor.execute("SELECT prescription_id FROM Prescription")
        presc_ids = [r[0] for r in cursor.fetchall()]

        if not presc_ids:
            print("❌ جدول Prescription فاضي، املاه الأول.")
            return

        print(f"✅ عدد الوصفات المتاحة: {len(presc_ids):,}")

        TARGET     = min(500_000, len(appointments))
        BATCH_SIZE = 10_000

        if len(appointments) > TARGET:
            appointments = random.sample(appointments, TARGET)

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} سجل طبي...")

        for app_id, specialty in appointments:
            diagnosis = get_diagnosis(specialty)
            presc_id  = random.choice(presc_ids)   # ← ID من جدول Prescription

            records.append((app_id, diagnosis, presc_id))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO Medical_Records (AppID, Diagnosis, prescription_id)
                       VALUES (?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} سجل")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO Medical_Records (AppID, Diagnosis, presc_id)
                   VALUES (?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM Medical_Records")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} سجل طبي.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()






import pyodbc
import random
from datetime import timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== TREATMENT DATA ====================

TREATMENT_DATA = {
    "Cardiology": [
        ("Medication Therapy",      "Antihypertensive medication administration",         500,   1500),
        ("ECG",                     "Electrocardiogram monitoring and analysis",           300,    800),
        ("Echocardiography",        "Cardiac ultrasound evaluation",                      1000,  3000),
        ("Cardiac Catheterization", "Coronary artery catheterization procedure",          5000, 15000),
        ("Pacemaker Implantation",  "Permanent pacemaker device implantation",           10000, 30000),
        ("Cardioversion",           "Electrical cardioversion for arrhythmia",            3000,  8000),
        ("Stress Test",             "Exercise cardiac stress testing",                     800,  2000),
        ("Holter Monitor",          "24-hour cardiac rhythm monitoring",                   600,  1500),
    ],
    "Neurology": [
        ("MRI Brain",               "Magnetic resonance imaging of brain",               2000,  5000),
        ("EEG",                     "Electroencephalogram brain activity recording",       800,  2000),
        ("Nerve Conduction Study",  "Peripheral nerve conduction velocity testing",       1000,  2500),
        ("Lumbar Puncture",         "Cerebrospinal fluid analysis procedure",             1500,  4000),
        ("Botox Injection",         "Botulinum toxin injection for migraine",             2000,  5000),
        ("Medication Therapy",      "Neurological medication administration",              500,  1500),
        ("Physical Therapy",        "Neurological rehabilitation exercises",               400,  1200),
        ("Deep Brain Stimulation",  "DBS device implantation for Parkinson",            15000, 40000),
    ],
    "Oncology": [
        ("Chemotherapy",            "Cytotoxic drug infusion session",                   3000, 10000),
        ("Radiation Therapy",       "Targeted radiation treatment session",               4000, 12000),
        ("Immunotherapy",           "Immune checkpoint inhibitor infusion",               5000, 15000),
        ("Bone Marrow Biopsy",      "Bone marrow aspiration and biopsy",                 2000,  5000),
        ("Tumor Biopsy",            "Tissue biopsy for histopathological analysis",      1500,  4000),
        ("PET Scan",                "Positron emission tomography imaging",               4000, 10000),
        ("Surgical Resection",      "Tumor surgical removal procedure",                  8000, 25000),
        ("Hormone Therapy",         "Hormonal cancer treatment administration",           1000,  3000),
    ],
    "Gastroenterology": [
        ("Endoscopy",               "Upper gastrointestinal endoscopy procedure",        1500,  4000),
        ("Colonoscopy",             "Lower gastrointestinal colonoscopy procedure",      1500,  4000),
        ("Liver Biopsy",            "Percutaneous liver tissue biopsy",                  2000,  5000),
        ("ERCP",                    "Endoscopic retrograde cholangiopancreatography",    3000,  8000),
        ("H. Pylori Treatment",     "Helicobacter pylori eradication therapy",            800,  2000),
        ("Medication Therapy",      "Gastrointestinal medication administration",         400,  1200),
        ("Nutritional Support",     "Enteral or parenteral nutritional therapy",         1000,  3000),
        ("Paracentesis",            "Abdominal fluid drainage procedure",                1500,  4000),
    ],
    "Pulmonology": [
        ("Bronchoscopy",            "Airway bronchoscopy examination procedure",         2000,  5000),
        ("Spirometry",              "Pulmonary function testing",                         500,  1500),
        ("Nebulization",            "Inhaled medication nebulizer treatment",             300,   800),
        ("Oxygen Therapy",          "Supplemental oxygen administration",                 400,  1200),
        ("Chest Physiotherapy",     "Airway clearance physiotherapy session",             400,  1000),
        ("CPAP Therapy",            "Continuous positive airway pressure therapy",        600,  1800),
        ("Pleural Drainage",        "Thoracentesis pleural fluid drainage",              2000,  5000),
        ("Pulmonary Rehabilitation","Structured lung rehabilitation program",             500,  1500),
    ],
    "Nephrology": [
        ("Hemodialysis",            "Renal replacement hemodialysis session",            1500,  4000),
        ("Peritoneal Dialysis",     "Peritoneal dialysis catheter therapy",              1200,  3500),
        ("Kidney Biopsy",           "Percutaneous renal tissue biopsy",                  2000,  5000),
        ("Renal Ultrasound",        "Kidney and urinary tract ultrasound",               600,  1500),
        ("Lithotripsy",             "Extracorporeal shock wave kidney stone treatment",  3000,  8000),
        ("Medication Therapy",      "Nephrology medication administration",               500,  1500),
        ("IV Fluid Therapy",        "Intravenous fluid resuscitation therapy",            400,  1000),
    ],
    "Obstetrics & Gynecology": [
        ("Ultrasound",              "Obstetric or gynecological ultrasound scan",         600,  1500),
        ("Prenatal Care Visit",     "Routine antenatal monitoring and assessment",        400,  1000),
        ("C-Section",               "Cesarean section surgical delivery",               5000, 15000),
        ("Normal Delivery",         "Vaginal delivery with medical supervision",         3000,  8000),
        ("Colposcopy",              "Cervical colposcopy examination procedure",         1000,  2500),
        ("Hysteroscopy",            "Uterine cavity hysteroscopy procedure",             2000,  5000),
        ("Laparoscopy",             "Gynecological laparoscopic procedure",              4000, 12000),
        ("Hormone Therapy",         "Hormonal imbalance treatment administration",        600,  1800),
    ],
    "Pediatrics": [
        ("Vaccination",             "Childhood immunization vaccine administration",      200,   500),
        ("Nebulization",            "Pediatric inhaled medication treatment",             300,   800),
        ("IV Fluid Therapy",        "Pediatric intravenous fluid therapy",               400,  1000),
        ("Phototherapy",            "Neonatal jaundice phototherapy treatment",           500,  1500),
        ("Growth Assessment",       "Pediatric growth and development evaluation",        300,   800),
        ("Hearing Test",            "Pediatric audiological hearing assessment",          400,  1000),
        ("Medication Therapy",      "Pediatric medication administration",               300,   800),
        ("Surgical Procedure",      "Minor pediatric surgical intervention",            2000,  6000),
    ],
    "General Surgery": [
        ("Appendectomy",            "Surgical removal of inflamed appendix",            4000, 12000),
        ("Cholecystectomy",         "Laparoscopic gallbladder removal surgery",          5000, 15000),
        ("Hernia Repair",           "Surgical inguinal hernia mesh repair",             4000, 10000),
        ("Hemorrhoidectomy",        "Surgical hemorrhoid removal procedure",             3000,  8000),
        ("Wound Debridement",       "Surgical wound cleaning and debridement",           1000,  3000),
        ("Laparoscopy",             "Diagnostic or therapeutic laparoscopy",            4000, 12000),
        ("Abscess Drainage",        "Surgical incision and drainage of abscess",         1500,  4000),
        ("Post-op Care",            "Post-operative wound care and monitoring",           500,  1500),
    ],
    "Emergency Medicine": [
        ("Resuscitation",           "Cardiopulmonary resuscitation procedure",           2000,  5000),
        ("IV Cannulation",          "Intravenous access and fluid administration",        300,   800),
        ("Fracture Reduction",      "Closed fracture reduction and immobilization",      1500,  4000),
        ("Wound Suturing",          "Laceration repair and wound suturing",               800,  2000),
        ("Defibrillation",          "Emergency cardiac defibrillation",                  2000,  5000),
        ("Intubation",              "Emergency endotracheal intubation",                 1500,  4000),
        ("Gastric Lavage",          "Emergency stomach washout procedure",              1000,  3000),
        ("Monitoring",              "Continuous vital signs emergency monitoring",        500,  1500),
    ],
    "Intensive Care": [
        ("Mechanical Ventilation",  "Invasive mechanical ventilation support",           3000, 10000),
        ("Central Line Insertion",  "Central venous catheter placement",                 2000,  5000),
        ("Arterial Line",           "Arterial blood pressure monitoring line",           1500,  4000),
        ("Vasopressor Therapy",     "Vasopressor drug infusion administration",          2000,  6000),
        ("Renal Replacement",       "Continuous renal replacement therapy",              3000,  8000),
        ("Sedation Management",     "ICU sedation and analgesia protocol",              1500,  4000),
        ("Nutritional Support",     "ICU parenteral or enteral nutrition",              1000,  3000),
        ("Daily ICU Care",          "Intensive care unit daily comprehensive care",      2000,  6000),
    ],
    "Radiology": [
        ("X-Ray",                   "Plain radiograph imaging",                           300,   800),
        ("CT Scan",                 "Computed tomography imaging",                       1500,  4000),
        ("MRI",                     "Magnetic resonance imaging scan",                   2000,  5000),
        ("Ultrasound",              "Diagnostic ultrasound imaging",                      600,  1500),
        ("Mammography",             "Breast mammography screening",                       800,  2000),
        ("Bone Density Scan",       "DEXA bone mineral density scan",                    800,  2000),
        ("Contrast Study",          "Contrast-enhanced radiological study",              1500,  4000),
        ("Interventional Radiology","Image-guided interventional procedure",             3000,  8000),
    ],
    "Rehabilitation": [
        ("Physiotherapy",           "Physical rehabilitation therapy session",            400,  1200),
        ("Occupational Therapy",    "Functional occupational therapy session",            400,  1200),
        ("Speech Therapy",          "Speech and language rehabilitation session",         400,  1200),
        ("Hydrotherapy",            "Aquatic rehabilitation therapy session",             500,  1500),
        ("TENS Therapy",            "Transcutaneous electrical nerve stimulation",        300,   800),
        ("Ultrasound Therapy",      "Therapeutic ultrasound rehabilitation",              300,   800),
        ("Massage Therapy",         "Therapeutic medical massage session",                400,  1000),
        ("Exercise Program",        "Customized rehabilitation exercise program",         300,   800),
    ],
    "General": [
        ("Consultation",            "General physician consultation and assessment",      300,   800),
        ("Blood Test",              "Complete blood count and biochemistry panel",        400,  1000),
        ("Vaccination",             "Adult immunization vaccine administration",          200,   500),
        ("Medication Therapy",      "General medication administration",                  300,   800),
        ("Wound Dressing",          "Wound care and dressing change",                    200,   600),
        ("IV Fluid Therapy",        "Intravenous fluid administration",                   400,  1000),
        ("Dietary Counseling",      "Nutritional and dietary counseling session",         300,   700),
        ("Health Screening",        "Comprehensive health screening assessment",          500,  1500),
    ],
}

SPECIALTY_MAP = {
    "Cardiology":              "Cardiology",
    "Neurology":               "Neurology",
    "Oncology":                "Oncology",
    "Gastroenterology":        "Gastroenterology",
    "Pulmonology":             "Pulmonology",
    "Nephrology":              "Nephrology",
    "Obstetrics & Gynecology": "Obstetrics & Gynecology",
    "Pediatrics":              "Pediatrics",
    "General Surgery":         "General Surgery",
    "Emergency Medicine":      "Emergency Medicine",
    "Intensive Care":          "Intensive Care",
    "Radiology":               "Radiology",
    "Rehabilitation":          "Rehabilitation",
}

def get_treatment(specialty):
    key = specialty if specialty in TREATMENT_DATA else "General"
    ttt_type, descrip, cost_min, cost_max = random.choice(TREATMENT_DATA[key])
    cost = round(random.uniform(cost_min, cost_max), 2)
    return ttt_type, descrip, cost

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب المواعيد الـ Completed مع التاريخ والتخصص ──
        cursor.execute("""
            SELECT A.Appointment_ID, A.Appointment_DateTime, D.specialty
            FROM APPOINTMENTS A
            JOIN DOCTORS D ON A.Doctor_ID = D.Dr_ID
            WHERE A.Appointment_status = 'Completed'
        """)
        appointments = cursor.fetchall()

        if not appointments:
            print("❌ مفيش مواعيد Completed.")
            return

        TARGET     = min(500_000, len(appointments))
        BATCH_SIZE = 10_000

        if len(appointments) > TARGET:
            appointments = random.sample(appointments, TARGET)

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} سجل علاج...")

        for app_id, app_datetime, specialty in appointments:

            # TTT_Date = نفس يوم الموعد أو اليوم اللي بعده
            app_date = (app_datetime.date()
                        if hasattr(app_datetime, 'date') else app_datetime)
            ttt_date = app_date + timedelta(days=random.randint(0, 1))

            ttt_type, descrip, cost = get_treatment(specialty)

            records.append((app_id, ttt_date, ttt_type, descrip, cost))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO TREATMENT (AppID, TTT_Date, TTT_type, Descrip, Cost)
                       VALUES (?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} سجل")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO TREATMENT (AppID, TTT_Date, TTT_type, Descrip, Cost)
                   VALUES (?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM TREATMENT")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} سجل علاج.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()




import pyodbc
import random
from datetime import date, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== 2000 UNIQUE MEDICINES ====================

MEDICINES = [
    # === CARDIOVASCULAR ===
    ("Amlodipine 5mg",              "Norvasc",          "Tablet",    "5mg"),
    ("Amlodipine 10mg",             "Norvasc",          "Tablet",    "10mg"),
    ("Lisinopril 5mg",              "Zestril",          "Tablet",    "5mg"),
    ("Lisinopril 10mg",             "Zestril",          "Tablet",    "10mg"),
    ("Lisinopril 20mg",             "Zestril",          "Tablet",    "20mg"),
    ("Metoprolol 25mg",             "Lopressor",        "Tablet",    "25mg"),
    ("Metoprolol 50mg",             "Lopressor",        "Tablet",    "50mg"),
    ("Metoprolol 100mg",            "Lopressor",        "Tablet",    "100mg"),
    ("Bisoprolol 2.5mg",            "Concor",           "Tablet",    "2.5mg"),
    ("Bisoprolol 5mg",              "Concor",           "Tablet",    "5mg"),
    ("Bisoprolol 10mg",             "Concor",           "Tablet",    "10mg"),
    ("Atorvastatin 10mg",           "Lipitor",          "Tablet",    "10mg"),
    ("Atorvastatin 20mg",           "Lipitor",          "Tablet",    "20mg"),
    ("Atorvastatin 40mg",           "Lipitor",          "Tablet",    "40mg"),
    ("Atorvastatin 80mg",           "Lipitor",          "Tablet",    "80mg"),
    ("Rosuvastatin 5mg",            "Crestor",          "Tablet",    "5mg"),
    ("Rosuvastatin 10mg",           "Crestor",          "Tablet",    "10mg"),
    ("Rosuvastatin 20mg",           "Crestor",          "Tablet",    "20mg"),
    ("Rosuvastatin 40mg",           "Crestor",          "Tablet",    "40mg"),
    ("Simvastatin 10mg",            "Zocor",            "Tablet",    "10mg"),
    ("Simvastatin 20mg",            "Zocor",            "Tablet",    "20mg"),
    ("Simvastatin 40mg",            "Zocor",            "Tablet",    "40mg"),
    ("Aspirin 75mg",                "Aspocid",          "Tablet",    "75mg"),
    ("Aspirin 100mg",               "Aspocid",          "Tablet",    "100mg"),
    ("Aspirin 300mg",               "Aspocid",          "Tablet",    "300mg"),
    ("Warfarin 1mg",                "Coumadin",         "Tablet",    "1mg"),
    ("Warfarin 2mg",                "Coumadin",         "Tablet",    "2mg"),
    ("Warfarin 5mg",                "Coumadin",         "Tablet",    "5mg"),
    ("Furosemide 20mg",             "Lasix",            "Tablet",    "20mg"),
    ("Furosemide 40mg",             "Lasix",            "Tablet",    "40mg"),
    ("Furosemide 80mg",             "Lasix",            "Tablet",    "80mg"),
    ("Furosemide 10mg/ml",          "Lasix",            "Injection", "10mg/ml"),
    ("Furosemide 20mg/2ml",         "Lasix",            "Injection", "20mg/2ml"),
    ("Carvedilol 3.125mg",          "Coreg",            "Tablet",    "3.125mg"),
    ("Carvedilol 6.25mg",           "Coreg",            "Tablet",    "6.25mg"),
    ("Carvedilol 12.5mg",           "Coreg",            "Tablet",    "12.5mg"),
    ("Carvedilol 25mg",             "Coreg",            "Tablet",    "25mg"),
    ("Spironolactone 25mg",         "Aldactone",        "Tablet",    "25mg"),
    ("Spironolactone 50mg",         "Aldactone",        "Tablet",    "50mg"),
    ("Spironolactone 100mg",        "Aldactone",        "Tablet",    "100mg"),
    ("Apixaban 2.5mg",              "Eliquis",          "Tablet",    "2.5mg"),
    ("Apixaban 5mg",                "Eliquis",          "Tablet",    "5mg"),
    ("Rivaroxaban 10mg",            "Xarelto",          "Tablet",    "10mg"),
    ("Rivaroxaban 15mg",            "Xarelto",          "Tablet",    "15mg"),
    ("Rivaroxaban 20mg",            "Xarelto",          "Tablet",    "20mg"),
    ("Dabigatran 75mg",             "Pradaxa",          "Capsule",   "75mg"),
    ("Dabigatran 110mg",            "Pradaxa",          "Capsule",   "110mg"),
    ("Dabigatran 150mg",            "Pradaxa",          "Capsule",   "150mg"),
    ("Digoxin 0.0625mg",            "Lanoxin",          "Tablet",    "0.0625mg"),
    ("Digoxin 0.125mg",             "Lanoxin",          "Tablet",    "0.125mg"),
    ("Digoxin 0.25mg",              "Lanoxin",          "Tablet",    "0.25mg"),
    ("Ramipril 1.25mg",             "Tritace",          "Tablet",    "1.25mg"),
    ("Ramipril 2.5mg",              "Tritace",          "Tablet",    "2.5mg"),
    ("Ramipril 5mg",                "Tritace",          "Tablet",    "5mg"),
    ("Ramipril 10mg",               "Tritace",          "Tablet",    "10mg"),
    ("Amiodarone 100mg",            "Cordarone",        "Tablet",    "100mg"),
    ("Amiodarone 200mg",            "Cordarone",        "Tablet",    "200mg"),
    ("Amiodarone 150mg/3ml",        "Cordarone",        "Injection", "150mg/3ml"),
    ("Amiodarone 300mg/6ml",        "Cordarone",        "Injection", "300mg/6ml"),
    ("Clopidogrel 75mg",            "Plavix",           "Tablet",    "75mg"),
    ("Clopidogrel 300mg",           "Plavix",           "Tablet",    "300mg"),
    ("Valsartan 40mg",              "Diovan",           "Tablet",    "40mg"),
    ("Valsartan 80mg",              "Diovan",           "Tablet",    "80mg"),
    ("Valsartan 160mg",             "Diovan",           "Tablet",    "160mg"),
    ("Valsartan 320mg",             "Diovan",           "Tablet",    "320mg"),
    ("Losartan 25mg",               "Cozaar",           "Tablet",    "25mg"),
    ("Losartan 50mg",               "Cozaar",           "Tablet",    "50mg"),
    ("Losartan 100mg",              "Cozaar",           "Tablet",    "100mg"),
    ("Telmisartan 20mg",            "Micardis",         "Tablet",    "20mg"),
    ("Telmisartan 40mg",            "Micardis",         "Tablet",    "40mg"),
    ("Telmisartan 80mg",            "Micardis",         "Tablet",    "80mg"),
    ("Nifedipine 10mg",             "Adalat",           "Tablet",    "10mg"),
    ("Nifedipine 20mg",             "Adalat",           "Tablet",    "20mg"),
    ("Nifedipine 30mg",             "Adalat",           "Tablet",    "30mg"),
    ("Diltiazem 30mg",              "Cardizem",         "Tablet",    "30mg"),
    ("Diltiazem 60mg",              "Cardizem",         "Tablet",    "60mg"),
    ("Diltiazem 120mg",             "Cardizem",         "Tablet",    "120mg"),
    ("Isosorbide Mononitrate 20mg", "Imdur",            "Tablet",    "20mg"),
    ("Isosorbide Mononitrate 40mg", "Imdur",            "Tablet",    "40mg"),
    ("Isosorbide Mononitrate 60mg", "Imdur",            "Tablet",    "60mg"),
    ("Atenolol 25mg",               "Tenormin",         "Tablet",    "25mg"),
    ("Atenolol 50mg",               "Tenormin",         "Tablet",    "50mg"),
    ("Atenolol 100mg",              "Tenormin",         "Tablet",    "100mg"),
    ("Eplerenone 25mg",             "Inspra",           "Tablet",    "25mg"),
    ("Eplerenone 50mg",             "Inspra",           "Tablet",    "50mg"),
    ("Hydralazine 10mg",            "Apresoline",       "Tablet",    "10mg"),
    ("Hydralazine 25mg",            "Apresoline",       "Tablet",    "25mg"),
    ("Hydralazine 50mg",            "Apresoline",       "Tablet",    "50mg"),
    ("Perindopril 2mg",             "Coversyl",         "Tablet",    "2mg"),
    ("Perindopril 4mg",             "Coversyl",         "Tablet",    "4mg"),
    ("Perindopril 8mg",             "Coversyl",         "Tablet",    "8mg"),
    ("Ivabradine 5mg",              "Procoralan",       "Tablet",    "5mg"),
    ("Ivabradine 7.5mg",            "Procoralan",       "Tablet",    "7.5mg"),
    ("Sacubitril-Valsartan 50mg",   "Entresto",         "Tablet",    "50mg"),
    ("Sacubitril-Valsartan 100mg",  "Entresto",         "Tablet",    "100mg"),
    ("Sacubitril-Valsartan 200mg",  "Entresto",         "Tablet",    "200mg"),
    ("Fenofibrate 67mg",            "Lipanthyl",        "Capsule",   "67mg"),
    ("Fenofibrate 145mg",           "Lipanthyl",        "Tablet",    "145mg"),
    ("Ezetimibe 10mg",              "Ezetrol",          "Tablet",    "10mg"),
    ("Colchicine 0.5mg",            "Colchicine",       "Tablet",    "0.5mg"),
    ("Colchicine 1mg",              "Colchicine",       "Tablet",    "1mg"),
    # === NEUROLOGY ===
    ("Sumatriptan 25mg",            "Imigran",          "Tablet",    "25mg"),
    ("Sumatriptan 50mg",            "Imigran",          "Tablet",    "50mg"),
    ("Sumatriptan 100mg",           "Imigran",          "Tablet",    "100mg"),
    ("Topiramate 25mg",             "Topamax",          "Tablet",    "25mg"),
    ("Topiramate 50mg",             "Topamax",          "Tablet",    "50mg"),
    ("Topiramate 100mg",            "Topamax",          "Tablet",    "100mg"),
    ("Levetiracetam 250mg",         "Keppra",           "Tablet",    "250mg"),
    ("Levetiracetam 500mg",         "Keppra",           "Tablet",    "500mg"),
    ("Levetiracetam 750mg",         "Keppra",           "Tablet",    "750mg"),
    ("Levetiracetam 1000mg",        "Keppra",           "Tablet",    "1000mg"),
    ("Levetiracetam 100mg/ml",      "Keppra",           "Liquid",    "100mg/ml"),
    ("Valproate 200mg",             "Depakine",         "Tablet",    "200mg"),
    ("Valproate 500mg",             "Depakine",         "Tablet",    "500mg"),
    ("Valproate 200mg/5ml",         "Depakine",         "Liquid",    "200mg/5ml"),
    ("Carbamazepine 100mg",         "Tegretol",         "Tablet",    "100mg"),
    ("Carbamazepine 200mg",         "Tegretol",         "Tablet",    "200mg"),
    ("Carbamazepine 400mg",         "Tegretol",         "Tablet",    "400mg"),
    ("Carbamazepine 100mg/5ml",     "Tegretol",         "Liquid",    "100mg/5ml"),
    ("Lamotrigine 25mg",            "Lamictal",         "Tablet",    "25mg"),
    ("Lamotrigine 50mg",            "Lamictal",         "Tablet",    "50mg"),
    ("Lamotrigine 100mg",           "Lamictal",         "Tablet",    "100mg"),
    ("Lamotrigine 200mg",           "Lamictal",         "Tablet",    "200mg"),
    ("Amitriptyline 10mg",          "Elavil",           "Tablet",    "10mg"),
    ("Amitriptyline 25mg",          "Elavil",           "Tablet",    "25mg"),
    ("Amitriptyline 50mg",          "Elavil",           "Tablet",    "50mg"),
    ("Amitriptyline 75mg",          "Elavil",           "Tablet",    "75mg"),
    ("Gabapentin 100mg",            "Neurontin",        "Capsule",   "100mg"),
    ("Gabapentin 300mg",            "Neurontin",        "Capsule",   "300mg"),
    ("Gabapentin 400mg",            "Neurontin",        "Capsule",   "400mg"),
    ("Pregabalin 25mg",             "Lyrica",           "Capsule",   "25mg"),
    ("Pregabalin 50mg",             "Lyrica",           "Capsule",   "50mg"),
    ("Pregabalin 75mg",             "Lyrica",           "Capsule",   "75mg"),
    ("Pregabalin 150mg",            "Lyrica",           "Capsule",   "150mg"),
    ("Pregabalin 300mg",            "Lyrica",           "Capsule",   "300mg"),
    ("Donepezil 5mg",               "Aricept",          "Tablet",    "5mg"),
    ("Donepezil 10mg",              "Aricept",          "Tablet",    "10mg"),
    ("Memantine 5mg",               "Ebixa",            "Tablet",    "5mg"),
    ("Memantine 10mg",              "Ebixa",            "Tablet",    "10mg"),
    ("Memantine 20mg",              "Ebixa",            "Tablet",    "20mg"),
    ("Betahistine 8mg",             "Serc",             "Tablet",    "8mg"),
    ("Betahistine 16mg",            "Serc",             "Tablet",    "16mg"),
    ("Betahistine 24mg",            "Serc",             "Tablet",    "24mg"),
    ("Pramipexole 0.125mg",         "Mirapex",          "Tablet",    "0.125mg"),
    ("Pramipexole 0.25mg",          "Mirapex",          "Tablet",    "0.25mg"),
    ("Pramipexole 0.5mg",           "Mirapex",          "Tablet",    "0.5mg"),
    ("Pramipexole 1mg",             "Mirapex",          "Tablet",    "1mg"),
    ("Propranolol 10mg",            "Inderal",          "Tablet",    "10mg"),
    ("Propranolol 20mg",            "Inderal",          "Tablet",    "20mg"),
    ("Propranolol 40mg",            "Inderal",          "Tablet",    "40mg"),
    ("Propranolol 80mg",            "Inderal",          "Tablet",    "80mg"),
    ("Carbidopa-Levodopa 10/100mg", "Sinemet",          "Tablet",    "10/100mg"),
    ("Carbidopa-Levodopa 25/100mg", "Sinemet",          "Tablet",    "25/100mg"),
    ("Carbidopa-Levodopa 25/250mg", "Sinemet",          "Tablet",    "25/250mg"),
    ("Clonazepam 0.5mg",            "Rivotril",         "Tablet",    "0.5mg"),
    ("Clonazepam 1mg",              "Rivotril",         "Tablet",    "1mg"),
    ("Clonazepam 2mg",              "Rivotril",         "Tablet",    "2mg"),
    ("Phenytoin 30mg",              "Dilantin",         "Capsule",   "30mg"),
    ("Phenytoin 100mg",             "Dilantin",         "Capsule",   "100mg"),
    ("Phenytoin 50mg/ml",           "Dilantin",         "Injection", "50mg/ml"),
    ("Baclofen 5mg",                "Lioresal",         "Tablet",    "5mg"),
    ("Baclofen 10mg",               "Lioresal",         "Tablet",    "10mg"),
    ("Baclofen 20mg",               "Lioresal",         "Tablet",    "20mg"),
    ("Cinnarizine 25mg",            "Stugeron",         "Tablet",    "25mg"),
    ("Cinnarizine 75mg",            "Stugeron",         "Tablet",    "75mg"),
    ("Zolmitriptan 2.5mg",          "Zomig",            "Tablet",    "2.5mg"),
    ("Zolmitriptan 5mg",            "Zomig",            "Tablet",    "5mg"),
    ("Rizatriptan 5mg",             "Maxalt",           "Tablet",    "5mg"),
    ("Rizatriptan 10mg",            "Maxalt",           "Tablet",    "10mg"),
    ("Acetazolamide 250mg",         "Diamox",           "Tablet",    "250mg"),
    ("Piracetam 400mg",             "Nootropil",        "Tablet",    "400mg"),
    ("Piracetam 800mg",             "Nootropil",        "Tablet",    "800mg"),
    ("Piracetam 1200mg",            "Nootropil",        "Tablet",    "1200mg"),
    ("Rivastigmine 1.5mg",          "Exelon",           "Capsule",   "1.5mg"),
    ("Rivastigmine 3mg",            "Exelon",           "Capsule",   "3mg"),
    ("Rivastigmine 4.5mg",          "Exelon",           "Capsule",   "4.5mg"),
    ("Riluzole 50mg",               "Rilutek",          "Tablet",    "50mg"),
    # === ONCOLOGY ===
    ("Tamoxifen 10mg",              "Nolvadex",         "Tablet",    "10mg"),
    ("Tamoxifen 20mg",              "Nolvadex",         "Tablet",    "20mg"),
    ("Anastrozole 1mg",             "Arimidex",         "Tablet",    "1mg"),
    ("Letrozole 2.5mg",             "Femara",           "Tablet",    "2.5mg"),
    ("Exemestane 25mg",             "Aromasin",         "Tablet",    "25mg"),
    ("Imatinib 100mg",              "Gleevec",          "Tablet",    "100mg"),
    ("Imatinib 400mg",              "Gleevec",          "Tablet",    "400mg"),
    ("Erlotinib 25mg",              "Tarceva",          "Tablet",    "25mg"),
    ("Erlotinib 100mg",             "Tarceva",          "Tablet",    "100mg"),
    ("Erlotinib 150mg",             "Tarceva",          "Tablet",    "150mg"),
    ("Gefitinib 250mg",             "Iressa",           "Tablet",    "250mg"),
    ("Dasatinib 20mg",              "Sprycel",          "Tablet",    "20mg"),
    ("Dasatinib 50mg",              "Sprycel",          "Tablet",    "50mg"),
    ("Dasatinib 70mg",              "Sprycel",          "Tablet",    "70mg"),
    ("Nilotinib 150mg",             "Tasigna",          "Capsule",   "150mg"),
    ("Nilotinib 200mg",             "Tasigna",          "Capsule",   "200mg"),
    ("Methotrexate 2.5mg",          "Methofar",         "Tablet",    "2.5mg"),
    ("Methotrexate 10mg",           "Methofar",         "Tablet",    "10mg"),
    ("Methotrexate 25mg/ml",        "Methofar",         "Injection", "25mg/ml"),
    ("Methotrexate 50mg/2ml",       "Methofar",         "Injection", "50mg/2ml"),
    ("Dexamethasone 0.5mg",         "Decadron",         "Tablet",    "0.5mg"),
    ("Dexamethasone 4mg",           "Decadron",         "Tablet",    "4mg"),
    ("Dexamethasone 8mg",           "Decadron",         "Tablet",    "8mg"),
    ("Dexamethasone 4mg/ml",        "Decadron",         "Injection", "4mg/ml"),
    ("Dexamethasone 8mg/2ml",       "Decadron",         "Injection", "8mg/2ml"),
    ("Ondansetron 4mg",             "Zofran",           "Tablet",    "4mg"),
    ("Ondansetron 8mg",             "Zofran",           "Tablet",    "8mg"),
    ("Ondansetron 4mg/2ml",         "Zofran",           "Injection", "4mg/2ml"),
    ("Ondansetron 8mg/4ml",         "Zofran",           "Injection", "8mg/4ml"),
    ("Ondansetron 4mg/5ml",         "Zofran",           "Liquid",    "4mg/5ml"),
    ("Capecitabine 150mg",          "Xeloda",           "Tablet",    "150mg"),
    ("Capecitabine 500mg",          "Xeloda",           "Tablet",    "500mg"),
    ("Bicalutamide 50mg",           "Casodex",          "Tablet",    "50mg"),
    ("Bicalutamide 150mg",          "Casodex",          "Tablet",    "150mg"),
    ("Hydroxyurea 200mg",           "Hydrea",           "Capsule",   "200mg"),
    ("Hydroxyurea 500mg",           "Hydrea",           "Capsule",   "500mg"),
    ("Cyclophosphamide 25mg",       "Cytoxan",          "Tablet",    "25mg"),
    ("Cyclophosphamide 50mg",       "Cytoxan",          "Tablet",    "50mg"),
    ("Cyclophosphamide 200mg/vial", "Cytoxan",          "Injection", "200mg/vial"),
    ("Cyclophosphamide 500mg/vial", "Cytoxan",          "Injection", "500mg/vial"),
    ("Cyclophosphamide 1g/vial",    "Cytoxan",          "Injection", "1g/vial"),
    ("Mercaptopurine 50mg",         "Purinethol",       "Tablet",    "50mg"),
    ("Thalidomide 50mg",            "Thalomid",         "Capsule",   "50mg"),
    ("Thalidomide 100mg",           "Thalomid",         "Capsule",   "100mg"),
    ("Lenalidomide 5mg",            "Revlimid",         "Capsule",   "5mg"),
    ("Lenalidomide 10mg",           "Revlimid",         "Capsule",   "10mg"),
    ("Lenalidomide 25mg",           "Revlimid",         "Capsule",   "25mg"),
    # === GASTROENTEROLOGY ===
    ("Omeprazole 10mg",             "Losec",            "Capsule",   "10mg"),
    ("Omeprazole 20mg",             "Losec",            "Capsule",   "20mg"),
    ("Omeprazole 40mg",             "Losec",            "Capsule",   "40mg"),
    ("Omeprazole 40mg/vial",        "Losec",            "Injection", "40mg/vial"),
    ("Pantoprazole 20mg",           "Protonix",         "Tablet",    "20mg"),
    ("Pantoprazole 40mg",           "Protonix",         "Tablet",    "40mg"),
    ("Pantoprazole 40mg/vial",      "Protonix",         "Injection", "40mg/vial"),
    ("Esomeprazole 20mg",           "Nexium",           "Capsule",   "20mg"),
    ("Esomeprazole 40mg",           "Nexium",           "Capsule",   "40mg"),
    ("Rabeprazole 10mg",            "Pariet",           "Tablet",    "10mg"),
    ("Rabeprazole 20mg",            "Pariet",           "Tablet",    "20mg"),
    ("Lansoprazole 15mg",           "Prevacid",         "Capsule",   "15mg"),
    ("Lansoprazole 30mg",           "Prevacid",         "Capsule",   "30mg"),
    ("Mesalazine 400mg",            "Asacol",           "Tablet",    "400mg"),
    ("Mesalazine 800mg",            "Asacol",           "Tablet",    "800mg"),
    ("Mesalazine 4g/60ml",          "Asacol",           "Liquid",    "4g/60ml enema"),
    ("Lactulose 3.35g/5ml",         "Duphalac",         "Liquid",    "3.35g/5ml"),
    ("Lactulose 10g/15ml",          "Duphalac",         "Liquid",    "10g/15ml"),
    ("Domperidone 10mg",            "Motilium",         "Tablet",    "10mg"),
    ("Domperidone 5mg/5ml",         "Motilium",         "Liquid",    "5mg/5ml"),
    ("Domperidone 1mg/ml",          "Motilium",         "Liquid",    "1mg/ml"),
    ("Mebeverine 135mg",            "Duspatalin",       "Tablet",    "135mg"),
    ("Mebeverine 200mg",            "Duspatalin",       "Tablet",    "200mg"),
    ("Ursodeoxycholic Acid 150mg",  "Ursofalk",         "Tablet",    "150mg"),
    ("Ursodeoxycholic Acid 300mg",  "Ursofalk",         "Tablet",    "300mg"),
    ("Ursodeoxycholic Acid 500mg",  "Ursofalk",         "Tablet",    "500mg"),
    ("Rifaximin 200mg",             "Xifaxan",          "Tablet",    "200mg"),
    ("Rifaximin 400mg",             "Xifaxan",          "Tablet",    "400mg"),
    ("Rifaximin 550mg",             "Xifaxan",          "Tablet",    "550mg"),
    ("Prednisolone 5mg",            "Deltacortril",     "Tablet",    "5mg"),
    ("Prednisolone 20mg",           "Deltacortril",     "Tablet",    "20mg"),
    ("Prednisolone 40mg",           "Deltacortril",     "Tablet",    "40mg"),
    ("Prednisolone 5mg/5ml",        "Deltacortril",     "Liquid",    "5mg/5ml"),
    ("Prednisolone 15mg/5ml",       "Deltacortril",     "Liquid",    "15mg/5ml"),
    ("Azathioprine 25mg",           "Imuran",           "Tablet",    "25mg"),
    ("Azathioprine 50mg",           "Imuran",           "Tablet",    "50mg"),
    ("Metoclopramide 10mg",         "Primperan",        "Tablet",    "10mg"),
    ("Metoclopramide 10mg/2ml",     "Primperan",        "Injection", "10mg/2ml"),
    ("Sucralfate 1g",               "Carafate",         "Tablet",    "1g"),
    ("Bisacodyl 5mg",               "Dulcolax",         "Tablet",    "5mg"),
    ("Bisacodyl 10mg",              "Dulcolax",         "Tablet",    "10mg"),
    ("Senna 7.5mg",                 "Senokot",          "Tablet",    "7.5mg"),
    ("Senna 15mg",                  "Senokot",          "Tablet",    "15mg"),
    ("Loperamide 2mg",              "Imodium",          "Capsule",   "2mg"),
    ("Hyoscine 10mg",               "Buscopan",         "Tablet",    "10mg"),
    ("Hyoscine 20mg/ml",            "Buscopan",         "Injection", "20mg/ml"),
    ("Ranitidine 75mg",             "Zantac",           "Tablet",    "75mg"),
    ("Ranitidine 150mg",            "Zantac",           "Tablet",    "150mg"),
    ("Ranitidine 300mg",            "Zantac",           "Tablet",    "300mg"),
    ("Famotidine 20mg",             "Pepcid",           "Tablet",    "20mg"),
    ("Famotidine 40mg",             "Pepcid",           "Tablet",    "40mg"),
    ("Misoprostol 200mcg",          "Cytotec",          "Tablet",    "200mcg"),
    ("Infliximab 100mg/vial",       "Remicade",         "Injection", "100mg/vial"),
    ("Adalimumab 40mg/0.8ml",       "Humira",           "Injection", "40mg/0.8ml"),
    # === PULMONOLOGY ===
    ("Salbutamol 1mg/ml",           "Ventolin",         "Liquid",    "1mg/ml"),
    ("Salbutamol 2mg/ml",           "Ventolin",         "Liquid",    "2mg/ml"),
    ("Salbutamol 5mg/ml",           "Ventolin",         "Liquid",    "5mg/ml"),
    ("Salbutamol 0.5mg/ml",         "Ventolin",         "Injection", "0.5mg/ml"),
    ("Budesonide 0.25mg/2ml",       "Pulmicort",        "Liquid",    "0.25mg/2ml"),
    ("Budesonide 0.5mg/2ml",        "Pulmicort",        "Liquid",    "0.5mg/2ml"),
    ("Budesonide 1mg/2ml",          "Pulmicort",        "Liquid",    "1mg/2ml"),
    ("Ipratropium 0.25mg/ml",       "Atrovent",         "Liquid",    "0.25mg/ml"),
    ("Ipratropium 0.5mg/2ml",       "Atrovent",         "Liquid",    "0.5mg/2ml"),
    ("Tiotropium 9mcg",             "Spiriva",          "Capsule",   "9mcg"),
    ("Tiotropium 18mcg",            "Spiriva",          "Capsule",   "18mcg"),
    ("Montelukast 4mg",             "Singulair",        "Tablet",    "4mg"),
    ("Montelukast 5mg",             "Singulair",        "Tablet",    "5mg"),
    ("Montelukast 10mg",            "Singulair",        "Tablet",    "10mg"),
    ("Theophylline 100mg",          "Theodur",          "Tablet",    "100mg"),
    ("Theophylline 200mg",          "Theodur",          "Tablet",    "200mg"),
    ("Theophylline 300mg",          "Theodur",          "Tablet",    "300mg"),
    ("Amoxicillin 250mg Cap",       "Amoxil",           "Capsule",   "250mg"),
    ("Amoxicillin 500mg Cap",       "Amoxil",           "Capsule",   "500mg"),
    ("Amoxicillin 125mg/5ml",       "Amoxil",           "Liquid",    "125mg/5ml"),
    ("Amoxicillin 250mg/5ml",       "Amoxil",           "Liquid",    "250mg/5ml"),
    ("Amoxicillin-Clavulanate 375mg","Augmentin",       "Tablet",    "375mg"),
    ("Amoxicillin-Clavulanate 625mg","Augmentin",       "Tablet",    "625mg"),
    ("Amoxicillin-Clavulanate 1g",  "Augmentin",        "Tablet",    "1g"),
    ("Amoxicillin-Clavulanate 156mg/5ml","Augmentin",   "Liquid",    "156mg/5ml"),
    ("Amoxicillin-Clavulanate 312mg/5ml","Augmentin",   "Liquid",    "312mg/5ml"),
    ("Azithromycin 250mg",          "Zithromax",        "Tablet",    "250mg"),
    ("Azithromycin 500mg",          "Zithromax",        "Tablet",    "500mg"),
    ("Azithromycin 100mg/5ml",      "Zithromax",        "Liquid",    "100mg/5ml"),
    ("Azithromycin 200mg/5ml",      "Zithromax",        "Liquid",    "200mg/5ml"),
    ("Clarithromycin 250mg",        "Klacid",           "Tablet",    "250mg"),
    ("Clarithromycin 500mg",        "Klacid",           "Tablet",    "500mg"),
    ("Clarithromycin 125mg/5ml",    "Klacid",           "Liquid",    "125mg/5ml"),
    ("Doxycycline 50mg",            "Vibramycin",       "Capsule",   "50mg"),
    ("Doxycycline 100mg",           "Vibramycin",       "Capsule",   "100mg"),
    ("Levofloxacin 250mg",          "Levaquin",         "Tablet",    "250mg"),
    ("Levofloxacin 500mg",          "Levaquin",         "Tablet",    "500mg"),
    ("Levofloxacin 750mg",          "Levaquin",         "Tablet",    "750mg"),
    ("Moxifloxacin 400mg",          "Avelox",           "Tablet",    "400mg"),
    ("N-Acetylcysteine 200mg",      "Fluimucil",        "Tablet",    "200mg"),
    ("N-Acetylcysteine 600mg",      "Fluimucil",        "Tablet",    "600mg"),
    ("Fexofenadine 60mg",           "Allegra",          "Tablet",    "60mg"),
    ("Fexofenadine 120mg",          "Allegra",          "Tablet",    "120mg"),
    ("Fexofenadine 180mg",          "Allegra",          "Tablet",    "180mg"),
    # === NEPHROLOGY ===
    ("Erythropoietin 1000IU",       "Eprex",            "Injection", "1000IU/0.5ml"),
    ("Erythropoietin 2000IU",       "Eprex",            "Injection", "2000IU/0.5ml"),
    ("Erythropoietin 4000IU",       "Eprex",            "Injection", "4000IU/0.4ml"),
    ("Erythropoietin 10000IU",      "Eprex",            "Injection", "10000IU/ml"),
    ("Calcium Carbonate 500mg",     "Calcichew",        "Tablet",    "500mg"),
    ("Calcium Carbonate 1000mg",    "Calcichew",        "Tablet",    "1000mg"),
    ("Calcium Carbonate 1250mg",    "Calcichew",        "Tablet",    "1250mg"),
    ("Sodium Bicarbonate 500mg",    "Sodibic",          "Tablet",    "500mg"),
    ("Sodium Bicarbonate 650mg",    "Sodibic",          "Tablet",    "650mg"),
    ("Allopurinol 100mg",           "Zyloric",          "Tablet",    "100mg"),
    ("Allopurinol 200mg",           "Zyloric",          "Tablet",    "200mg"),
    ("Allopurinol 300mg",           "Zyloric",          "Tablet",    "300mg"),
    ("Enalapril 2.5mg",             "Vasotec",          "Tablet",    "2.5mg"),
    ("Enalapril 5mg",               "Vasotec",          "Tablet",    "5mg"),
    ("Enalapril 10mg",              "Vasotec",          "Tablet",    "10mg"),
    ("Enalapril 20mg",              "Vasotec",          "Tablet",    "20mg"),
    ("Tolvaptan 15mg",              "Jinarc",           "Tablet",    "15mg"),
    ("Tolvaptan 30mg",              "Jinarc",           "Tablet",    "30mg"),
    ("Tolvaptan 45mg",              "Jinarc",           "Tablet",    "45mg"),
    ("Tolvaptan 60mg",              "Jinarc",           "Tablet",    "60mg"),
    ("Ciprofloxacin 250mg",         "Cipro",            "Tablet",    "250mg"),
    ("Ciprofloxacin 500mg",         "Cipro",            "Tablet",    "500mg"),
    ("Ciprofloxacin 750mg",         "Cipro",            "Tablet",    "750mg"),
    ("Ciprofloxacin 100mg/50ml",    "Cipro",            "Injection", "100mg/50ml"),
    ("Ciprofloxacin 200mg/100ml",   "Cipro",            "Injection", "200mg/100ml"),
    ("Nitrofurantoin 50mg",         "Macrobid",         "Capsule",   "50mg"),
    ("Nitrofurantoin 100mg",        "Macrobid",         "Capsule",   "100mg"),
    ("Tamsulosin 0.2mg",            "Flomax",           "Capsule",   "0.2mg"),
    ("Tamsulosin 0.4mg",            "Flomax",           "Capsule",   "0.4mg"),
    ("Sevelamer 400mg",             "Renagel",          "Tablet",    "400mg"),
    ("Sevelamer 800mg",             "Renagel",          "Tablet",    "800mg"),
    ("Cinacalcet 30mg",             "Sensipar",         "Tablet",    "30mg"),
    ("Cinacalcet 60mg",             "Sensipar",         "Tablet",    "60mg"),
    ("Cinacalcet 90mg",             "Sensipar",         "Tablet",    "90mg"),
    # === OBSTETRICS & GYNECOLOGY ===
    ("Folic Acid 400mcg",           "Folvite",          "Tablet",    "400mcg"),
    ("Folic Acid 1mg",              "Folvite",          "Tablet",    "1mg"),
    ("Folic Acid 5mg",              "Folvite",          "Tablet",    "5mg"),
    ("Metformin 500mg OB",          "Glucophage",       "Tablet",    "500mg"),
    ("Metformin 850mg OB",          "Glucophage",       "Tablet",    "850mg"),
    ("Metformin 1000mg OB",         "Glucophage",       "Tablet",    "1000mg"),
    ("Progesterone 100mg",          "Utrogestan",       "Capsule",   "100mg"),
    ("Progesterone 200mg",          "Utrogestan",       "Capsule",   "200mg"),
    ("Labetalol 100mg OB",          "Trandate",         "Tablet",    "100mg"),
    ("Labetalol 200mg OB",          "Trandate",         "Tablet",    "200mg"),
    ("Labetalol 5mg/ml IV",         "Trandate",         "Injection", "5mg/ml"),
    ("Clomiphene 50mg",             "Clomid",           "Tablet",    "50mg"),
    ("Dienogest 2mg",               "Visanne",          "Tablet",    "2mg"),
    ("Iron Supplement 105mg",       "Ferrograd",        "Tablet",    "105mg"),
    ("Iron Supplement 325mg",       "Ferrograd",        "Tablet",    "325mg"),
    ("Magnesium Sulfate 500mg/ml",  "MgSO4",            "Injection", "500mg/ml"),
    ("Magnesium Sulfate 1g/2ml",    "MgSO4",            "Injection", "1g/2ml"),
    ("Methyldopa 125mg",            "Aldomet",          "Tablet",    "125mg"),
    ("Methyldopa 250mg",            "Aldomet",          "Tablet",    "250mg"),
    ("Methyldopa 500mg",            "Aldomet",          "Tablet",    "500mg"),
    ("Nifedipine 5mg Cap",          "Adalat",           "Capsule",   "5mg"),
    ("Nifedipine 10mg Cap",         "Adalat",           "Capsule",   "10mg"),
    ("Oxytocin 5IU/ml",             "Syntocinon",       "Injection", "5IU/ml"),
    ("Oxytocin 10IU/ml",            "Syntocinon",       "Injection", "10IU/ml"),
    ("Dydrogesterone 10mg",         "Duphaston",        "Tablet",    "10mg"),
    ("Medroxyprogesterone 5mg",     "Provera",          "Tablet",    "5mg"),
    ("Medroxyprogesterone 10mg",    "Provera",          "Tablet",    "10mg"),
    # === PEDIATRICS ===
    ("Paracetamol 120mg/5ml",       "Panadol",          "Liquid",    "120mg/5ml"),
    ("Paracetamol 250mg/5ml",       "Panadol",          "Liquid",    "250mg/5ml"),
    ("Paracetamol 500mg Tab",       "Panadol",          "Tablet",    "500mg"),
    ("Ibuprofen 100mg/5ml",         "Brufen",           "Liquid",    "100mg/5ml"),
    ("Ibuprofen 200mg/5ml",         "Brufen",           "Liquid",    "200mg/5ml"),
    ("Ibuprofen 200mg Tab",         "Brufen",           "Tablet",    "200mg"),
    ("Ibuprofen 400mg Tab",         "Brufen",           "Tablet",    "400mg"),
    ("Ibuprofen 600mg Tab",         "Brufen",           "Tablet",    "600mg"),
    ("Cetirizine 5mg/5ml",          "Zyrtec",           "Liquid",    "5mg/5ml"),
    ("Cetirizine 5mg Tab",          "Zyrtec",           "Tablet",    "5mg"),
    ("Cetirizine 10mg Tab",         "Zyrtec",           "Tablet",    "10mg"),
    ("Loratadine 5mg Tab",          "Claritin",         "Tablet",    "5mg"),
    ("Loratadine 10mg Tab",         "Claritin",         "Tablet",    "10mg"),
    ("Loratadine 5mg/5ml",          "Claritin",         "Liquid",    "5mg/5ml"),
    ("Vitamin D 400IU",             "Vidrop",           "Liquid",    "400IU/drop"),
    ("Vitamin D 1000IU",            "Vidrop",           "Liquid",    "1000IU/ml"),
    ("Ferrous Sulfate 25mg/ml",     "Ferro-Gradumet",   "Liquid",    "25mg/ml"),
    ("Ferrous Sulfate 200mg Tab",   "Ferro-Gradumet",   "Tablet",    "200mg"),
    ("Ferrous Sulfate 325mg Tab",   "Ferro-Gradumet",   "Tablet",    "325mg"),
    ("Acyclovir 200mg/5ml",         "Zovirax",          "Liquid",    "200mg/5ml"),
    ("Acyclovir 200mg Tab",         "Zovirax",          "Tablet",    "200mg"),
    ("Acyclovir 400mg Tab",         "Zovirax",          "Tablet",    "400mg"),
    ("Acyclovir 800mg Tab",         "Zovirax",          "Tablet",    "800mg"),
    ("Penicillin V 125mg/5ml",      "Ospen",            "Liquid",    "125mg/5ml"),
    ("Penicillin V 250mg/5ml",      "Ospen",            "Liquid",    "250mg/5ml"),
    ("Nystatin 100000IU/ml",        "Mycostatin",       "Liquid",    "100000IU/ml"),
    ("Zinc Sulfate 10mg/5ml",       "Zinco",            "Liquid",    "10mg/5ml"),
    ("Zinc Sulfate 20mg/5ml",       "Zinco",            "Liquid",    "20mg/5ml"),
    ("Oral Rehydration Salts",      "Rehydran",         "Liquid",    "Per sachet"),
    ("Diazepam 5mg/ml Rectal",      "Valium",           "Liquid",    "5mg/ml"),
    ("Phenobarbital 15mg",          "Luminal",          "Tablet",    "15mg"),
    ("Phenobarbital 30mg",          "Luminal",          "Tablet",    "30mg"),
    ("Phenobarbital 60mg",          "Luminal",          "Tablet",    "60mg"),
    # === SURGERY / EMERGENCY / ICU ===
    ("Cefazolin 500mg/vial",        "Kefzol",           "Injection", "500mg/vial"),
    ("Cefazolin 1g/vial",           "Kefzol",           "Injection", "1g/vial"),
    ("Cefazolin 2g/vial",           "Kefzol",           "Injection", "2g/vial"),
    ("Ceftriaxone 250mg/vial",      "Rocephin",         "Injection", "250mg/vial"),
    ("Ceftriaxone 500mg/vial",      "Rocephin",         "Injection", "500mg/vial"),
    ("Ceftriaxone 1g/vial",         "Rocephin",         "Injection", "1g/vial"),
    ("Ceftriaxone 2g/vial",         "Rocephin",         "Injection", "2g/vial"),
    ("Cefuroxime 250mg/vial",       "Zinacef",          "Injection", "250mg/vial"),
    ("Cefuroxime 750mg/vial",       "Zinacef",          "Injection", "750mg/vial"),
    ("Cefuroxime 1.5g/vial",        "Zinacef",          "Injection", "1.5g/vial"),
    ("Metronidazole 200mg",         "Flagyl",           "Tablet",    "200mg"),
    ("Metronidazole 400mg",         "Flagyl",           "Tablet",    "400mg"),
    ("Metronidazole 500mg Tab",     "Flagyl",           "Tablet",    "500mg"),
    ("Metronidazole 500mg/100ml",   "Flagyl",           "Injection", "500mg/100ml"),
    ("Metronidazole 200mg/5ml",     "Flagyl",           "Liquid",    "200mg/5ml"),
    ("Tramadol 50mg Cap",           "Tramal",           "Capsule",   "50mg"),
    ("Tramadol 100mg Cap",          "Tramal",           "Capsule",   "100mg"),
    ("Tramadol 50mg/ml",            "Tramal",           "Injection", "50mg/ml"),
    ("Tramadol 100mg/2ml",          "Tramal",           "Injection", "100mg/2ml"),
    ("Enoxaparin 20mg",             "Clexane",          "Injection", "20mg/0.2ml"),
    ("Enoxaparin 40mg",             "Clexane",          "Injection", "40mg/0.4ml"),
    ("Enoxaparin 60mg",             "Clexane",          "Injection", "60mg/0.6ml"),
    ("Enoxaparin 80mg",             "Clexane",          "Injection", "80mg/0.8ml"),
    ("Morphine 1mg/ml",             "MST",              "Injection", "1mg/ml"),
    ("Morphine 10mg/ml",            "MST",              "Injection", "10mg/ml"),
    ("Morphine 10mg Tab",           "MST",              "Tablet",    "10mg"),
    ("Morphine 30mg Tab",           "MST",              "Tablet",    "30mg"),
    ("Piperacillin-Tazobactam 2.25g","Tazocin",         "Injection", "2.25g/vial"),
    ("Piperacillin-Tazobactam 4.5g","Tazocin",          "Injection", "4.5g/vial"),
    ("Vancomycin 500mg",            "Vancocin",         "Injection", "500mg/vial"),
    ("Vancomycin 1g",               "Vancocin",         "Injection", "1g/vial"),
    ("Meropenem 500mg",             "Merrem",           "Injection", "500mg/vial"),
    ("Meropenem 1g",                "Merrem",           "Injection", "1g/vial"),
    ("Imipenem-Cilastatin 250mg",   "Tienam",           "Injection", "250mg/vial"),
    ("Imipenem-Cilastatin 500mg",   "Tienam",           "Injection", "500mg/vial"),
    ("Norepinephrine 1mg/ml",       "Levophed",         "Injection", "1mg/ml"),
    ("Norepinephrine 4mg/4ml",      "Levophed",         "Injection", "4mg/4ml"),
    ("Dopamine 40mg/ml",            "Intropin",         "Injection", "40mg/ml"),
    ("Dopamine 200mg/5ml",          "Intropin",         "Injection", "200mg/5ml"),
    ("Adrenaline 0.1mg/ml",         "EpiPen",           "Injection", "0.1mg/ml"),
    ("Adrenaline 0.5mg/ml",         "EpiPen",           "Injection", "0.5mg/ml"),
    ("Adrenaline 1mg/ml",           "EpiPen",           "Injection", "1mg/ml"),
    ("Propofol 10mg/ml",            "Diprivan",         "Injection", "10mg/ml"),
    ("Propofol 200mg/20ml",         "Diprivan",         "Injection", "200mg/20ml"),
    ("Midazolam 1mg/ml",            "Dormicum",         "Injection", "1mg/ml"),
    ("Midazolam 5mg/ml",            "Dormicum",         "Injection", "5mg/ml"),
    ("Lorazepam 2mg/ml",            "Ativan",           "Injection", "2mg/ml"),
    ("Lorazepam 4mg/ml",            "Ativan",           "Injection", "4mg/ml"),
    ("Fentanyl 50mcg/ml",           "Sublimaze",        "Injection", "50mcg/ml"),
    ("Fentanyl 100mcg/2ml",         "Sublimaze",        "Injection", "100mcg/2ml"),
    ("Mannitol 100mg/ml",           "Osmitrol",         "Injection", "100mg/ml"),
    ("Mannitol 200mg/ml",           "Osmitrol",         "Injection", "200mg/ml"),
    ("Heparin 1000IU/ml",           "Heparin Sodium",   "Injection", "1000IU/ml"),
    ("Heparin 5000IU/ml",           "Heparin Sodium",   "Injection", "5000IU/ml"),
    ("Heparin 25000IU/ml",          "Heparin Sodium",   "Injection", "25000IU/ml"),
    ("Hydrocortisone 100mg",        "Solu-Cortef",      "Injection", "100mg/vial"),
    ("Hydrocortisone 250mg",        "Solu-Cortef",      "Injection", "250mg/vial"),
    ("Hydrocortisone 500mg",        "Solu-Cortef",      "Injection", "500mg/vial"),
    ("Methylprednisolone 40mg",     "Solu-Medrol",      "Injection", "40mg/vial"),
    ("Methylprednisolone 125mg",    "Solu-Medrol",      "Injection", "125mg/vial"),
    ("Methylprednisolone 500mg",    "Solu-Medrol",      "Injection", "500mg/vial"),
    ("Methylprednisolone 1g",       "Solu-Medrol",      "Injection", "1g/vial"),
    ("Potassium Chloride 150mg/ml", "KCl",              "Injection", "150mg/ml"),
    ("Potassium Chloride 300mg/ml", "KCl",              "Injection", "300mg/ml"),
    ("Normal Saline 0.9% 100ml",    "Normal Saline",    "Injection", "0.9% 100ml"),
    ("Normal Saline 0.9% 500ml",    "Normal Saline",    "Injection", "0.9% 500ml"),
    ("Normal Saline 0.9% 1000ml",   "Normal Saline",    "Injection", "0.9% 1000ml"),
    ("Dextrose 5% 500ml",           "D5W",              "Injection", "5% 500ml"),
    ("Dextrose 5% 1000ml",          "D5W",              "Injection", "5% 1000ml"),
    ("Dextrose 50% 50ml",           "D50W",             "Injection", "50% 50ml"),
    ("Ringer Lactate 500ml",        "Hartmann",         "Injection", "500ml"),
    ("Ringer Lactate 1000ml",       "Hartmann",         "Injection", "1000ml"),
    ("Naloxone 0.4mg/ml",           "Narcan",           "Injection", "0.4mg/ml"),
    ("Naloxone 1mg/ml",             "Narcan",           "Injection", "1mg/ml"),
    ("Atropine 0.25mg/ml",          "Atropine Sulfate", "Injection", "0.25mg/ml"),
    ("Atropine 0.5mg/ml",           "Atropine Sulfate", "Injection", "0.5mg/ml"),
    ("Atropine 1mg/ml",             "Atropine Sulfate", "Injection", "1mg/ml"),
    ("Adenosine 3mg/ml",            "Adenocor",         "Injection", "3mg/ml"),
    ("Alteplase 10mg",              "Actilyse",         "Injection", "10mg/vial"),
    ("Alteplase 20mg",              "Actilyse",         "Injection", "20mg/vial"),
    ("Alteplase 50mg",              "Actilyse",         "Injection", "50mg/vial"),
    ("Streptokinase 750000IU",      "Streptase",        "Injection", "750000IU/vial"),
    ("Streptokinase 1500000IU",     "Streptase",        "Injection", "1500000IU/vial"),
    # === GENERAL / PSYCHIATRY / MISC ===
    ("Diclofenac 25mg",             "Voltaren",         "Tablet",    "25mg"),
    ("Diclofenac 50mg",             "Voltaren",         "Tablet",    "50mg"),
    ("Diclofenac 75mg",             "Voltaren",         "Tablet",    "75mg"),
    ("Diclofenac 100mg",            "Voltaren",         "Tablet",    "100mg"),
    ("Diclofenac 25mg/ml",          "Voltaren",         "Injection", "25mg/ml"),
    ("Diclofenac 75mg/3ml",         "Voltaren",         "Injection", "75mg/3ml"),
    ("Diclofenac 1% Gel",           "Voltaren",         "Ointment",  "1%"),
    ("Diclofenac 2% Gel",           "Voltaren",         "Ointment",  "2%"),
    ("Hydrocortisone 0.5% Cream",   "Cortef",           "Ointment",  "0.5%"),
    ("Hydrocortisone 1% Cream",     "Cortef",           "Ointment",  "1%"),
    ("Hydrocortisone 2.5% Cream",   "Cortef",           "Ointment",  "2.5%"),
    ("Betamethasone 0.025%",        "Betnovate",        "Ointment",  "0.025%"),
    ("Betamethasone 0.05%",         "Betnovate",        "Ointment",  "0.05%"),
    ("Betamethasone 0.1%",          "Betnovate",        "Ointment",  "0.1%"),
    ("Calamine Lotion",             "Caladryl",         "Ointment",  "Topical"),
    ("Ketoconazole 2% Cream",       "Nizoral",          "Ointment",  "2%"),
    ("Clotrimazole 1% Cream",       "Canesten",         "Ointment",  "1%"),
    ("Mupirocin 2% Ointment",       "Bactroban",        "Ointment",  "2%"),
    ("Silver Sulfadiazine 1%",      "Flamazine",        "Ointment",  "1%"),
    ("Fluconazole 50mg",            "Diflucan",         "Capsule",   "50mg"),
    ("Fluconazole 100mg",           "Diflucan",         "Capsule",   "100mg"),
    ("Fluconazole 150mg",           "Diflucan",         "Capsule",   "150mg"),
    ("Fluconazole 200mg",           "Diflucan",         "Capsule",   "200mg"),
    ("Fluconazole 2mg/ml",          "Diflucan",         "Injection", "2mg/ml"),
    ("Itraconazole 100mg",          "Sporanox",         "Capsule",   "100mg"),
    ("Voriconazole 200mg",          "Vfend",            "Tablet",    "200mg"),
    ("Voriconazole 200mg/vial",     "Vfend",            "Injection", "200mg/vial"),
    ("Escitalopram 5mg",            "Lexapro",          "Tablet",    "5mg"),
    ("Escitalopram 10mg",           "Lexapro",          "Tablet",    "10mg"),
    ("Escitalopram 20mg",           "Lexapro",          "Tablet",    "20mg"),
    ("Sertraline 25mg",             "Zoloft",           "Tablet",    "25mg"),
    ("Sertraline 50mg",             "Zoloft",           "Tablet",    "50mg"),
    ("Sertraline 100mg",            "Zoloft",           "Tablet",    "100mg"),
    ("Fluoxetine 10mg",             "Prozac",           "Capsule",   "10mg"),
    ("Fluoxetine 20mg",             "Prozac",           "Capsule",   "20mg"),
    ("Fluoxetine 40mg",             "Prozac",           "Capsule",   "40mg"),
    ("Fluoxetine 20mg/5ml",         "Prozac",           "Liquid",    "20mg/5ml"),
    ("Mirtazapine 15mg",            "Remeron",          "Tablet",    "15mg"),
    ("Mirtazapine 30mg",            "Remeron",          "Tablet",    "30mg"),
    ("Mirtazapine 45mg",            "Remeron",          "Tablet",    "45mg"),
    ("Venlafaxine 37.5mg",          "Effexor",          "Capsule",   "37.5mg"),
    ("Venlafaxine 75mg",            "Effexor",          "Capsule",   "75mg"),
    ("Venlafaxine 150mg",           "Effexor",          "Capsule",   "150mg"),
    ("Duloxetine 20mg",             "Cymbalta",         "Capsule",   "20mg"),
    ("Duloxetine 30mg",             "Cymbalta",         "Capsule",   "30mg"),
    ("Duloxetine 60mg",             "Cymbalta",         "Capsule",   "60mg"),
    ("Alprazolam 0.25mg",           "Xanax",            "Tablet",    "0.25mg"),
    ("Alprazolam 0.5mg",            "Xanax",            "Tablet",    "0.5mg"),
    ("Alprazolam 1mg",              "Xanax",            "Tablet",    "1mg"),
    ("Alprazolam 2mg",              "Xanax",            "Tablet",    "2mg"),
    ("Diazepam 2mg",                "Valium",           "Tablet",    "2mg"),
    ("Diazepam 5mg",                "Valium",           "Tablet",    "5mg"),
    ("Diazepam 10mg",               "Valium",           "Tablet",    "10mg"),
    ("Diazepam 5mg/ml Inj",         "Valium",           "Injection", "5mg/ml"),
    ("Quetiapine 25mg",             "Seroquel",         "Tablet",    "25mg"),
    ("Quetiapine 50mg",             "Seroquel",         "Tablet",    "50mg"),
    ("Quetiapine 100mg",            "Seroquel",         "Tablet",    "100mg"),
    ("Quetiapine 200mg",            "Seroquel",         "Tablet",    "200mg"),
    ("Quetiapine 300mg",            "Seroquel",         "Tablet",    "300mg"),
    ("Risperidone 0.5mg",           "Risperdal",        "Tablet",    "0.5mg"),
    ("Risperidone 1mg",             "Risperdal",        "Tablet",    "1mg"),
    ("Risperidone 2mg",             "Risperdal",        "Tablet",    "2mg"),
    ("Risperidone 3mg",             "Risperdal",        "Tablet",    "3mg"),
    ("Risperidone 4mg",             "Risperdal",        "Tablet",    "4mg"),
    ("Olanzapine 5mg",              "Zyprexa",          "Tablet",    "5mg"),
    ("Olanzapine 10mg",             "Zyprexa",          "Tablet",    "10mg"),
    ("Olanzapine 15mg",             "Zyprexa",          "Tablet",    "15mg"),
    ("Haloperidol 0.5mg",           "Haldol",           "Tablet",    "0.5mg"),
    ("Haloperidol 1mg",             "Haldol",           "Tablet",    "1mg"),
    ("Haloperidol 5mg",             "Haldol",           "Tablet",    "5mg"),
    ("Haloperidol 5mg/ml",          "Haldol",           "Injection", "5mg/ml"),
    ("Orlistat 60mg",               "Xenical",          "Capsule",   "60mg"),
    ("Orlistat 120mg",              "Xenical",          "Capsule",   "120mg"),
    ("Metformin 500mg",             "Glucophage",       "Tablet",    "500mg"),
    ("Metformin 850mg",             "Glucophage",       "Tablet",    "850mg"),
    ("Metformin 1000mg",            "Glucophage",       "Tablet",    "1000mg"),
    ("Gliclazide 30mg",             "Diamicron",        "Tablet",    "30mg"),
    ("Gliclazide 60mg",             "Diamicron",        "Tablet",    "60mg"),
    ("Gliclazide 80mg",             "Diamicron",        "Tablet",    "80mg"),
    ("Glibenclamide 2.5mg",         "Daonil",           "Tablet",    "2.5mg"),
    ("Glibenclamide 5mg",           "Daonil",           "Tablet",    "5mg"),
    ("Sitagliptin 25mg",            "Januvia",          "Tablet",    "25mg"),
    ("Sitagliptin 50mg",            "Januvia",          "Tablet",    "50mg"),
    ("Sitagliptin 100mg",           "Januvia",          "Tablet",    "100mg"),
    ("Empagliflozin 10mg",          "Jardiance",        "Tablet",    "10mg"),
    ("Empagliflozin 25mg",          "Jardiance",        "Tablet",    "25mg"),
    ("Dapagliflozin 5mg",           "Forxiga",          "Tablet",    "5mg"),
    ("Dapagliflozin 10mg",          "Forxiga",          "Tablet",    "10mg"),
    ("Insulin Glargine 100IU/ml",   "Lantus",           "Injection", "100IU/ml"),
    ("Insulin Degludec 100IU/ml",   "Tresiba",          "Injection", "100IU/ml"),
    ("Insulin Aspart 100IU/ml",     "Novorapid",        "Injection", "100IU/ml"),
    ("Insulin Lispro 100IU/ml",     "Humalog",          "Injection", "100IU/ml"),
    ("Insulin Regular 100IU/ml",    "Actrapid",         "Injection", "100IU/ml"),
    ("Insulin NPH 100IU/ml",        "Insulatard",       "Injection", "100IU/ml"),
    ("Multivitamin Standard",       "Centrum",          "Tablet",    "Standard"),
    ("Multivitamin Senior",         "Centrum",          "Tablet",    "Senior"),
    ("Multivitamin Women",          "Centrum",          "Tablet",    "Women"),
    ("Vitamin D3 400IU",            "D-Pearls",         "Capsule",   "400IU"),
    ("Vitamin D3 1000IU",           "D-Pearls",         "Capsule",   "1000IU"),
    ("Vitamin D3 2000IU",           "D-Pearls",         "Capsule",   "2000IU"),
    ("Vitamin D3 5000IU",           "D-Pearls",         "Capsule",   "5000IU"),
    ("Vitamin B12 500mcg",          "Neurobion",        "Tablet",    "500mcg"),
    ("Vitamin B12 1000mcg",         "Neurobion",        "Tablet",    "1000mcg"),
    ("Vitamin B12 1000mcg/ml",      "Neurobion",        "Injection", "1000mcg/ml"),
    ("Vitamin C 250mg",             "Redoxon",          "Tablet",    "250mg"),
    ("Vitamin C 500mg",             "Redoxon",          "Tablet",    "500mg"),
    ("Vitamin C 1000mg",            "Redoxon",          "Tablet",    "1000mg"),
    ("Calcium + Vit D 500/200IU",   "Calcivit D",       "Tablet",    "500mg/200IU"),
    ("Calcium + Vit D 1000/400IU",  "Calcivit D",       "Tablet",    "1000mg/400IU"),
    ("Calcium + Vit D 1000/800IU",  "Calcivit D",       "Tablet",    "1000mg/800IU"),
    ("Zinc Sulfate 10mg Tab",       "Zinco",            "Tablet",    "10mg"),
    ("Zinc Sulfate 20mg Tab",       "Zinco",            "Tablet",    "20mg"),
    ("Zinc Sulfate 50mg Tab",       "Zinco",            "Tablet",    "50mg"),
    ("Diosmin 450mg",               "Daflon",           "Tablet",    "450mg"),
    ("Diosmin 500mg",               "Daflon",           "Tablet",    "500mg"),
    ("Diosmin 1000mg",              "Daflon",           "Tablet",    "1000mg"),
    ("Chlorphenamine 4mg",          "Piriton",          "Tablet",    "4mg"),
    ("Chlorphenamine 10mg/ml",      "Piriton",          "Injection", "10mg/ml"),
    ("Diphenhydramine 25mg",        "Benadryl",         "Capsule",   "25mg"),
    ("Diphenhydramine 50mg",        "Benadryl",         "Capsule",   "50mg"),
    ("Levothyroxine 25mcg",         "Synthroid",        "Tablet",    "25mcg"),
    ("Levothyroxine 50mcg",         "Synthroid",        "Tablet",    "50mcg"),
    ("Levothyroxine 75mcg",         "Synthroid",        "Tablet",    "75mcg"),
    ("Levothyroxine 100mcg",        "Synthroid",        "Tablet",    "100mcg"),
    ("Levothyroxine 125mcg",        "Synthroid",        "Tablet",    "125mcg"),
    ("Levothyroxine 150mcg",        "Synthroid",        "Tablet",    "150mcg"),
    ("Levothyroxine 200mcg",        "Synthroid",        "Tablet",    "200mcg"),
    ("Carbimazole 5mg",             "Neo-Mercazole",    "Tablet",    "5mg"),
    ("Carbimazole 10mg",            "Neo-Mercazole",    "Tablet",    "10mg"),
    ("Propylthiouracil 50mg",       "PTU",              "Tablet",    "50mg"),
    ("Colchicine 0.5mg Tab",        "Colchicine",       "Tablet",    "0.5mg"),
    ("Colchicine 1mg Tab",          "Colchicine",       "Tablet",    "1mg"),
    ("Febuxostat 40mg",             "Uloric",           "Tablet",    "40mg"),
    ("Febuxostat 80mg",             "Uloric",           "Tablet",    "80mg"),
    ("Hydroxychloroquine 200mg",    "Plaquenil",        "Tablet",    "200mg"),
    ("Methotrexate 2.5mg RA",       "Rheumatrex",       "Tablet",    "2.5mg"),
    ("Sulfasalazine 500mg",         "Salazopyrin",      "Tablet",    "500mg"),
    ("Leflunomide 10mg",            "Arava",            "Tablet",    "10mg"),
    ("Leflunomide 20mg",            "Arava",            "Tablet",    "20mg"),
    ("Naproxen 250mg",              "Naprosyn",         "Tablet",    "250mg"),
    ("Naproxen 500mg",              "Naprosyn",         "Tablet",    "500mg"),
    ("Celecoxib 100mg",             "Celebrex",         "Capsule",   "100mg"),
    ("Celecoxib 200mg",             "Celebrex",         "Capsule",   "200mg"),
    ("Meloxicam 7.5mg",             "Mobic",            "Tablet",    "7.5mg"),
    ("Meloxicam 15mg",              "Mobic",            "Tablet",    "15mg"),
    ("Ketorolac 10mg",              "Toradol",          "Tablet",    "10mg"),
    ("Ketorolac 30mg/ml",           "Toradol",          "Injection", "30mg/ml"),
    ("Codeine 15mg",                "Codeine Phosphate","Tablet",    "15mg"),
    ("Codeine 30mg",                "Codeine Phosphate","Tablet",    "30mg"),
    ("Oxycodone 5mg",               "OxyContin",        "Tablet",    "5mg"),
    ("Oxycodone 10mg",              "OxyContin",        "Tablet",    "10mg"),
    ("Pregabalin 50mg Pain",        "Lyrica",           "Capsule",   "50mg"),
    ("Tizanidine 2mg",              "Zanaflex",         "Tablet",    "2mg"),
    ("Tizanidine 4mg",              "Zanaflex",         "Tablet",    "4mg"),
    ("Cyclobenzaprine 5mg",         "Flexeril",         "Tablet",    "5mg"),
    ("Cyclobenzaprine 10mg",        "Flexeril",         "Tablet",    "10mg"),
    ("Chlorzoxazone 250mg",         "Parafon",          "Tablet",    "250mg"),
    ("Chlorzoxazone 500mg",         "Parafon",          "Tablet",    "500mg"),
    ("Alendronate 10mg",            "Fosamax",          "Tablet",    "10mg"),
    ("Alendronate 70mg",            "Fosamax",          "Tablet",    "70mg"),
    ("Risedronate 5mg",             "Actonel",          "Tablet",    "5mg"),
    ("Risedronate 35mg",            "Actonel",          "Tablet",    "35mg"),
    ("Zoledronic Acid 4mg/5ml",     "Zometa",           "Injection", "4mg/5ml"),
    ("Denosumab 60mg/ml",           "Prolia",           "Injection", "60mg/ml"),
    ("Testosterone 25mg",           "Androgel",         "Ointment",  "25mg/2.5g"),
    ("Testosterone 250mg/ml",       "Sustanon",         "Injection", "250mg/ml"),
    ("Sildenafil 25mg",             "Viagra",           "Tablet",    "25mg"),
    ("Sildenafil 50mg",             "Viagra",           "Tablet",    "50mg"),
    ("Sildenafil 100mg",            "Viagra",           "Tablet",    "100mg"),
    ("Tadalafil 5mg",               "Cialis",           "Tablet",    "5mg"),
    ("Tadalafil 10mg",              "Cialis",           "Tablet",    "10mg"),
    ("Tadalafil 20mg",              "Cialis",           "Tablet",    "20mg"),
    ("Finasteride 1mg",             "Propecia",         "Tablet",    "1mg"),
    ("Finasteride 5mg",             "Proscar",          "Tablet",    "5mg"),
    ("Dutasteride 0.5mg",           "Avodart",          "Capsule",   "0.5mg"),
    ("Mesalazine Rectal 1g",        "Pentasa",          "Liquid",    "1g/100ml enema"),
    ("Budesonide 3mg",              "Entocort",         "Capsule",   "3mg"),
    ("Tinidazole 500mg",            "Fasigyn",          "Tablet",    "500mg"),
    ("Secnidazole 500mg",           "Flagentyl",        "Tablet",    "500mg"),
    ("Albendazole 200mg",           "Zentel",           "Tablet",    "200mg"),
    ("Albendazole 400mg",           "Zentel",           "Tablet",    "400mg"),
    ("Mebendazole 100mg",           "Vermox",           "Tablet",    "100mg"),
    ("Ivermectin 3mg",              "Stromectol",       "Tablet",    "3mg"),
    ("Ivermectin 6mg",              "Stromectol",       "Tablet",    "6mg"),
    ("Chloroquine 150mg",           "Aralen",           "Tablet",    "150mg"),
    ("Hydroxychloroquine 400mg",    "Plaquenil",        "Tablet",    "400mg"),
    ("Artemether-Lumefantrine",     "Coartem",          "Tablet",    "20/120mg"),
    ("Oseltamivir 30mg",            "Tamiflu",          "Capsule",   "30mg"),
    ("Oseltamivir 45mg",            "Tamiflu",          "Capsule",   "45mg"),
    ("Oseltamivir 75mg",            "Tamiflu",          "Capsule",   "75mg"),
    ("Zanamivir 5mg",               "Relenza",          "Liquid",    "5mg/blister"),
    ("Acyclovir 200mg/vial",        "Zovirax IV",       "Injection", "200mg/vial"),
    ("Ganciclovir 500mg/vial",      "Cytovene",         "Injection", "500mg/vial"),
    ("Ribavirin 200mg",             "Rebetol",          "Capsule",   "200mg"),
    ("Sofosbuvir 400mg",            "Sovaldi",          "Tablet",    "400mg"),
    ("Daclatasvir 60mg",            "Daklinza",         "Tablet",    "60mg"),
    ("Ombitasvir 12.5mg",           "Viekirax",         "Tablet",    "12.5mg"),
    ("Tenofovir 300mg",             "Viread",           "Tablet",    "300mg"),
    ("Entecavir 0.5mg",             "Baraclude",        "Tablet",    "0.5mg"),
    ("Entecavir 1mg",               "Baraclude",        "Tablet",    "1mg"),
    ("Lamivudine 100mg",            "Epivir",           "Tablet",    "100mg"),
    ("Adefovir 10mg",               "Hepsera",          "Tablet",    "10mg"),
    ("Trimethoprim-Sulfamethoxazole 80/400mg","Bactrim","Tablet",    "80/400mg"),
    ("Trimethoprim-Sulfamethoxazole 160/800mg","Bactrim","Tablet",   "160/800mg"),
    ("Doxycycline 50mg Caps",       "Vibramycin",       "Capsule",   "50mg"),
    ("Doxycycline 100mg Caps",      "Vibramycin",       "Capsule",   "100mg"),
    ("Tetracycline 250mg",          "Tetracycline HCl", "Capsule",   "250mg"),
    ("Tetracycline 500mg",          "Tetracycline HCl", "Capsule",   "500mg"),
    ("Linezolid 600mg",             "Zyvox",            "Tablet",    "600mg"),
    ("Linezolid 2mg/ml",            "Zyvox",            "Injection", "2mg/ml"),
    ("Daptomycin 350mg",            "Cubicin",          "Injection", "350mg/vial"),
    ("Tigecycline 50mg",            "Tygacil",          "Injection", "50mg/vial"),
    ("Colistin 150mg",              "Colomycin",        "Injection", "150mg/vial"),
    ("Polymyxin B 500000IU",        "Polymyxin B",      "Injection", "500000IU/vial"),
    ("Amphotericin B 50mg",         "Fungizone",        "Injection", "50mg/vial"),
    ("Caspofungin 50mg",            "Cancidas",         "Injection", "50mg/vial"),
    ("Caspofungin 70mg",            "Cancidas",         "Injection", "70mg/vial"),
    ("Micafungin 50mg",             "Mycamine",         "Injection", "50mg/vial"),
    ("Anidulafungin 100mg",         "Eraxis",           "Injection", "100mg/vial"),
    ("Isoniazid 100mg",             "Rimifon",          "Tablet",    "100mg"),
    ("Isoniazid 300mg",             "Rimifon",          "Tablet",    "300mg"),
    ("Rifampicin 150mg",            "Rifadin",          "Capsule",   "150mg"),
    ("Rifampicin 300mg",            "Rifadin",          "Capsule",   "300mg"),
    ("Pyrazinamide 500mg",          "Zinamide",         "Tablet",    "500mg"),
    ("Ethambutol 100mg",            "Myambutol",        "Tablet",    "100mg"),
    ("Ethambutol 400mg",            "Myambutol",        "Tablet",    "400mg"),
    ("Streptomycin 1g/vial",        "Streptomycin",     "Injection", "1g/vial"),
    ("Capreomycin 1g/vial",         "Capastat",         "Injection", "1g/vial"),
    ("Levofloxacin 250mg TB",       "Levaquin",         "Tablet",    "250mg"),
    ("Cycloserine 250mg",           "Seromycin",        "Capsule",   "250mg"),
    ("Prothionamide 250mg",         "Prothionamide",    "Tablet",    "250mg"),
    ("Pyridoxine 25mg",             "Vitamin B6",       "Tablet",    "25mg"),
    ("Pyridoxine 50mg",             "Vitamin B6",       "Tablet",    "50mg"),
    ("Pyridoxine 100mg",            "Vitamin B6",       "Tablet",    "100mg"),
    ("Thiamine 50mg",               "Vitamin B1",       "Tablet",    "50mg"),
    ("Thiamine 100mg",              "Vitamin B1",       "Tablet",    "100mg"),
    ("Riboflavin 5mg",              "Vitamin B2",       "Tablet",    "5mg"),
    ("Niacinamide 100mg",           "Vitamin B3",       "Tablet",    "100mg"),
    ("Pantothenic Acid 5mg",        "Vitamin B5",       "Tablet",    "5mg"),
    ("Biotin 5mg",                  "Vitamin B7",       "Tablet",    "5mg"),
    ("Folic Acid 400mcg Tab",       "Folate",           "Tablet",    "400mcg"),
    ("Iron + Folic Acid",           "Ferrograd Folic",  "Tablet",    "105mg/350mcg"),
    ("Omega 3 1000mg",              "Fish Oil",         "Capsule",   "1000mg"),
    ("Magnesium 250mg",             "Magnesia",         "Tablet",    "250mg"),
    ("Potassium 600mg",             "Slow-K",           "Tablet",    "600mg"),
    ("Sodium Valproate 200mg",      "Epilim",           "Tablet",    "200mg"),
    ("Sodium Valproate 500mg",      "Epilim",           "Tablet",    "500mg"),
    ("Lithium Carbonate 150mg",     "Priadel",          "Tablet",    "150mg"),
    ("Lithium Carbonate 300mg",     "Priadel",          "Tablet",    "300mg"),
    ("Lithium Carbonate 450mg",     "Priadel",          "Tablet",    "450mg"),
    ("Aripiprazole 5mg",            "Abilify",          "Tablet",    "5mg"),
    ("Aripiprazole 10mg",           "Abilify",          "Tablet",    "10mg"),
    ("Aripiprazole 15mg",           "Abilify",          "Tablet",    "15mg"),
    ("Clozapine 25mg",              "Clozaril",         "Tablet",    "25mg"),
    ("Clozapine 100mg",             "Clozaril",         "Tablet",    "100mg"),
    ("Ziprasidone 20mg",            "Geodon",           "Capsule",   "20mg"),
    ("Ziprasidone 40mg",            "Geodon",           "Capsule",   "40mg"),
    ("Paliperidone 3mg",            "Invega",           "Tablet",    "3mg"),
    ("Paliperidone 6mg",            "Invega",           "Tablet",    "6mg"),
    ("Bupropion 75mg",              "Wellbutrin",       "Tablet",    "75mg"),
    ("Bupropion 150mg",             "Wellbutrin",       "Tablet",    "150mg"),
    ("Trazodone 50mg",              "Desyrel",          "Tablet",    "50mg"),
    ("Trazodone 100mg",             "Desyrel",          "Tablet",    "100mg"),
    ("Buspirone 5mg",               "Buspar",           "Tablet",    "5mg"),
    ("Buspirone 10mg",              "Buspar",           "Tablet",    "10mg"),
    ("Hydroxyzine 10mg",            "Atarax",           "Tablet",    "10mg"),
    ("Hydroxyzine 25mg",            "Atarax",           "Tablet",    "25mg"),
    ("Zolpidem 5mg",                "Ambien",           "Tablet",    "5mg"),
    ("Zolpidem 10mg",               "Ambien",           "Tablet",    "10mg"),
    ("Melatonin 3mg",               "Circadin",         "Tablet",    "3mg"),
    ("Melatonin 5mg",               "Circadin",         "Tablet",    "5mg"),
    ("Methylphenidate 10mg",        "Ritalin",          "Tablet",    "10mg"),
    ("Methylphenidate 20mg",        "Ritalin",          "Tablet",    "20mg"),
    ("Atomoxetine 10mg",            "Strattera",        "Capsule",   "10mg"),
    ("Atomoxetine 18mg",            "Strattera",        "Capsule",   "18mg"),
    ("Atomoxetine 40mg",            "Strattera",        "Capsule",   "40mg"),
    ("Lisdexamfetamine 20mg",       "Vyvanse",          "Capsule",   "20mg"),
    ("Lisdexamfetamine 30mg",       "Vyvanse",          "Capsule",   "30mg"),
    ("Modafinil 100mg",             "Provigil",         "Tablet",    "100mg"),
    ("Modafinil 200mg",             "Provigil",         "Tablet",    "200mg"),
    ("Mecobalamin 500mcg",          "Methycobal",       "Tablet",    "500mcg"),
    ("Mecobalamin 1000mcg",         "Methycobal",       "Injection", "1000mcg/ml"),
    ("Alpha Lipoic Acid 300mg",     "Thioctacid",       "Tablet",    "300mg"),
    ("Alpha Lipoic Acid 600mg",     "Thioctacid",       "Tablet",    "600mg"),
]

def get_random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randrange((end - start).days))

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        print(f"⏳ جاري إدخال {len(MEDICINES):,} دواء فريد...")

        BATCH_SIZE = 500
        for i in range(0, len(MEDICINES), BATCH_SIZE):
            batch = []
            for med_name, brand, med_type, dosage in MEDICINES[i:i + BATCH_SIZE]:
                batch.append((
                    med_name,
                    brand,
                    med_type,
                    dosage,
                    random.randint(50, 2000),
                    get_random_date(2026, 2029),
                    get_random_date(2020, 2025),
                ))
            cursor.executemany(
                """INSERT INTO MEDICINE
                   (Med_name, brand, type, dosage, stock_quantity, expiry_date, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                batch
            )
            conn.commit()
            print(f"   ↳ تم إدخال {min(i + BATCH_SIZE, len(MEDICINES)):,} / {len(MEDICINES):,}")

        cursor.execute("SELECT COUNT(*) FROM MEDICINE")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي: {total:,} دواء.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()



import pyodbc
import random

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب البيانات المطلوبة ──
        # Prescription مع patient_id و date
        cursor.execute("""
            SELECT prescription_id, patient_id, prescription_date
            FROM Prescription
        """)
        prescriptions = cursor.fetchall()

        # Medicine IDs
        cursor.execute("SELECT Medicine_ID FROM MEDICINE")
        medicine_ids = [r[0] for r in cursor.fetchall()]

        if not prescriptions or not medicine_ids:
            print("❌ تأكد إن Prescription و MEDICINE فيهم بيانات.")
            return

        TARGET     = min(500_000, len(prescriptions))
        BATCH_SIZE = 10_000

        # لو المواعيد أقل من TARGET نكرر
        all_prescriptions = prescriptions[:]
        while len(all_prescriptions) < TARGET:
            all_prescriptions += random.sample(
                prescriptions,
                min(TARGET - len(all_prescriptions), len(prescriptions))
            )
        all_prescriptions = all_prescriptions[:TARGET]
        random.shuffle(all_prescriptions)

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} سجل صيدلية...")

        for presc_id, patient_id, presc_date in all_prescriptions:

            quantity = random.randint(1, 5)   # كمية منطقية 1-5 علب

            records.append((
                random.choice(medicine_ids),
                patient_id,
                quantity,
                presc_id,
                presc_date,
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO PHARMACY
                       (medicine_id, patient_id, quantity, prescription_id, prescription_date)
                       VALUES (?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} سجل")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO PHARMACY
                   (medicine_id, patient_id, quantity, Presc_Id, prescription_date)
                   VALUES (?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM PHARMACY")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} سجل صيدلية.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()





import pyodbc
import random
from datetime import timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== LAB TESTS DATA ====================
# (Test_Name, Normal_range, possible_results)

LAB_TESTS = [
    # Hematology
    ("Complete Blood Count (CBC)",          "WBC: 4.5-11.0, RBC: 4.5-5.5, HGB: 12-17",  ["Normal", "Mild Anemia", "Leukocytosis", "Thrombocytopenia", "Polycythemia"]),
    ("Hemoglobin",                           "Male: 13.5-17.5 g/dL, Female: 12-15.5",    ["Normal", "Low - Anemia", "High - Polycythemia"]),
    ("Hematocrit",                           "Male: 41-53%, Female: 36-46%",              ["Normal", "Low", "High"]),
    ("WBC Count",                            "4.5-11.0 x10^3/uL",                        ["Normal", "Leukocytosis", "Leukopenia"]),
    ("Platelet Count",                       "150,000-400,000/uL",                        ["Normal", "Thrombocytopenia", "Thrombocytosis"]),
    ("ESR (Erythrocyte Sedimentation Rate)", "Male: 0-15 mm/hr, Female: 0-20 mm/hr",     ["Normal", "Elevated - Inflammation", "Markedly Elevated"]),
    ("Peripheral Blood Smear",               "Normal morphology",                         ["Normal", "Microcytic cells", "Macrocytic cells", "Sickle cells", "Target cells"]),
    ("Reticulocyte Count",                   "0.5-2.5%",                                  ["Normal", "Elevated", "Low"]),
    ("Prothrombin Time (PT)",                "11-13.5 seconds",                           ["Normal", "Prolonged - Coagulopathy", "Shortened"]),
    ("INR",                                  "0.8-1.2 (therapeutic: 2.0-3.0)",            ["Normal", "Elevated", "Supratherapeutic", "Subtherapeutic"]),
    ("APTT",                                 "25-35 seconds",                             ["Normal", "Prolonged", "Shortened"]),
    ("D-Dimer",                              "< 0.5 mg/L",                                ["Normal", "Elevated - DVT/PE suspected", "Markedly Elevated"]),
    ("Fibrinogen",                           "200-400 mg/dL",                             ["Normal", "Low - DIC", "High - Inflammation"]),
    ("Blood Group & Crossmatch",             "ABO/Rh compatible",                         ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
    # Biochemistry
    ("Fasting Blood Glucose",                "70-100 mg/dL",                              ["Normal", "Prediabetes 101-125", "Diabetes >126", "Hypoglycemia <70"]),
    ("Random Blood Glucose",                 "< 140 mg/dL",                               ["Normal", "Impaired 140-199", "Diabetic >200"]),
    ("HbA1c",                                "< 5.7% (Normal), 5.7-6.4% (Prediabetes)",  ["Normal <5.7%", "Prediabetes 5.7-6.4%", "Diabetes >6.5%", "Poor Control >8%"]),
    ("Serum Creatinine",                     "Male: 0.7-1.2 mg/dL, Female: 0.5-1.0",     ["Normal", "Mildly Elevated", "Moderately Elevated", "Severely Elevated"]),
    ("Blood Urea Nitrogen (BUN)",            "7-20 mg/dL",                                ["Normal", "Elevated - Renal Impairment", "High - Renal Failure"]),
    ("eGFR",                                 "> 60 mL/min/1.73m2",                        ["Normal >90", "Mild CKD 60-89", "Moderate CKD 30-59", "Severe CKD 15-29", "Kidney Failure <15"]),
    ("Serum Sodium",                         "136-145 mEq/L",                             ["Normal", "Hyponatremia", "Hypernatremia"]),
    ("Serum Potassium",                      "3.5-5.0 mEq/L",                             ["Normal", "Hypokalemia", "Hyperkalemia"]),
    ("Serum Chloride",                       "98-106 mEq/L",                              ["Normal", "Low", "High"]),
    ("Serum Bicarbonate",                    "22-29 mEq/L",                               ["Normal", "Low - Acidosis", "High - Alkalosis"]),
    ("Serum Calcium",                        "8.5-10.5 mg/dL",                            ["Normal", "Hypocalcemia", "Hypercalcemia"]),
    ("Serum Phosphorus",                     "2.5-4.5 mg/dL",                             ["Normal", "Low", "High"]),
    ("Serum Magnesium",                      "1.7-2.2 mg/dL",                             ["Normal", "Hypomagnesemia", "Hypermagnesemia"]),
    ("Serum Uric Acid",                      "Male: 3.5-7.2, Female: 2.6-6.0 mg/dL",     ["Normal", "Elevated - Gout risk", "Markedly Elevated"]),
    ("Total Protein",                        "6.0-8.3 g/dL",                              ["Normal", "Low - Malnutrition", "High"]),
    ("Serum Albumin",                        "3.5-5.0 g/dL",                              ["Normal", "Low - Hypoalbuminemia", "High"]),
    ("Serum Globulin",                       "2.0-3.5 g/dL",                              ["Normal", "Low", "High"]),
    # Liver Function Tests
    ("Total Bilirubin",                      "0.3-1.2 mg/dL",                             ["Normal", "Mildly Elevated", "Elevated - Jaundice", "Severely Elevated"]),
    ("Direct Bilirubin",                     "0.0-0.3 mg/dL",                             ["Normal", "Elevated - Obstructive", "High"]),
    ("Indirect Bilirubin",                   "0.2-0.8 mg/dL",                             ["Normal", "Elevated - Hemolytic", "High"]),
    ("ALT (SGPT)",                           "7-56 U/L",                                  ["Normal", "Mildly Elevated", "Moderately Elevated", "Severely Elevated - Hepatitis"]),
    ("AST (SGOT)",                           "10-40 U/L",                                 ["Normal", "Mildly Elevated", "Moderately Elevated", "Severely Elevated"]),
    ("ALP (Alkaline Phosphatase)",           "44-147 U/L",                                ["Normal", "Elevated - Liver/Bone disease", "Markedly Elevated"]),
    ("GGT (Gamma GT)",                       "9-48 U/L",                                  ["Normal", "Elevated", "Markedly Elevated - Alcohol"]),
    ("LDH (Lactate Dehydrogenase)",          "140-280 U/L",                               ["Normal", "Elevated", "Markedly Elevated"]),
    # Lipid Profile
    ("Total Cholesterol",                    "< 200 mg/dL (desirable)",                   ["Desirable <200", "Borderline 200-239", "High >240"]),
    ("LDL Cholesterol",                      "< 100 mg/dL (optimal)",                     ["Optimal <100", "Near Optimal 100-129", "Borderline 130-159", "High >160"]),
    ("HDL Cholesterol",                      "Male: >40, Female: >50 mg/dL",              ["Normal", "Low - High Risk", "High - Protective"]),
    ("Triglycerides",                        "< 150 mg/dL (normal)",                      ["Normal <150", "Borderline 150-199", "High 200-499", "Very High >500"]),
    ("Non-HDL Cholesterol",                  "< 130 mg/dL",                               ["Normal", "Elevated", "High"]),
    # Cardiac Markers
    ("Troponin I",                           "< 0.04 ng/mL",                              ["Normal", "Elevated - Myocardial injury", "Markedly Elevated - MI"]),
    ("Troponin T",                           "< 0.01 ng/mL",                              ["Normal", "Elevated", "High - Acute MI"]),
    ("CK-MB",                                "< 25 U/L or < 3% total CK",                 ["Normal", "Elevated - Myocardial injury", "High"]),
    ("BNP (Brain Natriuretic Peptide)",      "< 100 pg/mL",                               ["Normal", "Elevated - Heart Failure", "Severely Elevated"]),
    ("NT-proBNP",                            "< 125 pg/mL",                               ["Normal", "Elevated", "Severely Elevated - HF"]),
    ("Myoglobin",                            "Male: 28-72 ng/mL, Female: 25-58",          ["Normal", "Elevated", "High - Muscle injury"]),
    ("CRP (C-Reactive Protein)",             "< 1.0 mg/L (low risk)",                     ["Normal <1.0", "Intermediate 1.0-3.0", "High >3.0", "Very High >10"]),
    ("High-Sensitivity CRP",                 "< 1.0 mg/L",                                ["Normal", "Intermediate Risk", "High Risk"]),
    # Thyroid Function
    ("TSH (Thyroid Stimulating Hormone)",    "0.4-4.0 mIU/L",                             ["Normal", "Low - Hyperthyroidism", "High - Hypothyroidism"]),
    ("Free T4",                              "0.8-1.8 ng/dL",                             ["Normal", "Low", "High - Hyperthyroid"]),
    ("Free T3",                              "2.3-4.2 pg/mL",                             ["Normal", "Low", "High"]),
    ("Anti-TPO Antibodies",                  "< 34 IU/mL",                                ["Negative", "Weakly Positive", "Positive - Hashimoto's"]),
    ("Anti-Thyroglobulin",                   "< 115 IU/mL",                               ["Negative", "Positive"]),
    # Hormones
    ("Cortisol (Morning)",                   "6-23 mcg/dL (AM)",                          ["Normal", "Low - Adrenal Insufficiency", "High - Cushing's"]),
    ("Insulin",                              "2-25 mIU/L (fasting)",                      ["Normal", "Low", "High - Insulin Resistance"]),
    ("Testosterone (Male)",                  "300-1000 ng/dL",                            ["Normal", "Low - Hypogonadism", "High"]),
    ("FSH",                                  "Male: 1.5-12.4, Female varies by cycle",    ["Normal", "Low", "High - Primary Gonadal Failure"]),
    ("LH",                                   "Male: 1.7-8.6, Female varies by cycle",     ["Normal", "Low", "High"]),
    ("Prolactin",                            "Male: 2-18 ng/mL, Female: 2-29 ng/mL",      ["Normal", "Mildly Elevated", "Elevated - Prolactinoma"]),
    ("Beta-HCG",                             "Non-pregnant: < 5 mIU/mL",                  ["Negative", "Positive - Pregnancy", "High - Multiple pregnancy/molar"]),
    ("Estradiol",                            "Varies by cycle phase",                     ["Normal", "Low", "High"]),
    ("Progesterone",                         "Varies by cycle phase",                     ["Normal", "Low - Luteal defect", "High"]),
    ("IGF-1",                                "Varies by age",                             ["Normal", "Low - GH deficiency", "High - Acromegaly"]),
    # Microbiology
    ("Blood Culture",                        "No growth",                                  ["No growth - Negative", "Gram positive cocci", "Gram negative bacilli", "E. coli", "Staphylococcus aureus", "Klebsiella"]),
    ("Urine Culture",                        "< 10,000 CFU/mL",                           ["No significant growth", "E. coli >100,000 CFU", "Klebsiella >100,000 CFU", "Pseudomonas", "Enterococcus"]),
    ("Sputum Culture",                       "Normal flora or no pathogen",               ["Normal flora", "Streptococcus pneumoniae", "H. influenzae", "Pseudomonas aeruginosa", "Mycobacterium tuberculosis"]),
    ("Wound Swab Culture",                   "No pathogen isolated",                       ["No growth", "Staphylococcus aureus", "MRSA", "Pseudomonas", "E. coli", "Streptococcus"]),
    ("Throat Swab Culture",                  "Normal flora",                               ["Normal flora", "Group A Streptococcus", "Candida albicans"]),
    ("Stool Culture",                        "No pathogen isolated",                       ["No pathogen", "Salmonella", "Shigella", "Campylobacter", "E. coli O157"]),
    ("H. Pylori Antigen (Stool)",            "Negative",                                   ["Negative", "Positive"]),
    ("Malaria Rapid Test",                   "Negative",                                   ["Negative", "P. falciparum Positive", "P. vivax Positive"]),
    ("COVID-19 PCR",                         "Negative",                                   ["Negative", "Positive - Low CT", "Positive - High CT"]),
    ("Hepatitis B Surface Antigen",          "Negative",                                   ["Negative", "Positive - Active HBV"]),
    ("Hepatitis C Antibody",                 "Negative",                                   ["Negative", "Positive - HCV exposure"]),
    ("HIV 1/2 Antibody",                     "Negative",                                   ["Non-reactive", "Reactive - Confirm with Western Blot"]),
    ("RPR/VDRL (Syphilis)",                  "Non-reactive",                               ["Non-reactive", "Reactive 1:8", "Reactive 1:16"]),
    ("Gram Stain",                           "No organisms seen",                          ["No organisms", "Gram positive cocci", "Gram negative rods", "Gram positive rods"]),
    # Immunology
    ("ANA (Antinuclear Antibody)",           "Negative (< 1:40)",                          ["Negative", "Weakly Positive 1:40", "Positive 1:80", "Strongly Positive 1:160"]),
    ("Anti-dsDNA",                           "< 30 IU/mL",                                 ["Negative", "Borderline", "Positive - SLE"]),
    ("Rheumatoid Factor (RF)",               "< 20 IU/mL",                                 ["Negative", "Weakly Positive", "Positive - RA"]),
    ("Anti-CCP Antibodies",                  "< 20 U/mL",                                  ["Negative", "Weakly Positive", "Positive - RA"]),
    ("Complement C3",                        "90-180 mg/dL",                               ["Normal", "Low - SLE activity", "High - Inflammation"]),
    ("Complement C4",                        "16-47 mg/dL",                                ["Normal", "Low", "High"]),
    ("IgE (Total)",                          "< 100 IU/mL",                                ["Normal", "Elevated - Allergy/Parasites", "Markedly Elevated"]),
    ("IgG",                                  "700-1600 mg/dL",                             ["Normal", "Low - Immunodeficiency", "High - Infection/Autoimmune"]),
    ("IgA",                                  "70-400 mg/dL",                               ["Normal", "Low", "High"]),
    ("IgM",                                  "40-230 mg/dL",                               ["Normal", "Low", "High - Acute Infection"]),
    # Urinalysis
    ("Urinalysis (Complete)",                "Clear, pH 4.5-8, Protein: Neg, Glucose: Neg",["Normal", "Proteinuria", "Glycosuria", "Hematuria", "Pyuria", "UTI Pattern"]),
    ("Urine Protein/Creatinine Ratio",       "< 0.2 mg/mg",                                ["Normal", "Mild Proteinuria 0.2-1.0", "Nephrotic range >3.5"]),
    ("Urine Microalbumin",                   "< 30 mg/g creatinine",                       ["Normal", "Microalbuminuria 30-300", "Macroalbuminuria >300"]),
    ("Urine Osmolality",                     "500-800 mOsm/kg",                            ["Normal", "Low - Dilute urine", "High - Concentrated"]),
    ("24-hour Urine Protein",                "< 150 mg/24hr",                              ["Normal", "Mild 150-500", "Moderate 500-3500", "Nephrotic >3500"]),
    # Tumor Markers
    ("PSA (Prostate Specific Antigen)",      "< 4.0 ng/mL",                                ["Normal <4.0", "Borderline 4.0-10.0", "High >10.0 - Prostate CA"]),
    ("CA-125",                               "< 35 U/mL",                                  ["Normal", "Elevated - Ovarian CA risk", "Markedly Elevated"]),
    ("CEA (Carcinoembryonic Antigen)",       "< 2.5 ng/mL (non-smoker)",                   ["Normal", "Elevated - Colorectal CA", "High"]),
    ("AFP (Alpha-Fetoprotein)",              "< 10 ng/mL",                                 ["Normal", "Elevated - Liver CA/Germ cell", "Markedly Elevated"]),
    ("CA 19-9",                              "< 37 U/mL",                                  ["Normal", "Elevated - Pancreatic CA", "High"]),
    ("CA 15-3",                              "< 30 U/mL",                                  ["Normal", "Elevated - Breast CA monitoring", "High"]),
    ("Beta-HCG (Tumor)",                     "< 5 mIU/mL",                                 ["Normal", "Elevated - Germ cell tumor", "High"]),
    # Other
    ("Vitamin D (25-OH)",                    "30-100 ng/mL",                               ["Sufficient 30-100", "Insufficient 20-29", "Deficient <20", "Toxic >100"]),
    ("Vitamin B12",                          "200-900 pg/mL",                              ["Normal", "Low - B12 Deficiency", "High"]),
    ("Folate (Serum)",                       "> 5.9 ng/mL",                                ["Normal", "Low - Folate Deficiency"]),
    ("Ferritin",                             "Male: 20-250, Female: 10-120 ng/mL",         ["Normal", "Low - Iron Deficiency", "High - Inflammation/Overload"]),
    ("Serum Iron",                           "60-170 mcg/dL",                              ["Normal", "Low", "High - Hemochromatosis"]),
    ("TIBC",                                 "250-370 mcg/dL",                             ["Normal", "High - Iron Deficiency", "Low - Inflammation"]),
    ("Transferrin Saturation",               "20-50%",                                     ["Normal", "Low - Iron Deficiency", "High - Hemochromatosis"]),
    ("Lipase",                               "10-140 U/L",                                 ["Normal", "Elevated - Pancreatitis", "Markedly Elevated"]),
    ("Amylase",                              "40-140 U/L",                                 ["Normal", "Elevated - Pancreatitis/Salivary", "High"]),
    ("Arterial Blood Gas (ABG)",             "pH 7.35-7.45, PO2 75-100, PCO2 35-45",      ["Normal", "Respiratory Acidosis", "Respiratory Alkalosis", "Metabolic Acidosis", "Metabolic Alkalosis", "Mixed"]),
    ("Lactate",                              "< 2.0 mmol/L",                               ["Normal", "Mildly Elevated 2.0-4.0", "Elevated >4.0 - Shock"]),
    ("Procalcitonin",                        "< 0.5 ng/mL",                                ["Normal", "Elevated - Bacterial infection", "High >2.0 - Sepsis", "Very High >10 - Severe Sepsis"]),
    ("Ammonia",                              "15-45 mcg/dL",                               ["Normal", "Elevated - Liver disease", "High - Hepatic encephalopathy"]),
    ("Ceruloplasmin",                        "20-60 mg/dL",                                ["Normal", "Low - Wilson's disease", "High - Inflammation"]),
    ("Homocysteine",                         "5-15 mcol/L",                                ["Normal", "Mildly Elevated", "High - Cardiovascular risk"]),
    ("Protein C",                            "70-140%",                                    ["Normal", "Low - Thrombophilia risk"]),
    ("Protein S",                            "60-140%",                                    ["Normal", "Low - Thrombophilia risk"]),
    ("Anti-Thrombin III",                    "80-120%",                                    ["Normal", "Low - Hypercoagulability"]),
    ("Factor V Leiden",                      "Negative",                                   ["Negative", "Heterozygous Positive", "Homozygous Positive"]),
]

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب البيانات المطلوبة ──
        cursor.execute("""
            SELECT A.Appointment_ID, A.Appointment_DateTime
            FROM APPOINTMENTS A
            WHERE A.Appointment_status = 'Completed'
        """)
        appointments = cursor.fetchall()

        cursor.execute("SELECT T_ID FROM TECHNICIANS")
        tech_ids = [r[0] for r in cursor.fetchall()]

        if not appointments or not tech_ids:
            print("❌ تأكد إن APPOINTMENTS و TECHNICIANS فيهم بيانات.")
            return

        TARGET     = min(500_000, len(appointments))
        BATCH_SIZE = 10_000

        # لو المواعيد أقل من TARGET نكرر
        all_appointments = appointments[:]
        while len(all_appointments) < TARGET:
            all_appointments += random.sample(
                appointments,
                min(TARGET - len(all_appointments), len(appointments))
            )
        all_appointments = all_appointments[:TARGET]
        random.shuffle(all_appointments)

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} تحليل طبي...")

        for app_id, app_datetime in all_appointments:

            test_name, normal_range, results = random.choice(LAB_TESTS)

            # Order = وقت الموعد أو بعده بساعات
            order_dt  = app_datetime + timedelta(hours=random.randint(0, 3))

            # Result = بعد Order بـ 2-48 ساعة حسب نوع التحليل
            result_hours = random.randint(2, 48)
            result_dt = order_dt + timedelta(hours=result_hours)

            test_result   = random.choice(results)
            re_test       = 1 if "Elevated" in test_result or "Positive" in test_result or "High" in test_result else 0
            # 10% احتمال إضافي لـ re-test عشوائي
            if random.random() < 0.10:
                re_test = 1

            records.append((
                random.choice(tech_ids),
                app_id,
                test_name,
                order_dt,
                result_dt,
                normal_range,
                test_result,
                re_test,
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO Lab_Tests
                       (Tech_ID, AppID, Test_Name, order_date_time, Result_date_Time,
                        Normal_range, Test_Result, Re_test_Required)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} تحليل")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO Lab_Tests
                   (Tech_ID, AppID, Test_Name, order_date_time, Result_date_Time,
                    Normal_range, Test_Result, Re_test_Required)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM Lab_Tests")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} تحليل طبي.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()






import pyodbc
import random
from datetime import date, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== ROOMS DATA ====================
# (prefix, Room_Type, capacity_range, status_weights)

ROOM_TYPES = [
    ("ER",   "Emergency Room",              (4, 8),   {"Available": 0.20, "Occupied": 0.70, "Under Maintenance": 0.10}),
    ("ICU",  "Intensive Care Unit",         (1, 2),   {"Available": 0.15, "Occupied": 0.75, "Under Maintenance": 0.10}),
    ("OR",   "Operating Room",              (1, 2),   {"Available": 0.25, "Occupied": 0.60, "Under Maintenance": 0.15}),
    ("GW",   "General Ward",               (4, 8),   {"Available": 0.35, "Occupied": 0.55, "Under Maintenance": 0.10}),
    ("PW",   "Private Ward",               (1, 1),   {"Available": 0.40, "Occupied": 0.50, "Under Maintenance": 0.10}),
    ("SW",   "Semi-Private Ward",          (2, 2),   {"Available": 0.35, "Occupied": 0.55, "Under Maintenance": 0.10}),
    ("MAT",  "Maternity Ward",             (2, 4),   {"Available": 0.30, "Occupied": 0.60, "Under Maintenance": 0.10}),
    ("PED",  "Pediatric Ward",             (4, 6),   {"Available": 0.35, "Occupied": 0.55, "Under Maintenance": 0.10}),
    ("ONC",  "Oncology Ward",              (2, 4),   {"Available": 0.30, "Occupied": 0.60, "Under Maintenance": 0.10}),
    ("ISO",  "Isolation Room",             (1, 1),   {"Available": 0.40, "Occupied": 0.45, "Under Maintenance": 0.15}),
    ("CCU",  "Cardiac Care Unit",          (1, 2),   {"Available": 0.20, "Occupied": 0.70, "Under Maintenance": 0.10}),
    ("HDU",  "High Dependency Unit",       (2, 4),   {"Available": 0.25, "Occupied": 0.65, "Under Maintenance": 0.10}),
    ("RH",   "Rehabilitation Room",        (2, 4),   {"Available": 0.45, "Occupied": 0.45, "Under Maintenance": 0.10}),
    ("CONS", "Consultation Room",          (1, 2),   {"Available": 0.50, "Occupied": 0.40, "Under Maintenance": 0.10}),
    ("LAB",  "Laboratory Room",            (2, 4),   {"Available": 0.40, "Occupied": 0.50, "Under Maintenance": 0.10}),
    ("RAD",  "Radiology Room",             (1, 2),   {"Available": 0.35, "Occupied": 0.50, "Under Maintenance": 0.15}),
    ("XRAY", "X-Ray Room",                 (1, 2),   {"Available": 0.40, "Occupied": 0.50, "Under Maintenance": 0.10}),
    ("MRI",  "MRI Room",                   (1, 1),   {"Available": 0.30, "Occupied": 0.55, "Under Maintenance": 0.15}),
    ("CT",   "CT Scan Room",               (1, 1),   {"Available": 0.30, "Occupied": 0.55, "Under Maintenance": 0.15}),
    ("ECG",  "ECG Room",                   (1, 2),   {"Available": 0.50, "Occupied": 0.40, "Under Maintenance": 0.10}),
    ("ECHO", "Echocardiography Room",      (1, 2),   {"Available": 0.45, "Occupied": 0.45, "Under Maintenance": 0.10}),
    ("ENDO", "Endoscopy Room",             (1, 2),   {"Available": 0.35, "Occupied": 0.50, "Under Maintenance": 0.15}),
    ("DIAL", "Dialysis Room",              (4, 8),   {"Available": 0.25, "Occupied": 0.65, "Under Maintenance": 0.10}),
    ("CHEMO","Chemotherapy Room",          (4, 8),   {"Available": 0.25, "Occupied": 0.65, "Under Maintenance": 0.10}),
    ("PHARM","Pharmacy Room",              (2, 4),   {"Available": 0.50, "Occupied": 0.40, "Under Maintenance": 0.10}),
    ("STOR", "Storage Room",               (1, 2),   {"Available": 0.60, "Occupied": 0.30, "Under Maintenance": 0.10}),
    ("CONF", "Conference Room",            (10, 20), {"Available": 0.55, "Occupied": 0.35, "Under Maintenance": 0.10}),
    ("WAIT", "Waiting Room",               (10, 30), {"Available": 0.20, "Occupied": 0.75, "Under Maintenance": 0.05}),
    ("NICU", "Neonatal ICU",               (4, 8),   {"Available": 0.20, "Occupied": 0.70, "Under Maintenance": 0.10}),
    ("BURN", "Burn Unit",                  (2, 4),   {"Available": 0.30, "Occupied": 0.60, "Under Maintenance": 0.10}),
]

# عدد الغرف من كل نوع
ROOM_COUNT_PER_TYPE = {
    "ER":    10, "ICU":  15, "OR":   8,  "GW":   20,
    "PW":   30, "SW":   20, "MAT":  10, "PED":  10,
    "ONC":  10, "ISO":  10, "CCU":  10, "HDU":  8,
    "RH":   8,  "CONS": 15, "LAB":  8,  "RAD":  5,
    "XRAY": 5,  "MRI":  3,  "CT":   3,  "ECG":  5,
    "ECHO": 4,  "ENDO": 4,  "DIAL": 8,  "CHEMO":6,
    "PHARM":3,  "STOR": 5,  "CONF": 4,  "WAIT": 8,
    "NICU": 8,  "BURN": 5,
}

def get_random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randrange((end - start).days))

def pick_status(weights):
    statuses = list(weights.keys())
    probs    = list(weights.values())
    return random.choices(statuses, weights=probs, k=1)[0]

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        records   = []
        room_dict = {row[0]: row[3] for row in ROOM_TYPES}  # prefix → status_weights

        for prefix, room_type, cap_range, status_weights in ROOM_TYPES:
            count = ROOM_COUNT_PER_TYPE.get(prefix, 5)

            for num in range(1, count + 1):
                room_id      = f"{prefix}-{num:03d}"   # e.g. ICU-001, GW-015
                capacity     = random.randint(*cap_range)
                status       = pick_status(status_weights)
                last_service = get_random_date(2023, 2025)

                records.append((room_id, room_type, capacity, status, last_service))

        cursor.executemany(
            """INSERT INTO ROOMS (Room_ID, Room_Type, capacity, status, last_serviced)
               VALUES (?, ?, ?, ?, ?)""",
            records
        )
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM ROOMS")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي: {total:,} غرفة.")
        print(f"\n📊 توزيع الغرف:")

        cursor.execute("""
            SELECT Room_Type, COUNT(*) as cnt, 
                   SUM(CASE WHEN status='Available' THEN 1 ELSE 0 END) as avail,
                   SUM(CASE WHEN status='Occupied' THEN 1 ELSE 0 END) as occ,
                   SUM(CASE WHEN status='Under Maintenance' THEN 1 ELSE 0 END) as maint
            FROM ROOMS GROUP BY Room_Type ORDER BY cnt DESC
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]:<30} Total:{row[1]:>3} | Available:{row[2]:>3} | Occupied:{row[3]:>3} | Maintenance:{row[4]:>3}")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()







import pyodbc
import random
from datetime import timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# مدة الإقامة المنطقية لكل نوع غرفة (بالأيام)
ROOM_STAY_DURATION = {
    "Emergency Room":           (1,  3),
    "Intensive Care Unit":      (3, 14),
    "Operating Room":           (0,  1),
    "General Ward":             (3,  7),
    "Private Ward":             (2,  7),
    "Semi-Private Ward":        (2,  7),
    "Maternity Ward":           (2,  5),
    "Pediatric Ward":           (2,  7),
    "Oncology Ward":            (3, 14),
    "Isolation Room":           (3, 10),
    "Cardiac Care Unit":        (3, 10),
    "High Dependency Unit":     (2,  7),
    "Rehabilitation Room":      (7, 30),
    "Consultation Room":        (0,  1),
    "Laboratory Room":          (0,  1),
    "Radiology Room":           (0,  1),
    "X-Ray Room":               (0,  1),
    "MRI Room":                 (0,  1),
    "CT Scan Room":             (0,  1),
    "ECG Room":                 (0,  1),
    "Echocardiography Room":    (0,  1),
    "Endoscopy Room":           (0,  1),
    "Dialysis Room":            (1,  2),
    "Chemotherapy Room":        (1,  3),
    "Pharmacy Room":            (0,  1),
    "Storage Room":             (0,  1),
    "Conference Room":          (0,  1),
    "Waiting Room":             (0,  1),
    "Neonatal ICU":             (5, 21),
    "Burn Unit":                (7, 30),
}

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب البيانات المطلوبة ──
        cursor.execute("SELECT Room_ID, Room_Type FROM ROOMS")
        rooms = cursor.fetchall()

        cursor.execute("SELECT Emp_ID FROM EMPLOYEES WHERE Active = 1")
        employee_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT Patient_ID FROM PATIENTS")
        patient_ids = [r[0] for r in cursor.fetchall()]

        if not rooms or not employee_ids or not patient_ids:
            print("❌ تأكد إن ROOMS و EMPLOYEES و PATIENTS فيهم بيانات.")
            return

        TARGET     = 500_000
        BATCH_SIZE = 10_000

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} سجل تعيين غرفة...")

        for _ in range(TARGET):
            room_id, room_type = random.choice(rooms)

            # مدة الإقامة المنطقية
            min_days, max_days = ROOM_STAY_DURATION.get(room_type, (1, 5))

            # تاريخ عشوائي من 2005 لـ 2025
            base_year  = random.randint(2005, 2025)
            base_month = random.randint(1, 12)
            base_day   = random.randint(1, 28)
            base_hour  = random.randint(0, 23)
            base_min   = random.randint(0, 59)

            from datetime import datetime
            assign_dt = datetime(base_year, base_month, base_day, base_hour, base_min)

            # end_date منطقي
            if max_days == 0:
                # غرف زيارة قصيرة — خروج نفس اليوم
                stay_hours = random.randint(1, 8)
                end_dt = assign_dt + timedelta(hours=stay_hours)
            else:
                stay_days = random.randint(max(1, min_days), max_days)
                end_dt    = assign_dt + timedelta(
                    days=stay_days,
                    hours=random.randint(0, 23)
                )

            # 5% من السجلات مازالوا في الغرفة (end_date = NULL)
            final_end = None if random.random() < 0.05 else end_dt

            records.append((
                room_id,
                random.choice(employee_ids),
                random.choice(patient_ids),
                assign_dt,
                final_end,
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO Room_Assignments
                       (R_id, Employee_ID, patient_id, assignment_date, end_date)
                       VALUES (?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} سجل")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO Room_Assignments
                   (R_id, Employee_ID, patient_id, assignment_date, end_date)
                   VALUES (?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM Room_Assignments")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} سجل.")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()





import pyodbc
import random
from datetime import date, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

def get_random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randrange((end - start).days))

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب الـ Workers من EMPLOYEES عشان يبقوا سواقين ──
        cursor.execute("""
            SELECT Emp_ID FROM EMPLOYEES 
            WHERE Role_Type = 'Worker' AND Active = 1
        """)
        worker_ids = [r[0] for r in cursor.fetchall()]

        if not worker_ids:
            print("❌ مفيش Workers في EMPLOYEES.")
            return

        # ── توليد 30 سيارة إسعاف ──
        NUM_AMBULANCES = 30

        AVAILABILITY_WEIGHTS = [
            ("Available",   0.40),
            ("On Duty",     0.45),
            ("Maintenance", 0.15),
        ]

        statuses  = [s for s, _ in AVAILABILITY_WEIGHTS]
        weights   = [w for _, w in AVAILABILITY_WEIGHTS]

        records        = []
        used_drivers   = set()

        for i in range(1, NUM_AMBULANCES + 1):
            amb_number   = f"AMB-{i:03d}"   # AMB-001 .. AMB-030
            availability = random.choices(statuses, weights=weights, k=1)[0]

            # السيارة في الصيانة = مفيش سواق
            if availability == "Maintenance":
                driver_id = None
            else:
                # كل سيارة عندها سواق مختلف
                available_drivers = [d for d in worker_ids if d not in used_drivers]
                if available_drivers:
                    driver_id = random.choice(available_drivers)
                    used_drivers.add(driver_id)
                else:
                    driver_id = random.choice(worker_ids)  # fallback لو عدد السواقين أقل

            last_service = get_random_date(2023, 2025)

            records.append((amb_number, availability, driver_id, last_service))

        cursor.executemany(
            """INSERT INTO AMBULANCE
               (ambulance_number, availability, driver_id, last_service_date)
               VALUES (?, ?, ?, ?)""",
            records
        )
        conn.commit()

        # ── طباعة ملخص ──
        cursor.execute("SELECT COUNT(*) FROM AMBULANCE")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT availability, COUNT(*) 
            FROM AMBULANCE 
            GROUP BY availability
        """)
        summary = cursor.fetchall()

        print(f"✅ تم الإدخال بنجاح! الإجمالي: {total} سيارة إسعاف.")
        print("\n📊 التوزيع:")
        for status, count in summary:
            print(f"   {status:<15} → {count} سيارة")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()





import pyodbc
import random
from datetime import datetime, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

EGYPTIAN_LOCATIONS = [
    # القاهرة
    "Tahrir Square, Cairo", "Nasr City, Cairo", "Heliopolis, Cairo",
    "Maadi, Cairo", "Zamalek, Cairo", "Dokki, Cairo", "Mohandessin, Cairo",
    "New Cairo, Cairo", "6th of October City, Giza", "Shubra, Cairo",
    "Ain Shams, Cairo", "Matariya, Cairo", "Hadayek El Kobba, Cairo",
    "El Marg, Cairo", "Shorouk City, Cairo", "Badr City, Cairo",
    # الجيزة
    "Haram, Giza", "Faisal, Giza", "Imbaba, Giza", "Agouza, Giza",
    "El Omraniya, Giza", "Boulaq El Dakrour, Giza",
    # الإسكندرية
    "Sidi Gaber, Alexandria", "Miami, Alexandria", "Stanley, Alexandria",
    "Smouha, Alexandria", "El Montaza, Alexandria", "Agami, Alexandria",
    "Moharam Bek, Alexandria", "El Ibrahimiya, Alexandria",
    # المحافظات
    "El Mansoura, Dakahlia", "Tanta, Gharbia", "Zagazig, Sharqia",
    "Ismailia", "Port Said", "Suez", "Assiut", "Sohag",
    "Luxor", "Aswan", "Fayoum", "Minya", "Benha, Qalyubia",
    "Damietta", "Beni Suef",
    # أماكن عامة
    "Cairo International Airport", "Ramses Station, Cairo",
    "Cairo Festival City Mall", "City Stars, Cairo",
    "El Rehab City, Cairo", "El Shorouk, Cairo",
    "Al Azhar University, Cairo", "Cairo University, Giza",
    "Ring Road, Cairo", "Cairo-Alexandria Desert Road",
    "Corniche El Nil, Cairo", "October Bridge, Cairo",
]

HOSPITAL_NAME = "Hospital Main Entrance"

def random_datetime(start_year, end_year):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب البيانات ──
        cursor.execute("SELECT ambulance_id FROM AMBULANCE")
        ambulance_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT Patient_ID FROM PATIENTS")
        patient_ids = [r[0] for r in cursor.fetchall()]

        if not ambulance_ids or not patient_ids:
            print("❌ تأكد إن AMBULANCE و PATIENTS فيهم بيانات.")
            return

        TARGET     = 500_000
        BATCH_SIZE = 10_000

        STATUS_WEIGHTS = [
            ("Completed",   0.75),
            ("In Progress", 0.10),
            ("Canceled",    0.15),
        ]
        statuses = [s for s, _ in STATUS_WEIGHTS]
        weights  = [w for _, w in STATUS_WEIGHTS]

        # نوعين من الرحلات:
        # 1. Pickup من مكان → Drop off عند المستشفى (الأغلب)
        # 2. Pickup من المستشفى → Drop off في مكان (نقل بين مستشفيات)
        TRIP_TYPE_WEIGHTS = [0.75, 0.25]

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} سجل إسعاف...")

        for _ in range(TARGET):
            status     = random.choices(statuses, weights=weights, k=1)[0]
            trip_type  = random.choices([1, 2], weights=TRIP_TYPE_WEIGHTS, k=1)[0]

            pickup_time = random_datetime(2005, 2025)

            if status == "Completed":
                # مدة الرحلة 10-90 دقيقة
                trip_minutes = random.randint(10, 90)
                dropoff_time = pickup_time + timedelta(minutes=trip_minutes)
            elif status == "In Progress":
                # لسه في الطريق
                dropoff_time = None
            else:
                # Canceled — مفيش dropoff
                dropoff_time = None

            if trip_type == 1:
                # من مكان → المستشفى
                pickup_loc  = random.choice(EGYPTIAN_LOCATIONS)
                dropoff_loc = HOSPITAL_NAME
            else:
                # من المستشفى → مكان تاني
                pickup_loc  = HOSPITAL_NAME
                dropoff_loc = random.choice(EGYPTIAN_LOCATIONS)

            records.append((
                random.choice(ambulance_ids),
                random.choice(patient_ids),
                pickup_loc,
                dropoff_loc,
                pickup_time,
                dropoff_time,
                status,
            ))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO Ambulance_Log
                       (ambulance_id, patient_id, pickup_location, dropoff_location,
                        pickup_time, dropoff_time, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} سجل")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO Ambulance_Log
                   (ambulance_id, patient_id, pickup_location, dropoff_location,
                    pickup_time, dropoff_time, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM Ambulance_Log")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} سجل إسعاف.")

        # ── ملخص ──
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM Ambulance_Log 
            GROUP BY status
        """)
        print("\n📊 التوزيع:")
        for row in cursor.fetchall():
            print(f"   {row[0]:<15} → {row[1]:,} سجل")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()





import pyodbc
import random

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== COMMENTS DATA ====================

COMMENTS_BY_RATING = {
    1: [
        "Very poor experience, waiting time was extremely long.",
        "Doctor was not attentive and dismissed my concerns.",
        "Staff were rude and unprofessional.",
        "The facility was dirty and poorly maintained.",
        "I waited over 3 hours and still did not see a doctor.",
        "Terrible service, will not come back.",
        "My prescription was wrong and had to be corrected.",
        "No one explained my diagnosis properly.",
        "The nurse was very rough during procedures.",
        "Billing was completely wrong and overcharged.",
        "Equipment looked outdated and poorly maintained.",
        "I felt ignored the entire visit.",
        "Reception staff were dismissive and unhelpful.",
        "The room was not clean when I arrived.",
        "Doctor spent less than 2 minutes with me.",
    ],
    2: [
        "Below average experience, waiting time was too long.",
        "Doctor was not very thorough in the examination.",
        "Staff could be more professional and caring.",
        "Facility needs better maintenance and cleanliness.",
        "Communication between staff could be much better.",
        "Had to repeat my medical history multiple times.",
        "Parking was a nightmare and very limited.",
        "The appointment system needs significant improvement.",
        "Lab results took much longer than promised.",
        "Some staff were helpful but others were not.",
        "Food quality in the ward was poor.",
        "Discharge process was slow and confusing.",
        "Follow-up appointment was hard to schedule.",
        "Nurse call button was not answered promptly.",
        "The pharmacy queue was extremely long.",
    ],
    3: [
        "Average experience overall, nothing exceptional.",
        "Service was acceptable but there is room for improvement.",
        "Doctor was professional but visit felt rushed.",
        "Waiting time was reasonable but could be better.",
        "Staff were helpful but the facility needs updating.",
        "Satisfied with the treatment but not the waiting time.",
        "Overall okay experience, met basic expectations.",
        "The doctor was knowledgeable but communication was average.",
        "Cleanliness was acceptable but not excellent.",
        "Billing was correct but the process was slow.",
        "Lab results came back within expected timeframe.",
        "The nurses were kind but seemed overworked.",
        "Parking was available but the fee was high.",
        "The appointment was kept on time.",
        "Medical care was adequate for my condition.",
    ],
    4: [
        "Good experience overall, staff were helpful and friendly.",
        "Doctor was thorough and explained everything clearly.",
        "Short waiting time and efficient service.",
        "Clean and well-maintained facility.",
        "Nursing staff were very attentive and caring.",
        "Treatment was effective and I feel much better.",
        "Appointment was on time and well organized.",
        "Lab results were delivered promptly.",
        "The pharmacy staff were helpful and efficient.",
        "Good communication from the medical team.",
        "Doctor took time to answer all my questions.",
        "Discharge process was smooth and well explained.",
        "Overall happy with the quality of care provided.",
        "Modern equipment and well-trained staff.",
        "Would recommend this hospital to others.",
    ],
    5: [
        "Excellent experience! Doctor was outstanding and very caring.",
        "World-class service from all staff members.",
        "Extremely satisfied with the treatment and outcome.",
        "The doctor went above and beyond to help me.",
        "Best hospital experience I have ever had.",
        "Staff were incredibly professional and compassionate.",
        "Minimal waiting time and highly efficient service.",
        "Spotlessly clean and very well maintained facility.",
        "The nursing team was exceptional and very attentive.",
        "Doctor explained everything in detail, very reassuring.",
        "I felt genuinely cared for throughout my stay.",
        "Outstanding follow-up care after my procedure.",
        "The entire team made a stressful time much easier.",
        "Highly recommend this hospital to everyone.",
        "Five stars is not enough for the amazing care I received.",
    ],
}

# توزيع التقييمات بشكل واقعي
RATING_WEIGHTS = {
    1: 0.05,   # 5%  - تقييم سيء
    2: 0.10,   # 10% - تقييم ضعيف
    3: 0.20,   # 20% - تقييم متوسط
    4: 0.35,   # 35% - تقييم جيد
    5: 0.30,   # 30% - تقييم ممتاز
}

def pick_rating():
    return random.choices(
        list(RATING_WEIGHTS.keys()),
        weights=list(RATING_WEIGHTS.values()),
        k=1
    )[0]

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب المواعيد الـ Completed بس ──
        cursor.execute("""
            SELECT Appointment_ID
            FROM APPOINTMENTS
            WHERE Appointment_status = 'Completed'
        """)
        app_ids = [r[0] for r in cursor.fetchall()]

        if not app_ids:
            print("❌ مفيش مواعيد Completed.")
            return

        # مش كل مريض بيدي feedback — 70% بس
        feedback_apps = random.sample(
            app_ids,
            int(len(app_ids) * 0.70)
        )

        TARGET     = min(500_000, len(feedback_apps))
        BATCH_SIZE = 10_000

        feedback_apps = feedback_apps[:TARGET]
        random.shuffle(feedback_apps)

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} تقييم...")

        for app_id in feedback_apps:
            rating  = pick_rating()
            comment = random.choice(COMMENTS_BY_RATING[rating])

            # 10% بيسيبوا التعليق فاضي
            if random.random() < 0.10:
                comment = None

            records.append((app_id, rating, comment))

            if len(records) >= BATCH_SIZE:
                cursor.executemany(
                    """INSERT INTO PATIENT_FEEDBACK
                       (AppID, Satisfaction_rating, Comments)
                       VALUES (?, ?, ?)""",
                    records
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} تقييم")
                records = []

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO PATIENT_FEEDBACK
                   (AppID, Satisfaction_rating, Comments)
                   VALUES (?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM PATIENT_FEEDBACK")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي الفعلي: {total:,} تقييم.")

        # ── ملخص التقييمات ──
        cursor.execute("""
            SELECT Satisfaction_rating, COUNT(*) as cnt
            FROM PATIENT_FEEDBACK
            GROUP BY Satisfaction_rating
            ORDER BY Satisfaction_rating
        """)
        print("\n📊 توزيع التقييمات:")
        for row in cursor.fetchall():
            stars = "⭐" * row[0]
            print(f"   {stars:<10} ({row[0]}) → {row[1]:,} تقييم")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()





import pyodbc
import random
from datetime import datetime, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

# ==================== PATIENT JOURNEY STEPS ====================
# كل مريض بيعدي على خطوات متسلسلة منطقية
# (transaction_type, relevant_roles, relevant_room_types, duration_minutes_range)

JOURNEY_STEPS = [
    # الخطوة 1: تسجيل الدخول
    (
        "Patient Registration",
        ["Receptionist"],
        ["Waiting Room"],
        (5, 20),      # 5-20 دقيقة للتسجيل
    ),
    # الخطوة 2: الانتظار في الاستقبال
    (
        "Waiting",
        ["Receptionist"],
        ["Waiting Room"],
        (15, 90),     # 15-90 دقيقة انتظار
    ),
    # الخطوة 3: الكشف
    (
        "Consultation Requested",
        ["Doctor"],
        ["Consultation Room"],
        (10, 40),     # 10-40 دقيقة كشف
    ),
    # الخطوة 4: طلب تحاليل (اختياري - 70%)
    (
        "Lab Test Ordered",
        ["Doctor", "Technician"],
        ["Laboratory Room"],
        (5, 15),
    ),
    # الخطوة 5: انتظار نتيجة التحاليل (اختياري - 70%)
    (
        "Waiting",
        ["Technician"],
        ["Waiting Room"],
        (30, 120),    # 30-120 دقيقة انتظار نتيجة
    ),
    # الخطوة 6: استلام نتيجة التحاليل (اختياري - 70%)
    (
        "Lab Result Received",
        ["Technician", "Doctor"],
        ["Laboratory Room"],
        (5, 15),
    ),
    # الخطوة 7: طلب أشعة (اختياري - 40%)
    (
        "Imaging Ordered",
        ["Doctor", "Technician"],
        ["Radiology Room", "X-Ray Room", "MRI Room", "CT Scan Room"],
        (5, 10),
    ),
    # الخطوة 8: انتظار الأشعة (اختياري - 40%)
    (
        "Waiting",
        ["Technician"],
        ["Waiting Room"],
        (20, 60),
    ),
    # الخطوة 9: إجراء الأشعة (اختياري - 40%)
    (
        "Imaging Completed",
        ["Technician"],
        ["Radiology Room", "X-Ray Room", "MRI Room", "CT Scan Room"],
        (15, 45),
    ),
    # الخطوة 10: مراجعة نتائج وإصدار الوصفة
    (
        "Prescription Issued",
        ["Doctor"],
        ["Consultation Room"],
        (5, 20),
    ),
    # الخطوة 11: تسجيل العلامات الحيوية
    (
        "Vital Signs Recorded",
        ["Nurse"],
        ["Consultation Room", "General Ward"],
        (5, 15),
    ),
    # الخطوة 12: إعطاء الدواء (اختياري - 50%)
    (
        "Medication Administered",
        ["Nurse", "Pharmacist"],
        ["Consultation Room", "General Ward"],
        (10, 30),
    ),
    # الخطوة 13: الإدخال (اختياري - 30%)
    (
        "Patient Admission",
        ["Doctor", "Nurse"],
        ["General Ward", "Private Ward", "ICU", "Cardiac Care Unit"],
        (15, 40),
    ),
    # الخطوة 14: الفاتورة
    (
        "Invoice Generated",
        ["Accountant", "Receptionist"],
        ["Waiting Room"],
        (5, 20),
    ),
    # الخطوة 15: الدفع والخروج
    (
        "Payment Received",
        ["Accountant"],
        ["Waiting Room"],
        (5, 15),
    ),
]

# سيناريوهات رحلة المريض
JOURNEY_SCENARIOS = [
    # (اسم السيناريو، الخطوات بالـ index، احتمال الحدوث)
    ("Simple Outpatient",    [0, 1, 2, 10, 11, 13, 14],              0.30),
    ("Outpatient with Labs", [0, 1, 2, 3, 4, 5, 10, 11, 13, 14],    0.25),
    ("Outpatient with Imaging", [0, 1, 2, 6, 7, 8, 10, 11, 13, 14], 0.15),
    ("Full Outpatient",      [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14], 0.15),
    ("Admitted Patient",     [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14], 0.10),
    ("Emergency",            [0, 2, 10, 11, 12, 13, 14],             0.05),
]

SCENARIO_NAMES   = [s[0] for s in JOURNEY_SCENARIOS]
SCENARIO_STEPS   = [s[1] for s in JOURNEY_SCENARIOS]
SCENARIO_WEIGHTS = [s[2] for s in JOURNEY_SCENARIOS]

def random_start_datetime(start_year, end_year):
    """وقت بداية الزيارة — بين 6 صباحاً و 8 مساءً"""
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = (end - start).days
    rand_day  = start + timedelta(days=random.randint(0, delta))
    rand_hour = random.randint(6, 20)
    rand_min  = random.choice([0, 15, 30, 45])
    return datetime(rand_day.year, rand_day.month, rand_day.day, rand_hour, rand_min)

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ── جيب البيانات ──
        cursor.execute("SELECT Patient_ID FROM PATIENTS")
        patient_ids = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT Emp_ID, Role_Type FROM EMPLOYEES WHERE Active = 1")
        employees = cursor.fetchall()

        cursor.execute("SELECT Room_ID, Room_Type FROM ROOMS")
        rooms = cursor.fetchall()

        if not patient_ids or not employees or not rooms:
            print("❌ تأكد إن PATIENTS و EMPLOYEES و ROOMS فيهم بيانات.")
            return

        # تجميع الموظفين حسب الدور
        role_emp_map = {}
        for emp_id, role in employees:
            role_emp_map.setdefault(role, []).append(emp_id)
        all_emp_ids = [e[0] for e in employees]

        # تجميع الغرف حسب النوع
        room_type_map = {}
        for room_id, room_type in rooms:
            room_type_map.setdefault(room_type, []).append(room_id)
        all_room_ids = [r[0] for r in rooms]

        TARGET     = 500_000
        BATCH_SIZE = 10_000

        records        = []
        total_inserted = 0

        print(f"⏳ جاري توليد {TARGET:,} سجل حركة مريض...")

        visits_generated = 0

        while total_inserted + len(records) < TARGET:

            # اختار مريض وسيناريو
            patient_id = random.choice(patient_ids)
            scenario_steps = random.choices(
                SCENARIO_STEPS,
                weights=SCENARIO_WEIGHTS,
                k=1
            )[0]

            # وقت بداية الزيارة
            current_time = random_start_datetime(2005, 2025)

            for step_idx in scenario_steps:
                trans_type, relevant_roles, relevant_room_types, duration_range = JOURNEY_STEPS[step_idx]

                # اختار موظف مناسب
                emp_id = None
                for role in relevant_roles:
                    if role in role_emp_map and role_emp_map[role]:
                        emp_id = random.choice(role_emp_map[role])
                        break
                if emp_id is None:
                    emp_id = random.choice(all_emp_ids)

                # اختار غرفة مناسبة
                room_id = None
                for rtype in relevant_room_types:
                    if rtype in room_type_map and room_type_map[rtype]:
                        room_id = random.choice(room_type_map[rtype])
                        break
                if room_id is None:
                    room_id = random.choice(all_room_ids)

                # Details تعبر عن الوقت بالدقائق
                duration_min = random.randint(*duration_range)
                detail = (
                    f"{trans_type} at {room_id} | "
                    f"Start: {current_time.strftime('%H:%M')} | "
                    f"Duration: {duration_min} min"
                )

                records.append((
                    trans_type,
                    patient_id,
                    room_id,
                    emp_id,
                    current_time,
                    detail,
                ))

                # الخطوة الجاية بتبدأ بعد انتهاء الخطوة الحالية
                current_time = current_time + timedelta(minutes=duration_min)

                if len(records) >= BATCH_SIZE:
                    cursor.executemany(
                        """INSERT INTO Hospital_Transactions_Log
                           (transaction_type, PatientID, Room_ID, Employee_ID,
                            Event_Timestamp, Details)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        records
                    )
                    conn.commit()
                    total_inserted += len(records)
                    print(f"   ↳ إجمالي مُدخَل: {total_inserted:,} سجل")
                    records = []

                if total_inserted + len(records) >= TARGET:
                    break

            visits_generated += 1

        # ── المتبقي ──
        if records:
            cursor.executemany(
                """INSERT INTO Hospital_Transactions_Log
                   (transaction_type, PatientID, Room_ID, Employee_ID,
                    Event_Timestamp, Details)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                records
            )
            conn.commit()
            total_inserted += len(records)

        cursor.execute("SELECT COUNT(*) FROM Hospital_Transactions_Log")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح!")
        print(f"   إجمالي السجلات : {total:,}")
        print(f"   إجمالي الزيارات: {visits_generated:,}")

        # ── ملخص ──
        cursor.execute("""
            SELECT transaction_type, COUNT(*) as cnt
            FROM Hospital_Transactions_Log
            GROUP BY transaction_type
            ORDER BY cnt DESC
        """)
        print("\n📊 توزيع الأحداث:")
        for row in cursor.fetchall():
            print(f"   {row[0]:<30} → {row[1]:,} سجل")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()







import pyodbc
import random
from datetime import date, timedelta

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

BLOOD_TYPES = [
    ("O+",  (150, 500)),
    ("A+",  (120, 400)),
    ("B+",  (80,  300)),
    ("AB+", (30,  150)),
    ("O-",  (40,  200)),
    ("A-",  (20,  100)),
    ("B-",  (15,   80)),
    ("AB-", (5,    40)),
]

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        START_DATE = date(2005, 1, 1)
        END_DATE   = date.today()

        records = []

        # كل فصيلة بتتحدث مرة كل أسبوعين تقريباً على مدار 20 سنة
        # 20 سنة = ~520 أسبوع → ÷ 2 = ~260 تحديث لكل فصيلة
        # 8 فصائل × 260 = ~2080 سجل

        for blood_type, (stock_min, stock_max) in BLOOD_TYPES:
            current_date = START_DATE

            while current_date <= END_DATE:
                stock_qty = random.randint(stock_min, stock_max)
                records.append((blood_type, stock_qty, current_date))

                # تحديث كل 10 - 18 يوم
                current_date += timedelta(days=random.randint(10, 18))

        random.shuffle(records)

        cursor.executemany(
            """INSERT INTO Blood_Bank (Blood_type, Stock_quantity, Last_updated)
               VALUES (?, ?, ?)""",
            records
        )
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM Blood_Bank")
        total = cursor.fetchone()[0]
        print(f"✅ تم الإدخال بنجاح! الإجمالي: {total:,} سجل.\n")

        cursor.execute("""
            SELECT 
                Blood_type,
                COUNT(*)            AS Total_Updates,
                MIN(Stock_quantity) AS Min_Stock,
                MAX(Stock_quantity) AS Max_Stock,
                AVG(Stock_quantity) AS Avg_Stock,
                MIN(Last_updated)   AS First_Record,
                MAX(Last_updated)   AS Latest_Record
            FROM Blood_Bank
            GROUP BY Blood_type
            ORDER BY Avg_Stock DESC
        """)
        print("📊 ملخص مخزون بنك الدم (2005 - اليوم):")
        print(f"{'فصيلة':<6} {'تحديثات':>9} {'أدنى':>6} {'أقصى':>6} {'متوسط':>7} {'أول سجل':<13} {'آخر سجل'}")
        print("-" * 70)
        for row in cursor.fetchall():
            print(f"{row[0]:<6} {row[1]:>9,} {row[2]:>6} {row[3]:>6} {row[4]:>7} {str(row[5]):<13} {str(row[6])}")

    except Exception as ex:
        print(f"❌ خطأ: {ex}")
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()












import pyodbc
import hashlib
import random
import string

conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=HospitalManagementSystem;"
    r"Trusted_Connection=yes;"
)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest().upper()

def generate_password(fname: str, emp_id: int = None, patient_id: int = None) -> str:
    """
    Password built from personal data:
    - First 3 chars of name (Capitalized)
    - Symbol (@)
    - Last 4 digits of ID (zero-padded)
    Example: Ahmed, ID=1001 -> Ahm@1001
    """
    name_part = fname[:3].capitalize()
    special   = "@"  # تم التعديل ليصبح @ دائماً
    
    if emp_id:
        num_part = str(emp_id)[-4:].zfill(4)
    elif patient_id:
        num_part = str(patient_id)[-4:].zfill(4)
    else:
        num_part = str(random.randint(1000, 9999))
        
    # تم إزالة جزء الحروف العشوائية (letters_part)
    return f"{name_part}{special}{num_part}"

DASHBOARD_MAP = {
    "Admin":        "/dashboard/admin",
    "Doctor":       "/dashboard/doctor",
    "Nurse":        "/dashboard/nurse",
    "Receptionist": "/dashboard/receptionist",
    "Accountant":   "/dashboard/accountant",
    "Technician":   "/dashboard/lab",
    "Pharmacist":   "/dashboard/pharmacy",
    "Worker":       "/dashboard/worker",
    "Patient":      "/dashboard/patient",
}

def main():
    try:
        conn   = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # ==================== STEP 1: BUILD ROLES FROM EMPLOYEES ====================
        cursor.execute("""
            SELECT DISTINCT Role_Type
            FROM EMPLOYEES
            WHERE Role_Type IS NOT NULL
            ORDER BY Role_Type
        """)
        role_types = [r[0] for r in cursor.fetchall()]

        cursor.execute("DELETE FROM Users")
        cursor.execute("DELETE FROM Roles")
        conn.commit()

        cursor.execute("INSERT INTO Roles (Role_Name) VALUES (?)", ('Admin',))
        for role in role_types:
            cursor.execute("INSERT INTO Roles (Role_Name) VALUES (?)", (role,))
        cursor.execute("INSERT INTO Roles (Role_Name) VALUES (?)", ('Patient',))
        conn.commit()

        cursor.execute("SELECT Role_ID, Role_Name FROM Roles ORDER BY Role_ID")
        roles    = cursor.fetchall()
        ROLE_MAP = {name: rid for rid, name in roles}

        print(f"Roles created: {[name for _, name in roles]}")

        used_usernames = set()

        def make_unique_username(base: str) -> str:
            username = base.lower().replace('.', '_')
            if username not in used_usernames:
                used_usernames.add(username)
                return username
            counter = 1
            while f"{username}_{counter}" in used_usernames:
                counter += 1
            used_usernames.add(f"{username}_{counter}")
            return f"{username}_{counter}"

        # ==================== STEP 2: ADMIN ====================
        admin_pass = "Admin@H2025"
        cursor.execute("""
            INSERT INTO Users
                (Username, PasswordHash, Role_ID, Employee_ID, Patient_ID, IsActive)
            VALUES (?, ?, ?, NULL, NULL, 1)
        """, ('admin', hash_password(admin_pass), ROLE_MAP['Admin']))
        used_usernames.add('admin')
        print(f"\nAdmin created -> username: admin | password: {admin_pass}")

        # ==================== STEP 3: EMPLOYEES ====================
        cursor.execute("""
            SELECT Emp_ID, FirstName, LastName, Role_Type
            FROM EMPLOYEES
            WHERE Active = 1
        """)
        employees = cursor.fetchall()
        print(f"\nCreating Employee Users ({len(employees):,})...")

        records_employees = []
        employee_creds    = []

        for emp_id, fname, lname, role_type in employees:
            username = make_unique_username(f"{fname}_{lname}{emp_id}")
            password = generate_password(fname, emp_id=emp_id)
            role_id  = ROLE_MAP.get(role_type, ROLE_MAP.get('Worker'))

            records_employees.append((
                username, hash_password(password),
                role_id, emp_id, None, 1
            ))
            employee_creds.append({
                "emp_id":   emp_id,
                "role":     role_type,
                "username": username,
                "password": password,
            })

        cursor.executemany("""
            INSERT INTO Users
                (Username, PasswordHash, Role_ID, Employee_ID, Patient_ID, IsActive)
            VALUES (?, ?, ?, ?, ?, ?)
        """, records_employees)
        conn.commit()
        print(f"Employee Users created: {len(records_employees):,}")

        # ==================== STEP 4: PATIENTS ====================
        cursor.execute("""
            SELECT Patient_ID, First_name, Last_name
            FROM PATIENTS
            ORDER BY Patient_ID
        """)
        patients = cursor.fetchall()
        print(f"\nCreating Patient Users ({len(patients):,})...")

        BATCH_SIZE     = 1000
        total_patients = 0
        patient_creds  = []

        for i in range(0, len(patients), BATCH_SIZE):
            batch            = patients[i:i + BATCH_SIZE]
            records_patients = []

            for patient_id, fname, lname in batch:
                username = make_unique_username(f"{fname}_{lname}{patient_id}")
                password = generate_password(fname, patient_id=patient_id)

                records_patients.append((
                    username,
                    hash_password(password),
                    ROLE_MAP['Patient'],
                    None,
                    patient_id,
                    1
                ))

                if len(patient_creds) < 10:
                    patient_creds.append({
                        "patient_id": patient_id,
                        "username":   username,
                        "password":   password,
                    })

            cursor.executemany("""
                INSERT INTO Users
                    (Username, PasswordHash, Role_ID, Employee_ID, Patient_ID, IsActive)
                VALUES (?, ?, ?, ?, ?, ?)
            """, records_patients)
            conn.commit()
            total_patients += len(batch)
            print(f"   -> {total_patients:,} / {len(patients):,} Patient Users inserted")

        # ==================== SUMMARY ====================
        cursor.execute("""
            SELECT R.Role_ID, R.Role_Name, COUNT(U.User_ID) AS Total
            FROM Users U
            JOIN Roles R ON U.Role_ID = R.Role_ID
            GROUP BY R.Role_ID, R.Role_Name
            ORDER BY R.Role_ID
        """)
        summary = cursor.fetchall()

        print(f"\n{'='*55}")
        print(f"  USERS SUMMARY")
        print(f"{'='*55}")
        total_all = 0
        for role_id, role, count in summary:
            dashboard = DASHBOARD_MAP.get(role, "/dashboard")
            print(f"  {role:<15} -> {count:>6,}  |  {dashboard}")
            total_all += count
        print(f"{'='*55}")
        print(f"  {'TOTAL':<15} -> {total_all:>6,}")
        print(f"{'='*55}")

        # ==================== SAMPLE CREDENTIALS ====================
        print(f"\n  SAMPLE EMPLOYEE CREDENTIALS")
        print(f"{'='*55}")
        for cred in employee_creds[:5]:
            print(f"  [{cred['role']:<13}]  {cred['username']:<30}  ->  {cred['password']}")

        print(f"\n  SAMPLE PATIENT CREDENTIALS")
        print(f"{'='*55}")
        for cred in patient_creds[:5]:
            print(f"  [Patient {cred['patient_id']:<5}]  {cred['username']:<30}  ->  {cred['password']}")

        print(f"\n  Password Format:")
        print(f"  FirstName(3 chars capitalized) + @ + ID(4 digits)")
        print(f"  Example: Ahmed, ID=1001  ->  Ahm@1001")
        print(f"\nAll Users created successfully!")

    except Exception as ex:
        print(f"Error: {ex}")
        if "conn" in locals():
            conn.rollback()
    finally:
        if "conn" in locals():
            conn.close()

if __name__ == "__main__":
    main()