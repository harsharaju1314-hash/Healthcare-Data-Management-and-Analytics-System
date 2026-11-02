-- ============================================================================
-- Healthcare Data Management and Analytics System
-- Oracle PL/SQL Package: PKG_HEALTHCARE_REPORTING
-- Organizes operational reporting procedures and analytical functions
-- ============================================================================

CREATE OR REPLACE PACKAGE PKG_HEALTHCARE_REPORTING AS
    -- Cursor types for reporting output
    TYPE t_report_cursor IS REF CURSOR;

    -- Custom Exceptions
    e_invalid_date_range EXCEPTION;
    PRAGMA EXCEPTION_INIT(e_invalid_date_range, -20010);

    -- Reporting Procedures
    PROCEDURE get_monthly_billing_report(
        p_year   IN  NUMBER,
        p_cursor OUT SYS_REFCURSOR
    );

    PROCEDURE get_appointment_statistics(
        p_start_date IN  DATE,
        p_end_date   IN  DATE,
        p_cursor     OUT SYS_REFCURSOR
    );

    PROCEDURE get_provider_utilization_report(
        p_start_date IN  DATE,
        p_end_date   IN  DATE,
        p_cursor     OUT SYS_REFCURSOR
    );

    PROCEDURE get_patient_visit_history(
        p_patient_id IN  NUMBER,
        p_cursor     OUT SYS_REFCURSOR
    );

    PROCEDURE get_outstanding_aging_report(
        p_cursor OUT SYS_REFCURSOR
    );

    -- Reporting Function
    FUNCTION calculate_total_revenue(
        p_start_date IN DATE,
        p_end_date   IN DATE
    ) RETURN NUMBER;

END PKG_HEALTHCARE_REPORTING;
/

CREATE OR REPLACE PACKAGE BODY PKG_HEALTHCARE_REPORTING AS

    -- ------------------------------------------------------------------------
    -- 1. Monthly Billing Report
    -- ------------------------------------------------------------------------
    PROCEDURE get_monthly_billing_report(
        p_year   IN  NUMBER,
        p_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT 
                TO_CHAR(billing_date, 'YYYY-MM') AS report_month,
                EXTRACT(MONTH FROM billing_date) AS month_num,
                COUNT(bill_id) AS total_bills,
                SUM(total_amount) AS total_billed,
                SUM(paid_amount) AS total_paid,
                SUM(balance_due) AS total_balance,
                ROUND(CASE WHEN SUM(total_amount) > 0 
                      THEN (SUM(paid_amount) / SUM(total_amount)) * 100 
                      ELSE 0 END, 2) AS collection_percentage
            FROM BILLING_RECORDS
            WHERE EXTRACT(YEAR FROM billing_date) = p_year
              AND status != 'CANCELLED'
            GROUP BY TO_CHAR(billing_date, 'YYYY-MM'), EXTRACT(MONTH FROM billing_date)
            ORDER BY month_num;
    END get_monthly_billing_report;

    -- ------------------------------------------------------------------------
    -- 2. Appointment Statistics Report
    -- ------------------------------------------------------------------------
    PROCEDURE get_appointment_statistics(
        p_start_date IN  DATE,
        p_end_date   IN  DATE,
        p_cursor     OUT SYS_REFCURSOR
    ) IS
    BEGIN
        IF p_start_date > p_end_date THEN
            RAISE_APPLICATION_ERROR(-20010, 'Start date cannot be after end date.');
        END IF;

        OPEN p_cursor FOR
            SELECT 
                status,
                COUNT(*) AS total_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM APPOINTMENTS 
                                          WHERE appointment_date BETWEEN p_start_date AND p_end_date), 2) AS status_percentage
            FROM APPOINTMENTS
            WHERE appointment_date BETWEEN p_start_date AND p_end_date
            GROUP BY status
            ORDER BY total_count DESC;
    END get_appointment_statistics;

    -- ------------------------------------------------------------------------
    -- 3. Provider Utilization Report
    -- ------------------------------------------------------------------------
    PROCEDURE get_provider_utilization_report(
        p_start_date IN  DATE,
        p_end_date   IN  DATE,
        p_cursor     OUT SYS_REFCURSOR
    ) IS
    BEGIN
        IF p_start_date > p_end_date THEN
            RAISE_APPLICATION_ERROR(-20010, 'Start date cannot be after end date.');
        END IF;

        OPEN p_cursor FOR
            SELECT 
                pr.provider_id,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.department,
                pr.specialty,
                COUNT(a.appointment_id) AS scheduled_appointments,
                COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed_appointments,
                COUNT(CASE WHEN a.status = 'CANCELLED' THEN 1 END) AS cancelled_appointments,
                ROUND(CASE WHEN COUNT(a.appointment_id) > 0 
                      THEN (COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) * 100.0 / COUNT(a.appointment_id))
                      ELSE 0 END, 2) AS utilization_rate_pct
            FROM PROVIDERS pr
            LEFT JOIN APPOINTMENTS a ON pr.provider_id = a.provider_id
                 AND a.appointment_date BETWEEN p_start_date AND p_end_date
            GROUP BY pr.provider_id, pr.first_name, pr.last_name, pr.department, pr.specialty
            ORDER BY utilization_rate_pct DESC;
    END get_provider_utilization_report;

    -- ------------------------------------------------------------------------
    -- 4. Patient Visit History Report
    -- ------------------------------------------------------------------------
    PROCEDURE get_patient_visit_history(
        p_patient_id IN  NUMBER,
        p_cursor     OUT SYS_REFCURSOR
    ) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT 
                e.encounter_id,
                e.encounter_date,
                e.encounter_type,
                pr.first_name || ' ' || pr.last_name AS attending_provider,
                pr.department,
                e.diagnosis_code,
                e.diagnosis_description,
                b.bill_number,
                NVL(b.total_amount, 0) AS bill_total,
                NVL(b.balance_due, 0) AS balance_due,
                NVL(b.status, 'N/A') AS billing_status
            FROM ENCOUNTERS e
            JOIN PROVIDERS pr ON e.provider_id = pr.provider_id
            LEFT JOIN BILLING_RECORDS b ON e.encounter_id = b.encounter_id
            WHERE e.patient_id = p_patient_id
            ORDER BY e.encounter_date DESC;
    END get_patient_visit_history;

    -- ------------------------------------------------------------------------
    -- 5. Outstanding Aging Report
    -- ------------------------------------------------------------------------
    PROCEDURE get_outstanding_aging_report(
        p_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT 
                CASE 
                    WHEN CURRENT_DATE <= due_date THEN 'Current (Not Due)'
                    WHEN TRUNC(CURRENT_DATE) - TRUNC(due_date) BETWEEN 1 AND 30 THEN '1-30 Days Overdue'
                    WHEN TRUNC(CURRENT_DATE) - TRUNC(due_date) BETWEEN 31 AND 60 THEN '31-60 Days Overdue'
                    WHEN TRUNC(CURRENT_DATE) - TRUNC(due_date) BETWEEN 61 AND 90 THEN '61-90 Days Overdue'
                    ELSE '90+ Days Overdue'
                END AS aging_category,
                COUNT(*) AS invoice_count,
                SUM(balance_due) AS total_outstanding_amount
            FROM BILLING_RECORDS
            WHERE balance_due > 0 AND status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE')
            GROUP BY 
                CASE 
                    WHEN CURRENT_DATE <= due_date THEN 'Current (Not Due)'
                    WHEN TRUNC(CURRENT_DATE) - TRUNC(due_date) BETWEEN 1 AND 30 THEN '1-30 Days Overdue'
                    WHEN TRUNC(CURRENT_DATE) - TRUNC(due_date) BETWEEN 31 AND 60 THEN '31-60 Days Overdue'
                    WHEN TRUNC(CURRENT_DATE) - TRUNC(due_date) BETWEEN 61 AND 90 THEN '61-90 Days Overdue'
                    ELSE '90+ Days Overdue'
                END
            ORDER BY total_outstanding_amount DESC;
    END get_outstanding_aging_report;

    -- ------------------------------------------------------------------------
    -- 6. Total Revenue Function
    -- ------------------------------------------------------------------------
    FUNCTION calculate_total_revenue(
        p_start_date IN DATE,
        p_end_date   IN DATE
    ) RETURN NUMBER IS
        v_total NUMBER(12, 2) := 0.00;
    BEGIN
        SELECT NVL(SUM(paid_amount), 0.00)
        INTO v_total
        FROM BILLING_RECORDS
        WHERE billing_date BETWEEN p_start_date AND p_end_date
          AND status != 'CANCELLED';

        RETURN v_total;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN 0.00;
    END calculate_total_revenue;

END PKG_HEALTHCARE_REPORTING;
/
