-- ============================================================================
-- Healthcare Data Management and Analytics System
-- Oracle PL/SQL Stored Procedures
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Procedure: SP_CANCEL_APPOINTMENT
-- Safely cancels a scheduled appointment and updates audit metadata.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_CANCEL_APPOINTMENT(
    p_appointment_id       IN  NUMBER,
    p_cancellation_reason  IN  VARCHAR2,
    p_success_out          OUT NUMBER,
    p_message_out          OUT VARCHAR2
)
IS
    v_current_status VARCHAR2(20);
BEGIN
    p_success_out := 0;

    -- Validate reason provided
    IF p_cancellation_reason IS NULL OR TRIM(p_cancellation_reason) = '' THEN
        p_message_out := 'Cancellation reason is required.';
        RETURN;
    END IF;

    -- Fetch current status
    BEGIN
        SELECT status INTO v_current_status
        FROM APPOINTMENTS
        WHERE appointment_id = p_appointment_id
        FOR UPDATE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_message_out := 'Appointment ID ' || p_appointment_id || ' does not exist.';
            RETURN;
    END;

    -- Enforce business rules on cancellation
    IF v_current_status = 'CANCELLED' THEN
        p_message_out := 'Appointment is already cancelled.';
        RETURN;
    ELSIF v_current_status = 'COMPLETED' THEN
        p_message_out := 'Cannot cancel an appointment that has already been completed.';
        RETURN;
    END IF;

    -- Perform update
    UPDATE APPOINTMENTS
    SET status = 'CANCELLED',
        cancellation_reason = p_cancellation_reason,
        cancelled_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
    WHERE appointment_id = p_appointment_id;

    p_success_out := 1;
    p_message_out := 'Appointment successfully cancelled.';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_success_out := 0;
        p_message_out := 'Database error during cancellation: ' || SQLERRM;
END SP_CANCEL_APPOINTMENT;
/

-- ----------------------------------------------------------------------------
-- 2. Procedure: SP_RECORD_CLINICAL_ENCOUNTER
-- Completes the clinical visit workflow: records encounter, completes appointment,
-- and automatically generates an initial billing record in one transaction.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_RECORD_CLINICAL_ENCOUNTER(
    p_patient_id             IN  NUMBER,
    p_provider_id            IN  NUMBER,
    p_appointment_id         IN  NUMBER,
    p_encounter_type         IN  VARCHAR2,
    p_chief_complaint        IN  VARCHAR2,
    p_clinical_notes         IN  VARCHAR2,
    p_diagnosis_code         IN  VARCHAR2,
    p_diagnosis_description  IN  VARCHAR2,
    p_billing_amount         IN  NUMBER,
    p_encounter_id_out       OUT NUMBER,
    p_bill_id_out            OUT NUMBER,
    p_status_out             OUT VARCHAR2
)
IS
    v_bill_num VARCHAR2(30);
    v_patient_count NUMBER;
    v_provider_count NUMBER;
BEGIN
    -- Verify patient & provider
    SELECT COUNT(*) INTO v_patient_count FROM PATIENTS WHERE patient_id = p_patient_id;
    IF v_patient_count = 0 THEN
        p_status_out := 'ERROR: Invalid patient ID.';
        RETURN;
    END IF;

    SELECT COUNT(*) INTO v_provider_count FROM PROVIDERS WHERE provider_id = p_provider_id;
    IF v_provider_count = 0 THEN
        p_status_out := 'ERROR: Invalid provider ID.';
        RETURN;
    END IF;

    -- Insert encounter
    INSERT INTO ENCOUNTERS (
        patient_id, provider_id, appointment_id,
        encounter_type, chief_complaint, clinical_notes,
        diagnosis_code, diagnosis_description, status
    ) VALUES (
        p_patient_id, p_provider_id, p_appointment_id,
        NVL(p_encounter_type, 'OUTPATIENT'), p_chief_complaint, p_clinical_notes,
        p_diagnosis_code, p_diagnosis_description, 'COMPLETED'
    ) RETURNING encounter_id INTO p_encounter_id_out;

    -- If linked to an appointment, mark appointment as COMPLETED
    IF p_appointment_id IS NOT NULL THEN
        UPDATE APPOINTMENTS
        SET status = 'COMPLETED', updated_at = CURRENT_TIMESTAMP
        WHERE appointment_id = p_appointment_id;
    END IF;

    -- Generate billing invoice if amount specified
    IF p_billing_amount IS NOT NULL AND p_billing_amount > 0 THEN
        v_bill_num := 'INV-' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || '-' || LPAD(p_encounter_id_out, 5, '0');
        
        INSERT INTO BILLING_RECORDS (
            bill_number, patient_id, encounter_id,
            billing_date, due_date, total_amount,
            paid_amount, balance_due, status
        ) VALUES (
            v_bill_num, p_patient_id, p_encounter_id_out,
            CURRENT_DATE, CURRENT_DATE + 30, p_billing_amount,
            0.00, p_billing_amount, 'PENDING'
        ) RETURNING bill_id INTO p_bill_id_out;
    ELSE
        p_bill_id_out := NULL;
    END IF;

    p_status_out := 'SUCCESS';
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status_out := 'ERROR: ' || SQLERRM;
END SP_RECORD_CLINICAL_ENCOUNTER;
/

-- ----------------------------------------------------------------------------
-- 3. Procedure: SP_PROCESS_BILLING_PAYMENT
-- Applies a payment to a billing record and updates the status accurately.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PROCESS_BILLING_PAYMENT(
    p_bill_id        IN  NUMBER,
    p_payment_amount IN  NUMBER,
    p_payment_method IN  VARCHAR2,
    p_success_out    OUT NUMBER,
    p_message_out    OUT VARCHAR2,
    p_new_balance    OUT NUMBER
)
IS
    v_total NUMBER(10, 2);
    v_paid NUMBER(10, 2);
    v_balance NUMBER(10, 2);
    v_new_paid NUMBER(10, 2);
    v_new_balance NUMBER(10, 2);
    v_new_status VARCHAR2(20);
BEGIN
    p_success_out := 0;

    IF p_payment_amount <= 0 THEN
        p_message_out := 'Payment amount must be greater than zero.';
        RETURN;
    END IF;

    -- Fetch current invoice
    BEGIN
        SELECT total_amount, paid_amount, balance_due
        INTO v_total, v_paid, v_balance
        FROM BILLING_RECORDS
        WHERE bill_id = p_bill_id
        FOR UPDATE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_message_out := 'Invoice ID ' || p_bill_id || ' does not exist.';
            RETURN;
    END;

    IF v_balance <= 0 THEN
        p_message_out := 'Invoice has already been settled in full.';
        RETURN;
    END IF;

    IF p_payment_amount > v_balance THEN
        p_message_out := 'Payment amount (' || p_payment_amount || ') exceeds remaining balance (' || v_balance || ').';
        RETURN;
    END IF;

    v_new_paid := v_paid + p_payment_amount;
    v_new_balance := v_balance - p_payment_amount;

    IF v_new_balance = 0 THEN
        v_new_status := 'PAID';
    ELSE
        v_new_status := 'PARTIALLY_PAID';
    END IF;

    UPDATE BILLING_RECORDS
    SET paid_amount = v_new_paid,
        balance_due = v_new_balance,
        status = v_new_status,
        payment_method = NVL(p_payment_method, payment_method),
        updated_at = CURRENT_TIMESTAMP
    WHERE bill_id = p_bill_id;

    p_success_out := 1;
    p_message_out := 'Payment processed successfully.';
    p_new_balance := v_new_balance;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_success_out := 0;
        p_message_out := 'Payment failed: ' || SQLERRM;
END SP_PROCESS_BILLING_PAYMENT;
/
