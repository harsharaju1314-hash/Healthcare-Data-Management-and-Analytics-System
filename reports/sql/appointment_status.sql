-- ============================================================================
-- Report 2: Appointment Status and Cancellation Report
-- Business Objective: Analyze scheduling pipeline health, patient compliance,
-- and identify cancellation drivers across departments.
-- ============================================================================

WITH status_summary AS (
    SELECT 
        status,
        COUNT(*) AS total_appointments,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM APPOINTMENTS), 2) AS status_percentage
    FROM APPOINTMENTS
    GROUP BY status
),
department_cancellations AS (
    SELECT 
        pr.department,
        COUNT(a.appointment_id) AS total_scheduled,
        COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed_count,
        COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) AS cancelled_count,
        COUNT(CASE WHEN a.status = 'NO_SHOW' THEN 1 END) AS no_show_count,
        ROUND(
            CASE 
                WHEN COUNT(a.appointment_id) > 0 
                THEN (COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) * 100.0 / COUNT(a.appointment_id))
                ELSE 0 
            END, 2
        ) AS cancellation_rate_pct
    FROM APPOINTMENTS a
    JOIN PROVIDERS pr ON a.provider_id = pr.provider_id
    GROUP BY pr.department
)
SELECT 
    d.department,
    d.total_scheduled,
    d.completed_count,
    d.cancelled_count,
    d.no_show_count,
    d.cancellation_rate_pct
FROM department_cancellations d
ORDER BY d.total_scheduled DESC;
