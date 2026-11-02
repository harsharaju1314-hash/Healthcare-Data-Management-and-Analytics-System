-- ============================================================================
-- Healthcare Data Management and Analytics System
-- Target Database: Oracle Database Free (23c / 21c)
-- Schema DDL: Tables, Constraints, and Indexes
-- ============================================================================

-- Clean up existing objects if script is re-run
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE BILLING_RECORDS CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ENCOUNTERS CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE APPOINTMENTS CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE PATIENTS CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE PROVIDERS CASCADE CONSTRAINTS PURGE';
EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

-- ----------------------------------------------------------------------------
-- 1. Table: PROVIDERS
-- Healthcare professionals providing clinical consultations and procedures.
-- ----------------------------------------------------------------------------
CREATE TABLE PROVIDERS (
    provider_id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name          VARCHAR2(50) NOT NULL,
    last_name           VARCHAR2(50) NOT NULL,
    specialty           VARCHAR2(100) NOT NULL,
    license_number      VARCHAR2(50) NOT NULL,
    email               VARCHAR2(100) NOT NULL,
    phone               VARCHAR2(20),
    department          VARCHAR2(50) NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_provider_license UNIQUE (license_number),
    CONSTRAINT uq_provider_email UNIQUE (email)
);

-- ----------------------------------------------------------------------------
-- 2. Table: PATIENTS
-- Registered patients receiving healthcare services.
-- ----------------------------------------------------------------------------
CREATE TABLE PATIENTS (
    patient_id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_mrn             VARCHAR2(20) NOT NULL,
    first_name              VARCHAR2(50) NOT NULL,
    last_name               VARCHAR2(50) NOT NULL,
    date_of_birth           DATE NOT NULL,
    gender                  VARCHAR2(10) NOT NULL,
    blood_group             VARCHAR2(5),
    email                   VARCHAR2(100),
    phone                   VARCHAR2(20) NOT NULL,
    address                 VARCHAR2(255),
    emergency_contact_name  VARCHAR2(100),
    emergency_contact_phone VARCHAR2(20),
    is_active               NUMBER(1) DEFAULT 1 NOT NULL,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_patient_mrn UNIQUE (patient_mrn),
    CONSTRAINT uq_patient_email UNIQUE (email),
    CONSTRAINT chk_patient_gender CHECK (gender IN ('Male', 'Female', 'Other', 'Unknown')),
    CONSTRAINT chk_patient_blood_group CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    CONSTRAINT chk_patient_active CHECK (is_active IN (0, 1))
);

-- ----------------------------------------------------------------------------
-- 3. Table: APPOINTMENTS
-- Scheduled consultations between patients and healthcare providers.
-- ----------------------------------------------------------------------------
CREATE TABLE APPOINTMENTS (
    appointment_id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id             NUMBER NOT NULL,
    provider_id            NUMBER NOT NULL,
    appointment_date       DATE NOT NULL,
    appointment_time       VARCHAR2(10) NOT NULL,
    appointment_datetime   TIMESTAMP NOT NULL,
    duration_minutes       NUMBER DEFAULT 30 NOT NULL,
    reason_for_visit       VARCHAR2(255) NOT NULL,
    status                 VARCHAR2(20) DEFAULT 'SCHEDULED' NOT NULL,
    cancellation_reason    VARCHAR2(255),
    cancelled_at           TIMESTAMP,
    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_appts_patient FOREIGN KEY (patient_id) REFERENCES PATIENTS(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_appts_provider FOREIGN KEY (provider_id) REFERENCES PROVIDERS(provider_id),
    CONSTRAINT chk_appts_duration CHECK (duration_minutes > 0),
    CONSTRAINT chk_appts_status CHECK (status IN ('SCHEDULED', 'CONFIRMED', 'COMPLETED', 'CANCELLED', 'NO_SHOW')),
    CONSTRAINT uq_prov_slot UNIQUE (provider_id, appointment_datetime)
);

-- ----------------------------------------------------------------------------
-- 4. Table: ENCOUNTERS
-- Clinical encounters documenting medical observations and diagnoses.
-- ----------------------------------------------------------------------------
CREATE TABLE ENCOUNTERS (
    encounter_id           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    appointment_id         NUMBER,
    patient_id             NUMBER NOT NULL,
    provider_id            NUMBER NOT NULL,
    encounter_type         VARCHAR2(30) DEFAULT 'OUTPATIENT' NOT NULL,
    encounter_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    chief_complaint        VARCHAR2(500) NOT NULL,
    clinical_notes         VARCHAR2(2000) NOT NULL,
    diagnosis_code         VARCHAR2(20) NOT NULL,
    diagnosis_description  VARCHAR2(255) NOT NULL,
    status                 VARCHAR2(20) DEFAULT 'COMPLETED' NOT NULL,
    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_enc_appt FOREIGN KEY (appointment_id) REFERENCES APPOINTMENTS(appointment_id) ON DELETE SET NULL,
    CONSTRAINT fk_enc_patient FOREIGN KEY (patient_id) REFERENCES PATIENTS(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_enc_provider FOREIGN KEY (provider_id) REFERENCES PROVIDERS(provider_id),
    CONSTRAINT chk_enc_type CHECK (encounter_type IN ('OUTPATIENT', 'INPATIENT', 'EMERGENCY', 'TELEHEALTH', 'FOLLOW_UP')),
    CONSTRAINT chk_enc_status CHECK (status IN ('IN_PROGRESS', 'COMPLETED', 'AMENDED', 'CANCELLED'))
);

-- ----------------------------------------------------------------------------
-- 5. Table: BILLING_RECORDS
-- Invoices and payment tracking associated with clinical encounters.
-- ----------------------------------------------------------------------------
CREATE TABLE BILLING_RECORDS (
    bill_id                NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bill_number            VARCHAR2(30) NOT NULL,
    patient_id             NUMBER NOT NULL,
    encounter_id           NUMBER NOT NULL,
    billing_date           DATE DEFAULT CURRENT_DATE NOT NULL,
    due_date               DATE NOT NULL,
    total_amount           NUMBER(10, 2) NOT NULL,
    paid_amount            NUMBER(10, 2) DEFAULT 0.00 NOT NULL,
    balance_due            NUMBER(10, 2) NOT NULL,
    status                 VARCHAR2(20) DEFAULT 'PENDING' NOT NULL,
    payment_method         VARCHAR2(30),
    insurance_claim_id     VARCHAR2(50),
    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_billing_number UNIQUE (bill_number),
    CONSTRAINT fk_bill_patient FOREIGN KEY (patient_id) REFERENCES PATIENTS(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_bill_encounter FOREIGN KEY (encounter_id) REFERENCES ENCOUNTERS(encounter_id) ON DELETE CASCADE,
    CONSTRAINT chk_bill_total_pos CHECK (total_amount >= 0),
    CONSTRAINT chk_bill_paid_pos CHECK (paid_amount >= 0),
    CONSTRAINT chk_bill_bal_pos CHECK (balance_due >= 0),
    CONSTRAINT chk_bill_amounts CHECK (paid_amount <= total_amount AND balance_due = total_amount - paid_amount),
    CONSTRAINT chk_bill_status CHECK (status IN ('PENDING', 'PAID', 'PARTIALLY_PAID', 'CANCELLED', 'OVERDUE')),
    CONSTRAINT chk_bill_pay_method CHECK (payment_method IN ('CASH', 'CREDIT_CARD', 'INSURANCE', 'DEBIT_CARD', 'BANK_TRANSFER', NULL))
);

-- ============================================================================
-- Performance Indexes
-- ============================================================================
CREATE INDEX idx_patients_mrn ON PATIENTS(patient_mrn);
CREATE INDEX idx_patients_name ON PATIENTS(last_name, first_name);
CREATE INDEX idx_appointments_pat ON APPOINTMENTS(patient_id);
CREATE INDEX idx_appointments_prov_dt ON APPOINTMENTS(provider_id, appointment_datetime);
CREATE INDEX idx_appointments_status ON APPOINTMENTS(status);
CREATE INDEX idx_encounters_pat ON ENCOUNTERS(patient_id);
CREATE INDEX idx_encounters_prov ON ENCOUNTERS(provider_id);
CREATE INDEX idx_encounters_date ON ENCOUNTERS(encounter_date);
CREATE INDEX idx_billing_pat ON BILLING_RECORDS(patient_id);
CREATE INDEX idx_billing_enc ON BILLING_RECORDS(encounter_id);
CREATE INDEX idx_billing_status_due ON BILLING_RECORDS(status, due_date);
CREATE INDEX idx_billing_date ON BILLING_RECORDS(billing_date);

COMMIT;
