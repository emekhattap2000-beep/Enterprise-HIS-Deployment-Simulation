USE HospitalManagementSystem;
GO
CREATE VIEW vw_PatientRegistry AS
SELECT
    P.Patient_ID                                    AS PatientID,
    P.First_name + ' ' + P.Last_name               AS FullName,
    CASE P.P_gender
        WHEN 'M' THEN 'Male'
        WHEN 'F' THEN 'Female'
    END                                             AS Gender,
    P.P_DOB                                         AS DOB,
    DATEDIFF(YEAR, P.P_DOB, GETDATE())
    - CASE
        WHEN MONTH(P.P_DOB) > MONTH(GETDATE())
          OR (MONTH(P.P_DOB) = MONTH(GETDATE())
         AND DAY(P.P_DOB)   > DAY(GETDATE()))
        THEN 1 ELSE 0
      END                                           AS PatientAge,
    -- استخراج المدينة من العنوان (الجزء بعد الفاصلة الأولى)
    TRIM(
        SUBSTRING(
            P.P_Address,
            CHARINDEX(',', P.P_Address) + 1,
            CHARINDEX(',', P.P_Address + ',', CHARINDEX(',', P.P_Address) + 1)
            - CHARINDEX(',', P.P_Address) - 1
        )
    )                                               AS City,
    P.P_phone                                       AS Phone,
    P.created_at                                    AS RegistrationDate
FROM PATIENTS P;

GO

-- ==================== USAGE QUERY ====================
-- Top 20 Newest Patients

SELECT TOP 20
    RegistrationDate,
    PatientID,
    FullName,
    Gender,
    DOB,
    PatientAge,
    City,
    Phone
FROM vw_PatientRegistry
ORDER BY RegistrationDate DESC;


-- ==================== Q2: Daily Appointments Schedule Per Doctor ====================

-- غير الـ DoctorID والتاريخ حسب اللي عايزه
DECLARE @DoctorID INT  = 1001        -- ← غير الرقم ده
DECLARE @Date     DATE = GETDATE()   -- ← أو حط تاريخ معين مثلاً '2024-06-15'

SELECT
    -- Doctor Info
    E.FirstName + ' ' + E.LastName                          AS DoctorName,
    D.specialty                                              AS Specialization,
    DEP.department_name                                      AS DepartmentName,

    -- Appointment Info
    A.Appointment_DateTime                                   AS AppointmentTime,
    CONVERT(VARCHAR(5), A.Appointment_DateTime, 108)         AS AppointmentHour,

    -- Patient Info
    P.First_name + ' ' + P.Last_name                        AS PatientName,
    DATEDIFF(YEAR, P.P_DOB, GETDATE())                      AS PatientAge,
    P.P_phone                                                AS PatientPhone,

    -- Status
    A.Appointment_status                                     AS AppointmentStatus,
    A.Visit_Reason                                           AS VisitReason,

    -- CheckIn
    CASE
        WHEN A.CheckInTime IS NOT NULL
        THEN CONVERT(VARCHAR(5), A.CheckInTime, 108)
        ELSE 'Not Checked In'
    END                                                      AS CheckInTime,

    -- وقت الانتظار لو اتسجل دخول
    CASE
        WHEN A.CheckInTime IS NOT NULL
        THEN CONCAT(
            DATEDIFF(MINUTE, A.Appointment_DateTime, A.CheckInTime),
            ' min'
        )
        ELSE '-'
    END                                                      AS WaitTime,

    -- Registered By
    RE.FirstName + ' ' + RE.LastName                        AS RegisteredBy

FROM       APPOINTMENTS   A
JOIN       DOCTORS        D   ON A.Doctor_ID       = D.Dr_ID
JOIN       EMPLOYEES      E   ON D.Dr_ID           = E.Emp_ID
JOIN       DEPARTMENTS    DEP ON E.Dep_Id          = DEP.Department_ID
JOIN       PATIENTS       P   ON A.PatientID       = P.Patient_ID
JOIN       RECEPTIONIST   R   ON A.Receptionist_ID = R.Recep_ID
JOIN       EMPLOYEES      RE  ON R.Recep_ID        = RE.Emp_ID

WHERE
    A.Doctor_ID            = @DoctorID
    AND CAST(A.Appointment_DateTime AS DATE) = @Date

ORDER BY
    A.Appointment_DateTime ASC;



-- ==================== CREATE VIEW ====================

CREATE VIEW vw_DailyDoctorSchedule AS
SELECT
    -- Doctor Info
    D.Dr_ID                                                  AS DoctorID,
    E.FirstName + ' ' + E.LastName                          AS DoctorName,
    D.specialty                                              AS Specialization,
    DEP.department_name                                      AS DepartmentName,
    D.available_schedule                                     AS DoctorSchedule,

    -- Appointment Info
    A.Appointment_ID                                         AS AppointmentID,
    A.Appointment_DateTime                                   AS AppointmentTime,
    CONVERT(VARCHAR(5), A.Appointment_DateTime, 108)         AS AppointmentHour,

    -- Patient Info
    P.Patient_ID                                             AS PatientID,
    P.First_name + ' ' + P.Last_name                        AS PatientName,
    DATEDIFF(YEAR, P.P_DOB, GETDATE())
    - CASE
        WHEN MONTH(P.P_DOB) > MONTH(GETDATE())
          OR (MONTH(P.P_DOB)  = MONTH(GETDATE())
         AND  DAY(P.P_DOB)    > DAY(GETDATE()))
        THEN 1 ELSE 0
      END                                                    AS PatientAge,
    P.P_phone                                                AS PatientPhone,

    -- Visit Details
    A.Visit_Reason                                           AS VisitReason,
    A.Appointment_status                                     AS AppointmentStatus,

    -- Check In
    CASE
        WHEN A.CheckInTime IS NOT NULL
        THEN CONVERT(VARCHAR(5), A.CheckInTime, 108)
        ELSE 'Not Checked In'
    END                                                      AS CheckInTime,

    -- Wait Time
    CASE
        WHEN A.CheckInTime IS NOT NULL
        THEN CONCAT(
            DATEDIFF(MINUTE, A.Appointment_DateTime, A.CheckInTime),
            ' min'
        )
        ELSE '-'
    END                                                      AS WaitTime,

    -- Registered By
    RE.FirstName + ' ' + RE.LastName                        AS RegisteredBy

FROM       APPOINTMENTS   A
JOIN       DOCTORS        D   ON A.Doctor_ID       = D.Dr_ID
JOIN       EMPLOYEES      E   ON D.Dr_ID           = E.Emp_ID
JOIN       DEPARTMENTS    DEP ON E.Dep_Id          = DEP.Department_ID
JOIN       PATIENTS       P   ON A.PatientID       = P.Patient_ID
JOIN       RECEPTIONIST   R   ON A.Receptionist_ID = R.Recep_ID
JOIN       EMPLOYEES      RE  ON R.Recep_ID        = RE.Emp_ID

WHERE CAST(A.Appointment_DateTime AS DATE) = CAST(GETDATE() AS DATE);

GO


-- ==================== USAGE QUERIES ====================

-- 1. كل مواعيد اليوم مرتبة بالوقت
SELECT *
FROM vw_DailyDoctorSchedule
ORDER BY AppointmentTime ASC;

-- 2. مواعيد دكتور معين النهارده
SELECT *
FROM vw_DailyDoctorSchedule
WHERE DoctorID = 1001
ORDER BY AppointmentTime ASC;

-- 3. ملخص كل دكتور النهارده
SELECT
    DoctorID,
    DoctorName,
    DepartmentName,
    COUNT(*)                                                         AS TotalAppointments,
    SUM(CASE WHEN AppointmentStatus = 'Completed'  THEN 1 ELSE 0 END) AS Completed,
    SUM(CASE WHEN AppointmentStatus = 'Scheduled'  THEN 1 ELSE 0 END) AS Scheduled,
    SUM(CASE WHEN AppointmentStatus = 'Cancelled'  THEN 1 ELSE 0 END) AS Cancelled,
    SUM(CASE WHEN AppointmentStatus = 'No_Show'    THEN 1 ELSE 0 END) AS NoShow,
    MIN(AppointmentHour)                                             AS FirstAppointment,
    MAX(AppointmentHour)                                             AS LastAppointment
FROM vw_DailyDoctorSchedule
GROUP BY DoctorID, DoctorName, DepartmentName
ORDER BY TotalAppointments DESC;

-- 4. المواعيد اللي لسه مجاش المريض (Scheduled)
SELECT
    DoctorName,
    DepartmentName,
    AppointmentHour,
    PatientName,
    PatientPhone,
    VisitReason
FROM vw_DailyDoctorSchedule
WHERE AppointmentStatus = 'Scheduled'
ORDER BY AppointmentTime ASC;






-- ==================== Q3: No-Show Rate Per Department (Last 3 Months) ====================

SELECT
    DEP.department_name                                          AS DepartmentName,
    D.specialty                                                  AS Specialization,

    -- Totals
    COUNT(A.Appointment_ID)                                      AS TotalAppointments,
    SUM(CASE WHEN A.Appointment_status = 'No_Show' THEN 1 ELSE 0 END) AS NoShows,
    SUM(CASE WHEN A.Appointment_status = 'Completed'  THEN 1 ELSE 0 END) AS Completed,
    SUM(CASE WHEN A.Appointment_status = 'Cancelled'  THEN 1 ELSE 0 END) AS Cancelled,
    SUM(CASE WHEN A.Appointment_status = 'Scheduled'  THEN 1 ELSE 0 END) AS Scheduled,

    -- No-Show Rate
    CAST(
        ROUND(
            100.0
            * SUM(CASE WHEN A.Appointment_status = 'No_Show' THEN 1 ELSE 0 END)
            / NULLIF(COUNT(A.Appointment_ID), 0),
        2)
    AS DECIMAL(5,2))                                             AS NoShowRate_Pct,

    -- Completion Rate
    CAST(
        ROUND(
            100.0
            * SUM(CASE WHEN A.Appointment_status = 'Completed' THEN 1 ELSE 0 END)
            / NULLIF(COUNT(A.Appointment_ID), 0),
        2)
    AS DECIMAL(5,2))                                             AS CompletionRate_Pct,

    -- Date Range
    CAST(DATEADD(MONTH, -3, GETDATE()) AS DATE)                  AS PeriodStart,
    CAST(GETDATE() AS DATE)                                      AS PeriodEnd

FROM       APPOINTMENTS  A
JOIN       DOCTORS       D   ON A.Doctor_ID  = D.Dr_ID
JOIN       EMPLOYEES     E   ON D.Dr_ID      = E.Emp_ID
JOIN       DEPARTMENTS   DEP ON E.Dep_Id     = DEP.Department_ID

WHERE A.Appointment_DateTime >= DATEADD(MONTH, -3, GETDATE())
  AND A.Appointment_DateTime <= GETDATE()

GROUP BY
    DEP.department_name,
    D.specialty

HAVING COUNT(A.Appointment_ID) > 0

ORDER BY NoShowRate_Pct DESC;






-- ==================== Q4 : CREATE VIEW ====================

CREATE VIEW vw_PatientVisitSummary AS
SELECT 
    P.Patient_ID,
    P.First_name + ' ' + P.Last_name AS PatientName,
    
    -- 1. إجمالي المواعيد
    COUNT(A.Appointment_ID) AS TotalVisits,
    
    -- 2. تاريخ آخر زيارة (من الكروس أبلاي)
    CAST(LastVisit.Appointment_DateTime AS DATE) AS LastVisitDate,
    
    -- 3. اسم آخر دكتور (من الموظفين المرتبطين بالدكتور في آخر موعد)
    E.FirstName + ' ' + E.LastName AS LastDoctorSeen,
    
    -- 4. آخر تشخيص (من جدول السجلات الطبية المرتبط بآخر موعد)
    ISNULL(MR.Diagnosis, 'No Diagnosis Recorded') AS LastDiagnosis

FROM PATIENTS P
-- نربط كل المواعيد لحساب الإجمالي (Inner Join لاستبعاد من ليس له مواعيد)
INNER JOIN APPOINTMENTS A ON P.Patient_ID = A.PatientID

-- الـ "مقص" اللي بيجيب لنا سطر واحد فقط (آخر موعد)
CROSS APPLY (
    SELECT TOP 1 
        App.Appointment_ID, 
        App.Appointment_DateTime, 
        App.Doctor_ID
    FROM APPOINTMENTS App
    WHERE App.PatientID = P.Patient_ID 
      AND App.Appointment_status = 'Completed'
    ORDER BY App.Appointment_DateTime DESC
) AS LastVisit

-- نربط اسم الدكتور الخاص بهذا الموعد فقط
LEFT JOIN EMPLOYEES E ON LastVisit.Doctor_ID = E.Emp_ID

-- نربط التشخيص الخاص بهذا الموعد فقط (باستخدام المفتاح الأجنبي AppID)
LEFT JOIN Medical_Records MR ON LastVisit.Appointment_ID = MR.AppID

GROUP BY 
    P.Patient_ID, 
    P.First_name, 
    P.Last_name, 
    LastVisit.Appointment_DateTime, 
    E.FirstName, 
    E.LastName, 
    MR.Diagnosis;
GO

-- ==================== USAGE QUERIES ====================

-- 1. كل المرضى مرتبين بآخر زيارة
SELECT *
FROM vw_PatientVisitSummary
ORDER BY LastVisitDate DESC;

-- 2. مريض معين
SELECT *
FROM vw_PatientVisitSummary
WHERE Patient_ID = 1;







-- ==================== Q5: Frequent Patients (5+ Visits in Last 6 Months) ====================

SELECT 
    P.First_name + ' ' + P.Last_name AS PatientName,
    P.P_phone AS Phone,
    COUNT(A.Appointment_ID) AS TotalVisits,
    MAX(CAST(A.Appointment_DateTime AS DATE)) AS LastVisitDate

FROM PATIENTS P
INNER JOIN APPOINTMENTS A ON P.Patient_ID = A.PatientID

WHERE 
    -- فلتر آخر 6 أشهر من تاريخ اليوم
    A.Appointment_DateTime >= DATEADD(MONTH, -6, GETDATE()) 
    AND A.Appointment_status = 'Completed'

GROUP BY 
    P.Patient_ID, 
    P.First_name, 
    P.Last_name, 
    P.P_phone

HAVING 
    -- فلتر العدد (أكثر من 5 زيارات)
    COUNT(A.Appointment_ID) > 5

ORDER BY 
    TotalVisits DESC;


-- ==================== Q6: Top 10 Most Prescribed Medications (Last 90 Days) ====================

WITH MedicationCounts AS (
    -- 1. نحدد أكثر 10 أدوية تم صرفها في آخر 90 يوم
    SELECT TOP 10 
        medication_name AS MedicationName, 
        COUNT(*) AS PrescriptionsCount
    FROM Prescription
    WHERE prescription_date >= DATEADD(DAY, -90, GETDATE())
    GROUP BY medication_name
    ORDER BY PrescriptionsCount DESC
),
DepartmentUsage AS (
    -- 2. نحسب تكرار كل دواء في كل قسم
    SELECT 
        PR.medication_name,
        DEP.department_name,
        COUNT(*) AS UsageInDept,
        ROW_NUMBER() OVER (PARTITION BY PR.medication_name ORDER BY COUNT(*) DESC) as RankNum
    FROM Prescription PR
    JOIN DOCTORS D ON PR.doctor_id = D.Dr_ID
    JOIN EMPLOYEES E ON D.Dr_ID = E.Emp_ID
    JOIN DEPARTMENTS DEP ON E.Dep_Id = DEP.Department_ID
    WHERE PR.prescription_date >= DATEADD(DAY, -90, GETDATE())
    GROUP BY PR.medication_name, DEP.department_name
)
-- 3. نربط النتائج ببعضها
SELECT 
    MC.MedicationName,
    MC.PrescriptionsCount,
    DU.department_name AS TopDepartment
FROM MedicationCounts MC
JOIN DepartmentUsage DU ON MC.MedicationName = DU.medication_name
WHERE DU.RankNum = 1 -- نأخذ القسم صاحب المركز الأول فقط لكل دواء
ORDER BY MC.PrescriptionsCount DESC;


-- ==================== BONUS QUERIES ====================


CREATE VIEW vw_TopMedications_Last90Days AS
WITH MedicationCounts AS (
    -- 1. نحدد أكثر 10 أدوية تم صرفها في آخر 90 يوم
    SELECT TOP 10 
        medication_name AS MedicationName, 
        COUNT(*) AS PrescriptionsCount
    FROM Prescription
    WHERE prescription_date >= DATEADD(DAY, -90, GETDATE())
    GROUP BY medication_name
    ORDER BY COUNT(*) DESC
),
DepartmentUsage AS (
    -- 2. نحسب تكرار كل دواء في كل قسم مع ترتيب الأقسام لكل دواء
    SELECT 
        PR.medication_name,
        DEP.department_name,
        COUNT(*) AS UsageInDept,
        ROW_NUMBER() OVER (PARTITION BY PR.medication_name ORDER BY COUNT(*) DESC) as RankNum
    FROM Prescription PR
    JOIN DOCTORS D ON PR.doctor_id = D.Dr_ID
    JOIN EMPLOYEES E ON D.Dr_ID = E.Emp_ID
    JOIN DEPARTMENTS DEP ON E.Dep_Id = DEP.Department_ID
    WHERE PR.prescription_date >= DATEADD(DAY, -90, GETDATE())
    GROUP BY PR.medication_name, DEP.department_name
)
-- 3. نربط النتائج النهائية
SELECT 
    MC.MedicationName,
    MC.PrescriptionsCount,
    DU.department_name AS TopDepartment
FROM MedicationCounts MC
JOIN DepartmentUsage DU ON MC.MedicationName = DU.medication_name
WHERE DU.RankNum = 1; -- نأخذ القسم الأكثر استخداماً لهذا الدواء فقط

GO

-- ==================== USAGE ====================

SELECT * FROM vw_TopMedications_Last90Days
ORDER BY PrescriptionsCount DESC;















-- ==================== Q7: Lab Test Turnaround Time ====================

SELECT
    LT.Test_Name AS TestName,
    
    -- حساب المتوسط بالساعات (تحويل الفرق لدقائق ثم قسمته على 60)
    CAST(
        AVG(DATEDIFF(MINUTE, LT.order_date_time, LT.Result_date_Time)) / 60.0 
    AS DECIMAL(5,2)) AS AvgTurnaroundHours

FROM Lab_Tests LT

WHERE
    -- فيلتر آخر 30 يوم
    LT.order_date_time >= DATEADD(DAY, -30, GETDATE())
    -- التأكد أن التحليل مكتمل (يوجد تاريخ نتيجة)
    AND LT.Result_date_Time IS NOT NULL
    -- التأكد أن البيانات منطقية (تاريخ النتيجة بعد تاريخ الطلب)
    AND LT.Result_date_Time > LT.order_date_time

GROUP BY LT.Test_Name

ORDER BY AvgTurnaroundHours ASC;

GO







-- ==================== CREATE VIEW ====================

CREATE VIEW vw_InvoiceAging AS
SELECT
    I.Invoice_ID                                 AS InvoiceID,
    P.First_name + ' ' + P.Last_name             AS PatientName,
    I.Invoice_date                               AS InvoiceDate,
    I.Total_Amount                               AS TotalAmount,
    I.Paid_Amount                                AS PaidAmount,
    I.outstanding_Amount                         AS OutstandingAmount,

    -- Aging Bucket: تقسيم الفواتير حسب مدة التأخير
    CASE
        WHEN DATEDIFF(DAY, I.Invoice_date, GETDATE()) BETWEEN 0  AND 30  THEN '0-30 days'
        WHEN DATEDIFF(DAY, I.Invoice_date, GETDATE()) BETWEEN 31 AND 60  THEN '31-60 days'
        WHEN DATEDIFF(DAY, I.Invoice_date, GETDATE()) BETWEEN 61 AND 90  THEN '61-90 days'
        ELSE                                                               '90+ days'
    END                                          AS AgingBucket

FROM INVOICES I
JOIN PATIENTS P ON I.Patient_ID = P.Patient_ID

-- فلترة الفواتير غير المدفوعة فقط (أو المدفوعة جزئياً)
WHERE I.Payment_status IN ('Unpaid', 'Partial Paid') 
  OR I.outstanding_Amount > 0;
GO

-- ==================== USAGE QUERIES ====================

SELECT 
    AgingBucket, 
    COUNT(InvoiceID) AS NumberOfInvoices,
    SUM(OutstandingAmount) AS TotalOutstanding,
    
    -- حساب النسبة المئوية لكل فئة من إجمالي الديون الكلية
    CAST(
        (SUM(OutstandingAmount) * 100.0) / SUM(SUM(OutstandingAmount)) OVER() 
    AS DECIMAL(5,2)) AS PercentageOfTotal

FROM vw_InvoiceAging
GROUP BY AgingBucket
ORDER BY 
    CASE 
        WHEN AgingBucket = '0-30 days'  THEN 1
        WHEN AgingBucket = '31-60 days' THEN 2
        WHEN AgingBucket = '61-90 days' THEN 3
        ELSE                                 4
    END;
















-- ==================== Q9: Monthly Revenue & Payment Breakdown (Last 12 Months) ====================

SELECT
    FORMAT(I.Invoice_date, 'yyyy-MM') AS YearMonth,
    
    -- الإجماليات المطلوبة
    SUM(I.Total_Amount)               AS TotalBilled,
    SUM(I.Paid_Amount)                AS TotalPaid,
    SUM(I.outstanding_Amount)         AS Outstanding,

    -- تفصيل طرق الدفع (Breakdown)
    SUM(CASE WHEN I.Paymentmethod = 'Cash'        THEN I.Paid_Amount ELSE 0 END) AS Cash_Paid,
    SUM(CASE WHEN I.Paymentmethod = 'Credit Card' THEN I.Paid_Amount ELSE 0 END) AS Card_Paid,
    SUM(CASE WHEN I.Paymentmethod = 'Insurance'   THEN I.Paid_Amount ELSE 0 END) AS Insurance_Paid

FROM INVOICES I
WHERE I.Invoice_date >= DATEADD(MONTH, -12, GETDATE())
GROUP BY FORMAT(I.Invoice_date, 'yyyy-MM')
ORDER BY YearMonth DESC;

GO






-- ==================== Q10) CREATE VIEW ====================

CREATE VIEW vw_DoctorPerformance AS
SELECT
    E.FirstName + ' ' + E.LastName AS DoctorName,
    
    -- 1. إجمالي المواعيد
    COUNT(A.Appointment_ID) AS TotalAppointments,
    
    -- 2. الزيارات المكتملة
    SUM(CASE WHEN A.Appointment_status = 'Completed' THEN 1 ELSE 0 END) AS CompletedVisits,
    
    -- 3. حالات عدم الحضور
    SUM(CASE WHEN A.Appointment_status = 'No_Show' THEN 1 ELSE 0 END) AS NoShows,
    
    -- 4. إجمالي الفواتير المرتبطة بالدكتور
    ISNULL(SUM(I.Total_Amount), 0) AS TotalBilledAmount,
    
    -- 5. متوسط وقت انتظار المريض (بالدقائق)
    AVG(CASE 
            WHEN A.CheckInTime IS NOT NULL 
            THEN DATEDIFF(MINUTE, A.Appointment_DateTime, A.CheckInTime) 
            ELSE NULL 
        END) AS AvgPatientWaitTime

FROM DOCTORS D
JOIN EMPLOYEES E ON D.Dr_ID = E.Emp_ID
LEFT JOIN APPOINTMENTS A ON D.Dr_ID = A.Doctor_ID
LEFT JOIN INVOICES I ON A.Appointment_ID = I.App_ID

-- فلترة آخر 30 يوم فقط
WHERE A.Appointment_DateTime >= DATEADD(DAY, -30, GETDATE())

GROUP BY E.FirstName, E.LastName;
GO
-- ==================== USAGE QUERIES ====================

SELECT 
    DoctorName, 
    AvgPatientWaitTime, 
    CompletedVisits
FROM vw_DoctorPerformance
WHERE AvgPatientWaitTime > 0 -- استبعاد من ليس لديهم بيانات دخول (Check-in)
ORDER BY AvgPatientWaitTime ASC;