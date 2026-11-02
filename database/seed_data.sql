-- ============================================================================
-- Healthcare Data Management and Analytics System
-- Synthetic Seed Data Script
-- NOTE: All data is fictional and synthetically generated for educational testing.
-- ============================================================================

-- Clean existing data
DELETE FROM BILLING_RECORDS;
DELETE FROM ENCOUNTERS;
DELETE FROM APPOINTMENTS;
DELETE FROM PATIENTS;
DELETE FROM PROVIDERS;

-- ----------------------------------------------------------------------------
-- 1. Insert Providers
-- ----------------------------------------------------------------------------
INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('Sarah', 'Jenkins', 'Cardiology', 'MD-CARD-101', 'sjenkins@hospital.org', '555-0101', 'Cardiovascular');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('Michael', 'Chang', 'Pediatrics', 'MD-PED-202', 'mchang@hospital.org', '555-0102', 'Pediatric Medicine');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('Elena', 'Rostova', 'General Medicine', 'MD-GEN-303', 'erostova@hospital.org', '555-0103', 'Internal Medicine');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('David', 'O''Connor', 'Orthopedics', 'MD-ORTH-404', 'doconnor@hospital.org', '555-0104', 'Orthopedic Surgery');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('Amina', 'Diallo', 'Neurology', 'MD-NEUR-505', 'adiallo@hospital.org', '555-0105', 'Neurosciences');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('Robert', 'Gupta', 'Dermatology', 'MD-DERM-606', 'rgupta@hospital.org', '555-0106', 'Dermatology');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('Rachel', 'Alvarez', 'Oncology', 'MD-ONC-707', 'ralvarez@hospital.org', '555-0107', 'Cancer Center');

INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
VALUES ('James', 'Wilson', 'Obstetrics & Gynecology', 'MD-OBGYN-808', 'jwilson@hospital.org', '555-0108', 'Women''s Health');

-- ----------------------------------------------------------------------------
-- 2. Insert Patients (25 Synthetic Records)
-- ----------------------------------------------------------------------------
INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10001', 'John', 'Doe', DATE '1985-04-12', 'Male', 'O+', 'john.doe@fakeemail.com', '555-1001', '124 Maple St, Springfield', 'Jane Doe', '555-9001', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10002', 'Alice', 'Smith', DATE '1990-08-25', 'Female', 'A+', 'alice.smith@fakeemail.com', '555-1002', '456 Oak Ave, Springfield', 'Bob Smith', '555-9002', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10003', 'Carlos', 'Mendoza', DATE '1978-11-03', 'Male', 'B+', 'carlos.m@fakeemail.com', '555-1003', '789 Pine Rd, Springfield', 'Maria Mendoza', '555-9003', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10004', 'Emily', 'Johnson', DATE '2001-02-14', 'Female', 'AB+', 'emily.j@fakeemail.com', '555-1004', '321 Elm St, Springfield', 'David Johnson', '555-9004', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10005', 'Liam', 'Brown', DATE '1965-06-30', 'Male', 'O-', 'liam.b@fakeemail.com', '555-1005', '654 Birch Blvd, Springfield', 'Sarah Brown', '555-9005', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10006', 'Sophia', 'Taylor', DATE '1995-12-08', 'Female', 'A-', 'sophia.t@fakeemail.com', '555-1006', '987 Cedar Ct, Springfield', 'Emma Taylor', '555-9006', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10007', 'Mason', 'Anderson', DATE '1982-03-21', 'Male', 'B-', 'mason.a@fakeemail.com', '555-1007', '159 Walnut Dr, Springfield', 'Laura Anderson', '555-9007', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10008', 'Olivia', 'Thomas', DATE '1992-09-17', 'Female', 'O+', 'olivia.t@fakeemail.com', '555-1008', '753 Willow Way, Springfield', 'Lucas Thomas', '555-9008', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10009', 'Noah', 'Jackson', DATE '2010-05-19', 'Male', 'A+', 'noah.j@fakeemail.com', '555-1009', '852 Spruce Pl, Springfield', 'Karen Jackson', '555-9009', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10010', 'Ava', 'White', DATE '1988-07-04', 'Female', 'AB-', 'ava.white@fakeemail.com', '555-1010', '951 Ash Ln, Springfield', 'Henry White', '555-9010', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10011', 'William', 'Harris', DATE '1972-10-11', 'Male', 'O+', 'william.h@fakeemail.com', '555-1011', '357 Hickory St, Springfield', 'Grace Harris', '555-9011', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10012', 'Isabella', 'Martin', DATE '1984-01-29', 'Female', 'A+', 'isabella.m@fakeemail.com', '555-1012', '258 Sycamore Ct, Springfield', 'Ethan Martin', '555-9012', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10013', 'James', 'Thompson', DATE '1960-08-15', 'Male', 'B+', 'james.t@fakeemail.com', '555-1013', '147 Chestnut Blvd, Springfield', 'Mary Thompson', '555-9013', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10014', 'Mia', 'Garcia', DATE '2003-11-22', 'Female', 'O-', 'mia.garcia@fakeemail.com', '555-1014', '369 Beech Rd, Springfield', 'Jose Garcia', '555-9014', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10015', 'Benjamin', 'Martinez', DATE '1975-03-09', 'Male', 'A-', 'ben.m@fakeemail.com', '555-1015', '741 Poplar Ave, Springfield', 'Elena Martinez', '555-9015', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10016', 'Charlotte', 'Robinson', DATE '1998-05-31', 'Female', 'AB+', 'charlotte.r@fakeemail.com', '555-1016', '852 Cypress Dr, Springfield', 'Jack Robinson', '555-9016', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10017', 'Lucas', 'Clark', DATE '1989-12-25', 'Male', 'O+', 'lucas.c@fakeemail.com', '555-1017', '963 Magnolia St, Springfield', 'Zoe Clark', '555-9017', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10018', 'Amelia', 'Rodriguez', DATE '1993-04-18', 'Female', 'B-', 'amelia.r@fakeemail.com', '555-1018', '159 Redwood Ct, Springfield', 'Mateo Rodriguez', '555-9018', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10019', 'Henry', 'Lewis', DATE '1968-09-02', 'Male', 'A+', 'henry.l@fakeemail.com', '555-1019', '357 Alder Way, Springfield', 'Chloe Lewis', '555-9019', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10020', 'Harper', 'Lee', DATE '2005-06-14', 'Female', 'O+', 'harper.lee@fakeemail.com', '555-1020', '753 Larch Ln, Springfield', 'Harper Sr.', '555-9020', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10021', 'Alexander', 'Walker', DATE '1981-02-28', 'Male', 'B+', 'alex.w@fakeemail.com', '555-1021', '951 Hemlock Pl, Springfield', 'Lily Walker', '555-9021', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10022', 'Evelyn', 'Hall', DATE '1996-10-07', 'Female', 'A-', 'evelyn.h@fakeemail.com', '555-1022', '258 Fir St, Springfield', 'Noah Hall', '555-9022', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10023', 'Daniel', 'Allen', DATE '1970-07-19', 'Male', 'O-', 'daniel.a@fakeemail.com', '555-1023', '147 Locust Ave, Springfield', 'Ruth Allen', '555-9023', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10024', 'Ella', 'Young', DATE '1991-03-15', 'Female', 'AB+', 'ella.y@fakeemail.com', '555-1024', '369 Linden Rd, Springfield', 'Owen Young', '555-9024', 1);

INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone, is_active)
VALUES ('MRN-10025', 'Matthew', 'King', DATE '1987-12-01', 'Male', 'B+', 'matthew.k@fakeemail.com', '555-1025', '741 Palm Blvd, Springfield', 'Hannah King', '555-9025', 1);

-- ----------------------------------------------------------------------------
-- 3. Insert Appointments
-- ----------------------------------------------------------------------------
INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (1, 1, DATE '2026-01-10', '09:00', TIMESTAMP '2026-01-10 09:00:00', 30, 'Chest palpitations and dizziness', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (2, 3, DATE '2026-01-12', '10:00', TIMESTAMP '2026-01-12 10:00:00', 30, 'Annual physical checkup', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (3, 4, DATE '2026-01-15', '14:00', TIMESTAMP '2026-01-15 14:00:00', 45, 'Right knee pain after sports', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status, cancellation_reason, cancelled_at)
VALUES (4, 6, DATE '2026-01-18', '11:00', TIMESTAMP '2026-01-18 11:00:00', 30, 'Skin rash evaluation', 'CANCELLED', 'Patient had personal emergency', TIMESTAMP '2026-01-17 15:30:00');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (5, 5, DATE '2026-01-20', '09:30', TIMESTAMP '2026-01-20 09:30:00', 45, 'Chronic migraine and photophobia', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (6, 3, DATE '2026-01-22', '11:30', TIMESTAMP '2026-01-22 11:30:00', 30, 'Persistent cough and fatigue', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (7, 1, DATE '2026-01-25', '13:00', TIMESTAMP '2026-01-25 13:00:00', 30, 'Hypertension follow-up', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (8, 8, DATE '2026-02-02', '10:00', TIMESTAMP '2026-02-02 10:00:00', 30, 'Prenatal routine consultation', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (9, 2, DATE '2026-02-05', '15:00', TIMESTAMP '2026-02-05 15:00:00', 30, 'Childhood immunization review', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status, cancellation_reason, cancelled_at)
VALUES (10, 4, DATE '2026-02-08', '09:00', TIMESTAMP '2026-02-08 09:00:00', 30, 'Shoulder stiffness and pain', 'CANCELLED', 'Provider schedule conflict', TIMESTAMP '2026-02-07 08:00:00');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (11, 7, DATE '2026-02-10', '14:30', TIMESTAMP '2026-02-10 14:30:00', 60, 'Oncology follow-up consultation', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (12, 3, DATE '2026-02-12', '08:30', TIMESTAMP '2026-02-12 08:30:00', 30, 'Elevated fasting glucose levels', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (13, 1, DATE '2026-02-16', '11:00', TIMESTAMP '2026-02-16 11:00:00', 30, 'Shortness of breath on exertion', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (14, 6, DATE '2026-02-20', '16:00', TIMESTAMP '2026-02-20 16:00:00', 30, 'Acne vulgaris consultation', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (15, 4, DATE '2026-02-23', '10:30', TIMESTAMP '2026-02-23 10:30:00', 45, 'Lumbar spine pain radiating to hip', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (16, 5, DATE '2026-03-01', '10:00', TIMESTAMP '2026-03-01 10:00:00', 30, 'Peripheral neuropathy assessment', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (17, 3, DATE '2026-03-04', '13:30', TIMESTAMP '2026-03-04 13:30:00', 30, 'Acid reflux and indigestion', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status, cancellation_reason, cancelled_at)
VALUES (18, 1, DATE '2026-03-08', '09:00', TIMESTAMP '2026-03-08 09:00:00', 30, 'Routine ECG review', 'CANCELLED', 'Transportation issues', TIMESTAMP '2026-03-07 18:00:00');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (19, 8, DATE '2026-03-10', '15:00', TIMESTAMP '2026-03-10 15:00:00', 30, 'Routine gynecological screening', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (20, 2, DATE '2026-03-15', '09:30', TIMESTAMP '2026-03-15 09:30:00', 30, 'Pediatric asthma check', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (21, 6, DATE '2026-03-20', '14:00', TIMESTAMP '2026-03-20 14:00:00', 30, 'Eczema flare-up', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (22, 4, DATE '2026-03-25', '11:00', TIMESTAMP '2026-03-25 11:00:00', 45, 'Wrist tendonitis following strain', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (23, 7, DATE '2026-04-02', '10:00', TIMESTAMP '2026-04-02 10:00:00', 60, 'Post-chemotherapy assessment', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (24, 3, DATE '2026-04-05', '09:00', TIMESTAMP '2026-04-05 09:00:00', 30, 'Seasonal allergy symptoms', 'COMPLETED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (25, 1, DATE '2026-04-10', '15:30', TIMESTAMP '2026-04-10 15:30:00', 30, 'Arrhythmia monitor setup', 'COMPLETED');

-- Upcoming & active appointments
INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (1, 1, DATE '2026-11-15', '09:00', TIMESTAMP '2026-11-15 09:00:00', 30, 'Semi-annual cardiac review', 'SCHEDULED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (2, 3, DATE '2026-11-16', '10:30', TIMESTAMP '2026-11-16 10:30:00', 30, 'Blood pressure monitoring', 'CONFIRMED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (3, 4, DATE '2026-11-17', '14:00', TIMESTAMP '2026-11-17 14:00:00', 45, 'Orthopedic rehabilitation progress check', 'SCHEDULED');

INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status)
VALUES (4, 6, DATE '2026-11-18', '11:00', TIMESTAMP '2026-11-18 11:00:00', 30, 'Mole mapping and screening', 'CONFIRMED');

-- ----------------------------------------------------------------------------
-- 4. Insert Encounters
-- ----------------------------------------------------------------------------
INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (1, 1, 1, 'OUTPATIENT', TIMESTAMP '2026-01-10 09:30:00', 'Chest palpitations and dizziness', 'ECG indicates occasional benign PVCs. Prescribed low-dose beta-blocker.', 'I49.3', 'Ventricular premature depolarization', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (2, 2, 3, 'OUTPATIENT', TIMESTAMP '2026-01-12 10:30:00', 'Annual physical checkup', 'Vitals normal, BMI 22.4. Ordered standard lipid panel and metabolic profile.', 'Z00.00', 'General adult medical examination without abnormal findings', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (3, 3, 4, 'OUTPATIENT', TIMESTAMP '2026-01-15 14:45:00', 'Right knee pain after sports', 'Physical exam shows mild medial joint line tenderness. Recommended physical therapy and ice.', 'M25.561', 'Pain in right knee', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (5, 5, 5, 'OUTPATIENT', TIMESTAMP '2026-01-20 10:15:00', 'Chronic migraine and photophobia', 'Patient reports weekly migraines with aura. Prescribed triptan abortive therapy.', 'G43.109', 'Migraine with aura, not intractable', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (6, 6, 3, 'OUTPATIENT', TIMESTAMP '2026-01-22 12:00:00', 'Persistent cough and fatigue', 'Lungs clear bilaterally, symptoms consistent with viral bronchitis. Supportive care advised.', 'J20.9', 'Acute bronchitis, unspecified', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (7, 7, 1, 'OUTPATIENT', TIMESTAMP '2026-01-25 13:30:00', 'Hypertension follow-up', 'Blood pressure 142/88 mmHg. Titrated lisinopril to 20mg daily.', 'I10', 'Essential (primary) hypertension', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (8, 8, 8, 'OUTPATIENT', TIMESTAMP '2026-02-02 10:30:00', 'Prenatal routine consultation', 'Gestational age 18 weeks. Fetal heart rate 145 bpm. Anatomy ultrasound scheduled.', 'Z34.82', 'Encounter for supervision of normal pregnancy, second trimester', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (9, 9, 2, 'OUTPATIENT', TIMESTAMP '2026-02-05 15:30:00', 'Childhood immunization review', 'Administered MMR and DTaP boosters. Child tolerated well.', 'Z23', 'Encounter for immunization', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (11, 11, 7, 'OUTPATIENT', TIMESTAMP '2026-02-10 15:30:00', 'Oncology follow-up consultation', 'CBC within acceptable parameters. Remission status maintained.', 'Z85.3', 'Personal history of malignant neoplasm of breast', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (12, 12, 3, 'OUTPATIENT', TIMESTAMP '2026-02-12 09:00:00', 'Elevated fasting glucose levels', 'HbA1c measured at 7.2%. Initiated Metformin 500mg BID and dietary counseling.', 'E11.9', 'Type 2 diabetes mellitus without complications', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (13, 13, 1, 'OUTPATIENT', TIMESTAMP '2026-02-16 11:30:00', 'Shortness of breath on exertion', 'Echocardiogram ordered. Mild peripheral edema noted. Started furosemide.', 'I50.9', 'Heart failure, unspecified', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (14, 14, 6, 'OUTPATIENT', TIMESTAMP '2026-02-20 16:30:00', 'Acne vulgaris consultation', 'Moderate comedonal and inflammatory acne on face. Prescribed topical retinoid and benzoyl peroxide.', 'L70.0', 'Acne vulgaris', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (15, 15, 4, 'OUTPATIENT', TIMESTAMP '2026-02-23 11:15:00', 'Lumbar spine pain radiating to hip', 'Straight leg raise negative. Paravertebral muscle spasms. Prescribed cyclobenzaprine.', 'M54.5', 'Low back pain, unspecified', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (16, 16, 5, 'OUTPATIENT', TIMESTAMP '2026-03-01 10:30:00', 'Peripheral neuropathy assessment', 'Decreased pinprick sensation in bilateral lower extremities. Started gabapentin titration.', 'G62.9', 'Polyneuropathy, unspecified', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (17, 17, 3, 'OUTPATIENT', TIMESTAMP '2026-03-04 14:00:00', 'Acid reflux and indigestion', 'Symptoms prominent after meals. Initiated omeprazole 20mg daily for 8 weeks.', 'K21.9', 'Gastro-esophageal reflux disease without esophagitis', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (19, 19, 8, 'OUTPATIENT', TIMESTAMP '2026-03-10 15:30:00', 'Routine gynecological screening', 'Cervical cytology collected. Pelvic exam normal.', 'Z01.419', 'Encounter for gynecological exam without abnormal findings', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (20, 20, 2, 'OUTPATIENT', TIMESTAMP '2026-03-15 10:00:00', 'Pediatric asthma check', 'Lungs clear, peak flow 85% of predicted. Refilled albuterol inhaler.', 'J45.909', 'Unspecified asthma, uncomplicated', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (21, 21, 6, 'OUTPATIENT', TIMESTAMP '2026-03-20 14:30:00', 'Eczema flare-up', 'Erythematous pruritic patches on antecubital fossae. Prescribed hydrocortisone 2.5%.', 'L20.9', 'Atopic dermatitis, unspecified', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (22, 22, 4, 'OUTPATIENT', TIMESTAMP '2026-03-25 11:45:00', 'Wrist tendonitis following strain', 'Finkelstein test negative. Tenderness over wrist extensors. Splint prescribed.', 'M77.9', 'Enthesopathy, unspecified', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (23, 23, 7, 'OUTPATIENT', TIMESTAMP '2026-04-02 11:00:00', 'Post-chemotherapy assessment', 'Fatigue improving. Restaging scans show no evidence of progression.', 'Z51.11', 'Encounter for antineoplastic chemotherapy', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (24, 24, 3, 'OUTPATIENT', TIMESTAMP '2026-04-05 09:30:00', 'Seasonal allergy symptoms', 'Allergic rhinitis with clear rhinorrhea and itchy eyes. Prescribed cetirizine.', 'J30.1', 'Allergic rhinitis due to pollen', 'COMPLETED');

INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
VALUES (25, 25, 1, 'OUTPATIENT', TIMESTAMP '2026-04-10 16:00:00', 'Arrhythmia monitor setup', 'Holter monitor placed for 48-hour continuous ambulatory recording.', 'Z45.018', 'Encounter for adjustment and management of other cardiac device', 'COMPLETED');

-- ----------------------------------------------------------------------------
-- 5. Insert Billing Records
-- ----------------------------------------------------------------------------
INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260110-00001', 1, 1, DATE '2026-01-10', DATE '2026-02-10', 250.00, 250.00, 0.00, 'PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260112-00002', 2, 2, DATE '2026-01-12', DATE '2026-02-12', 150.00, 150.00, 0.00, 'PAID', 'CREDIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260115-00003', 3, 3, DATE '2026-01-15', DATE '2026-02-15', 320.00, 320.00, 0.00, 'PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260120-00004', 5, 4, DATE '2026-01-20', DATE '2026-02-20', 400.00, 200.00, 200.00, 'PARTIALLY_PAID', 'CREDIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260122-00005', 6, 5, DATE '2026-01-22', DATE '2026-02-22', 120.00, 120.00, 0.00, 'PAID', 'CASH');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260125-00006', 7, 6, DATE '2026-01-25', DATE '2026-02-25', 180.00, 180.00, 0.00, 'PAID', 'DEBIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260202-00007', 8, 7, DATE '2026-02-02', DATE '2026-03-02', 220.00, 220.00, 0.00, 'PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260205-00008', 9, 8, DATE '2026-02-05', DATE '2026-03-05', 95.00, 95.00, 0.00, 'PAID', 'CREDIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260210-00009', 11, 9, DATE '2026-02-10', DATE '2026-03-10', 850.00, 500.00, 350.00, 'PARTIALLY_PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260212-00010', 12, 10, DATE '2026-02-12', DATE '2026-03-12', 175.00, 0.00, 175.00, 'OVERDUE', NULL);

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260216-00011', 13, 11, DATE '2026-02-16', DATE '2026-03-16', 450.00, 0.00, 450.00, 'OVERDUE', NULL);

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260220-00012', 14, 12, DATE '2026-02-20', DATE '2026-03-20', 130.00, 130.00, 0.00, 'PAID', 'CREDIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260223-00013', 15, 13, DATE '2026-02-23', DATE '2026-03-23', 280.00, 100.00, 180.00, 'OVERDUE', 'CASH');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260301-00014', 16, 14, DATE '2026-03-01', DATE '2026-04-01', 310.00, 310.00, 0.00, 'PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260304-00015', 17, 15, DATE '2026-03-04', DATE '2026-04-04', 160.00, 160.00, 0.00, 'PAID', 'CREDIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260310-00016', 19, 16, DATE '2026-03-10', DATE '2026-04-10', 210.00, 210.00, 0.00, 'PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260315-00017', 20, 17, DATE '2026-03-15', DATE '2026-04-15', 110.00, 110.00, 0.00, 'PAID', 'CASH');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260320-00018', 21, 18, DATE '2026-03-20', DATE '2026-04-20', 140.00, 0.00, 140.00, 'PENDING', NULL);

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260325-00019', 22, 19, DATE '2026-03-25', DATE '2026-04-25', 290.00, 290.00, 0.00, 'PAID', 'DEBIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260402-00020', 23, 20, DATE '2026-04-02', DATE '2026-05-02', 920.00, 500.00, 420.00, 'PARTIALLY_PAID', 'INSURANCE');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260405-00021', 24, 21, DATE '2026-04-05', DATE '2026-05-05', 115.00, 115.00, 0.00, 'PAID', 'CREDIT_CARD');

INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
VALUES ('INV-20260410-00022', 25, 22, DATE '2026-04-10', DATE '2026-05-10', 380.00, 0.00, 380.00, 'PENDING', NULL);

COMMIT;
