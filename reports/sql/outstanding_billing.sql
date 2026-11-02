-- ============================================================================
-- Report 5: Outstanding Billing Aging Report
-- Business Objective: Identify delinquent patient receivables, segment balances
-- into aging brackets, and enable accounts receivable collection workflows.
-- ============================================================================

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
WHERE b.balance_due > 0 
  AND b.status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE')
ORDER BY b.due_date ASC, b.balance_due DESC;
