-- ============================================================================
-- Report 1: Monthly Billing Summary
-- Business Objective: Track hospital revenue streams, collection efficiency,
-- and outstanding receivables by month.
-- ============================================================================

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
    EXTRACT(MONTH FROM billing_date)
ORDER BY billing_year, month_number;
