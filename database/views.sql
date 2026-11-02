-- ============================================================================
-- Healthcare Data Management and Analytics System
-- Oracle Database Views
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. View: VW_PATIENT_CLINICAL_SUMMARY
-- Aggregates patient demographic, clinical history, and billing overview.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW VW_PATIENT_CLINICAL_SUMMARY AS
SELECT 
    p.patient_id,
    p.patient_mrn,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.date_of_birth,
    FLOOR(MONTHS_BETWEEN(CURRENT_DATE, p.date_of_birth) / 12) AS age,
    p.gender,
    p.blood_group,
    p.phone,
    p.email,
    p.is_active,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT e.encounter_id) AS total_encounters,
    MAX(e.encounter_date) AS latest_encounter_date,
    NVL(SUM(b.total_amount), 0) AS total_amount_billed,
    NVL(SUM(b.paid_amount), 0) AS total_amount_paid,
    NVL(SUM(b.balance_due), 0) AS current_outstanding_balance
FROM PATIENTS p
LEFT JOIN APPOINTMENTS a ON p.patient_id = a.patient_id
LEFT JOIN ENCOUNTERS e ON p.patient_id = e.patient_id
LEFT JOIN BILLING_RECORDS b ON p.patient_id = b.patient_id AND b.status != 'CANCELLED'
GROUP BY 
    p.patient_id, p.patient_mrn, p.first_name, p.last_name, 
    p.date_of_birth, p.gender, p.blood_group, p.phone, p.email, p.is_active;

-- ----------------------------------------------------------------------------
-- 2. View: VW_MONTHLY_BILLING_SUMMARY
-- Monthly aggregate billing metrics, revenues, and collection rates.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW VW_MONTHLY_BILLING_SUMMARY AS
SELECT 
    TO_CHAR(billing_date, 'YYYY-MM') AS billing_month,
    EXTRACT(YEAR FROM billing_date) AS billing_year,
    EXTRACT(MONTH FROM billing_date) AS month_number,
    COUNT(bill_id) AS total_invoices,
    SUM(total_amount) AS total_billed,
    SUM(paid_amount) AS total_collected,
    SUM(balance_due) AS total_outstanding,
    ROUND(
        CASE 
            WHEN SUM(total_amount) > 0 THEN (SUM(paid_amount) / SUM(total_amount)) * 100 
            ELSE 0 
        END, 2
    ) AS collection_rate_pct,
    COUNT(CASE WHEN status = 'PAID' THEN 1 END) AS paid_invoices_count,
    COUNT(CASE WHEN status = 'PENDING' THEN 1 END) AS pending_invoices_count,
    COUNT(CASE WHEN status = 'OVERDUE' THEN 1 END) AS overdue_invoices_count
FROM BILLING_RECORDS
WHERE status != 'CANCELLED'
GROUP BY 
    TO_CHAR(billing_date, 'YYYY-MM'),
    EXTRACT(YEAR FROM billing_date),
    EXTRACT(MONTH FROM billing_date);

-- ----------------------------------------------------------------------------
-- 3. View: VW_APPOINTMENT_ANALYTICS
-- Appointment scheduling operational metrics joined with provider & patient info.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW VW_APPOINTMENT_ANALYTICS AS
SELECT 
    a.appointment_id,
    a.appointment_date,
    a.appointment_time,
    a.appointment_datetime,
    a.status AS appointment_status,
    a.reason_for_visit,
    a.cancellation_reason,
    p.patient_id,
    p.patient_mrn,
    p.first_name || ' ' || p.last_name AS patient_name,
    pr.provider_id,
    pr.first_name || ' ' || pr.last_name AS provider_name,
    pr.department,
    pr.specialty,
    CASE WHEN a.status = 'CANCELLED' THEN 1 ELSE 0 END AS is_cancelled,
    CASE WHEN a.status = 'COMPLETED' THEN 1 ELSE 0 END AS is_completed,
    CASE WHEN a.status = 'NO_SHOW' THEN 1 ELSE 0 END AS is_no_show
FROM APPOINTMENTS a
INNER JOIN PATIENTS p ON a.patient_id = p.patient_id
INNER JOIN PROVIDERS pr ON a.provider_id = pr.provider_id;

-- ----------------------------------------------------------------------------
-- 4. View: VW_PROVIDER_WORKLOAD
-- Provider performance, patient volume, and appointment completion rates.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW VW_PROVIDER_WORKLOAD AS
SELECT 
    pr.provider_id,
    pr.first_name || ' ' || pr.last_name AS provider_name,
    pr.department,
    pr.specialty,
    COUNT(a.appointment_id) AS total_scheduled_appointments,
    COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed_appointments,
    COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) AS cancelled_appointments,
    COUNT(CASE WHEN a.status = 'NO_SHOW' THEN 1 END) AS no_show_appointments,
    COUNT(DISTINCT a.patient_id) AS unique_patients_scheduled,
    ROUND(
        CASE 
            WHEN COUNT(a.appointment_id) > 0 
            THEN (COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) * 100.0 / COUNT(a.appointment_id))
            ELSE 0 
        END, 2
    ) AS completion_rate_pct,
    COUNT(e.encounter_id) AS total_clinical_encounters,
    NVL(SUM(b.total_amount), 0) AS total_revenue_generated
FROM PROVIDERS pr
LEFT JOIN APPOINTMENTS a ON pr.provider_id = a.provider_id
LEFT JOIN ENCOUNTERS e ON pr.provider_id = e.provider_id
LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id AND b.status != 'CANCELLED'
GROUP BY 
    pr.provider_id, pr.first_name, pr.last_name, pr.department, pr.specialty;

-- ----------------------------------------------------------------------------
-- 5. View: VW_OUTSTANDING_BALANCES
-- Detailed aging analysis of unpaid bills with categorized overdue buckets.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW VW_OUTSTANDING_BALANCES AS
SELECT 
    b.bill_id,
    b.bill_number,
    b.patient_id,
    p.patient_mrn,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.phone AS patient_phone,
    p.email AS patient_email,
    b.billing_date,
    b.due_date,
    b.total_amount,
    b.paid_amount,
    b.balance_due,
    b.status,
    TRUNC(CURRENT_DATE) - TRUNC(b.due_date) AS days_overdue,
    CASE 
        WHEN CURRENT_DATE <= b.due_date THEN 'Current (Not Due)'
        WHEN TRUNC(CURRENT_DATE) - TRUNC(b.due_date) BETWEEN 1 AND 30 THEN '1-30 Days Overdue'
        WHEN TRUNC(CURRENT_DATE) - TRUNC(b.due_date) BETWEEN 31 AND 60 THEN '31-60 Days Overdue'
        WHEN TRUNC(CURRENT_DATE) - TRUNC(b.due_date) BETWEEN 61 AND 90 THEN '61-90 Days Overdue'
        ELSE '90+ Days Overdue'
    END AS aging_bucket
FROM BILLING_RECORDS b
INNER JOIN PATIENTS p ON b.patient_id = p.patient_id
WHERE b.balance_due > 0 AND b.status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE');

COMMIT;
