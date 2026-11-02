-- ============================================================================
-- Report 4: Provider Appointment Utilization
-- Business Objective: Evaluate healthcare practitioner clinical workload,
-- completed vs booked consultations, and department billable productivity.
-- ============================================================================

SELECT 
    pr.provider_id,
    pr.first_name || ' ' || pr.last_name AS provider_name,
    pr.department,
    pr.specialty,
    COUNT(a.appointment_id) AS total_scheduled_appointments,
    COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed_appointments,
    COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) AS cancelled_appointments,
    COUNT(CASE WHEN a.status = 'NO_SHOW' THEN 1 END) AS no_show_appointments,
    COUNT(DISTINCT a.patient_id) AS unique_patients_treated,
    ROUND(
        CASE 
            WHEN COUNT(a.appointment_id) > 0 
            THEN (COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) * 100.0 / COUNT(a.appointment_id))
            ELSE 0 
        END, 2
    ) AS completion_rate_pct,
    COUNT(DISTINCT e.encounter_id) AS clinical_encounters_logged,
    NVL(SUM(b.total_amount), 0) AS total_revenue_generated
FROM PROVIDERS pr
LEFT JOIN APPOINTMENTS a ON pr.provider_id = a.provider_id
LEFT JOIN ENCOUNTERS e ON pr.provider_id = e.provider_id
LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id AND b.status != 'CANCELLED'
GROUP BY 
    pr.provider_id, pr.first_name, pr.last_name, pr.department, pr.specialty
ORDER BY total_scheduled_appointments DESC, completion_rate_pct DESC;
