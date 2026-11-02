-- ============================================================================
-- Healthcare Data Management and Analytics System
-- Oracle PL/SQL Functions
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Function: FN_CALC_OUTSTANDING_BALANCE
-- Calculates the total unpaid balance for a given patient.
-- Returns 0 if patient has no pending balances.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_CALC_OUTSTANDING_BALANCE(
    p_patient_id IN NUMBER
) RETURN NUMBER
IS
    v_total_balance NUMBER(10, 2) := 0.00;
    v_patient_exists NUMBER := 0;
BEGIN
    -- Verify patient exists
    SELECT COUNT(*) INTO v_patient_exists 
    FROM PATIENTS 
    WHERE patient_id = p_patient_id;

    IF v_patient_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Patient ID ' || p_patient_id || ' does not exist.');
    END IF;

    -- Aggregate balance due for all active invoices
    SELECT NVL(SUM(balance_due), 0.00)
    INTO v_total_balance
    FROM BILLING_RECORDS
    WHERE patient_id = p_patient_id
      AND status IN ('PENDING', 'PARTIALLY_PAID', 'OVERDUE');

    RETURN v_total_balance;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0.00;
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20099, 'Error calculating balance: ' || SQLERRM);
END FN_CALC_OUTSTANDING_BALANCE;
/

-- ----------------------------------------------------------------------------
-- 2. Function: FN_VALIDATE_BILLING_AMOUNT
-- Validates that monetary amounts satisfy business rules:
-- Returns 1 (VALID) or 0 (INVALID)
-- Rules: total >= 0, paid >= 0, paid <= total, balance_due = total - paid
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_VALIDATE_BILLING_AMOUNT(
    p_total   IN NUMBER,
    p_paid    IN NUMBER,
    p_balance IN NUMBER
) RETURN NUMBER
IS
BEGIN
    IF p_total IS NULL OR p_paid IS NULL OR p_balance IS NULL THEN
        RETURN 0;
    END IF;

    IF p_total < 0 OR p_paid < 0 OR p_balance < 0 THEN
        RETURN 0;
    END IF;

    IF p_paid > p_total THEN
        RETURN 0;
    END IF;

    IF (p_paid + p_balance) != p_total THEN
        RETURN 0;
    END IF;

    RETURN 1;
END FN_VALIDATE_BILLING_AMOUNT;
/

-- ----------------------------------------------------------------------------
-- 3. Function: FN_GET_PROVIDER_UTILIZATION
-- Returns percentage of completed appointments out of total scheduled for a provider.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_GET_PROVIDER_UTILIZATION(
    p_provider_id IN NUMBER,
    p_start_date  IN DATE,
    p_end_date    IN DATE
) RETURN NUMBER
IS
    v_total_appts NUMBER := 0;
    v_completed_appts NUMBER := 0;
    v_utilization_pct NUMBER(5, 2) := 0.00;
BEGIN
    SELECT 
        COUNT(*),
        COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END)
    INTO v_total_appts, v_completed_appts
    FROM APPOINTMENTS
    WHERE provider_id = p_provider_id
      AND appointment_date BETWEEN p_start_date AND p_end_date;

    IF v_total_appts = 0 THEN
        RETURN 0.00;
    END IF;

    v_utilization_pct := ROUND((v_completed_appts * 100.0) / v_total_appts, 2);
    RETURN v_utilization_pct;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0.00;
END FN_GET_PROVIDER_UTILIZATION;
/
