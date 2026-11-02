-- ============================================================================
-- Report 3: Longitudinal Patient Visit History
-- Business Objective: Produce a complete chronological timeline of patient care,
-- diagnoses, attending clinicians, and financial settlement.
-- ============================================================================

SELECT 
    p.patient_id,
    p.patient_mrn,
    p.first_name || ' ' || p.last_name AS patient_name,
    p.date_of_birth,
    p.gender,
    e.encounter_id,
    e.encounter_date,
    e.encounter_type,
    e.chief_complaint,
    e.diagnosis_code,
    e.diagnosis_description,
    pr.first_name || ' ' || pr.last_name AS attending_provider,
    pr.department,
    pr.specialty,
    b.bill_id,
    b.bill_number,
    b.total_amount,
    b.paid_amount,
    b.balance_due,
    b.status AS billing_status
FROM PATIENTS p
JOIN ENCOUNTERS e ON p.patient_id = e.patient_id
JOIN PROVIDERS pr ON e.provider_id = pr.provider_id
LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id
ORDER BY p.last_name, p.first_name, e.encounter_date DESC;
