"""
Synthetic Seed Data Seeder Script
Populates the database with realistic synthetic providers, patients, appointments,
clinical encounters, and billing records for development, testing, and Tableau analytics.
"""

import sys
from pathlib import Path

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.repositories.db import db
from app.utils.logger import logger

PROVIDERS_DATA = [
    ("Sarah", "Jenkins", "Cardiology", "MD-CARD-101", "sjenkins@hospital.org", "555-0101", "Cardiovascular"),
    ("Michael", "Chang", "Pediatrics", "MD-PED-202", "mchang@hospital.org", "555-0102", "Pediatric Medicine"),
    ("Elena", "Rostova", "General Medicine", "MD-GEN-303", "erostova@hospital.org", "555-0103", "Internal Medicine"),
    ("David", "O'Connor", "Orthopedics", "MD-ORTH-404", "doconnor@hospital.org", "555-0104", "Orthopedic Surgery"),
    ("Amina", "Diallo", "Neurology", "MD-NEUR-505", "adiallo@hospital.org", "555-0105", "Neurosciences"),
    ("Robert", "Gupta", "Dermatology", "MD-DERM-606", "rgupta@hospital.org", "555-0106", "Dermatology"),
    ("Rachel", "Alvarez", "Oncology", "MD-ONC-707", "ralvarez@hospital.org", "555-0107", "Cancer Center"),
    ("James", "Wilson", "Obstetrics & Gynecology", "MD-OBGYN-808", "jwilson@hospital.org", "555-0108", "Women's Health"),
]

PATIENTS_DATA = [
    ("MRN-10001", "John", "Doe", "1985-04-12", "Male", "O+", "john.doe@fakeemail.com", "555-1001", "124 Maple St, Springfield", "Jane Doe", "555-9001"),
    ("MRN-10002", "Alice", "Smith", "1990-08-25", "Female", "A+", "alice.smith@fakeemail.com", "555-1002", "456 Oak Ave, Springfield", "Bob Smith", "555-9002"),
    ("MRN-10003", "Carlos", "Mendoza", "1978-11-03", "Male", "B+", "carlos.m@fakeemail.com", "555-1003", "789 Pine Rd, Springfield", "Maria Mendoza", "555-9003"),
    ("MRN-10004", "Emily", "Johnson", "2001-02-14", "Female", "AB+", "emily.j@fakeemail.com", "555-1004", "321 Elm St, Springfield", "David Johnson", "555-9004"),
    ("MRN-10005", "Liam", "Brown", "1965-06-30", "Male", "O-", "liam.b@fakeemail.com", "555-1005", "654 Birch Blvd, Springfield", "Sarah Brown", "555-9005"),
    ("MRN-10006", "Sophia", "Taylor", "1995-12-08", "Female", "A-", "sophia.t@fakeemail.com", "555-1006", "987 Cedar Ct, Springfield", "Emma Taylor", "555-9006"),
    ("MRN-10007", "Mason", "Anderson", "1982-03-21", "Male", "B-", "mason.a@fakeemail.com", "555-1007", "159 Walnut Dr, Springfield", "Laura Anderson", "555-9007"),
    ("MRN-10008", "Olivia", "Thomas", "1992-09-17", "Female", "O+", "olivia.t@fakeemail.com", "555-1008", "753 Willow Way, Springfield", "Lucas Thomas", "555-9008"),
    ("MRN-10009", "Noah", "Jackson", "2010-05-19", "Male", "A+", "noah.j@fakeemail.com", "555-1009", "852 Spruce Pl, Springfield", "Karen Jackson", "555-9009"),
    ("MRN-10010", "Ava", "White", "1988-07-04", "Female", "AB-", "ava.white@fakeemail.com", "555-1010", "951 Ash Ln, Springfield", "Henry White", "555-9010"),
    ("MRN-10011", "William", "Harris", "1972-10-11", "Male", "O+", "william.h@fakeemail.com", "555-1011", "357 Hickory St, Springfield", "Grace Harris", "555-9011"),
    ("MRN-10012", "Isabella", "Martin", "1984-01-29", "Female", "A+", "isabella.m@fakeemail.com", "555-1012", "258 Sycamore Ct, Springfield", "Ethan Martin", "555-9012"),
    ("MRN-10013", "James", "Thompson", "1960-08-15", "Male", "B+", "james.t@fakeemail.com", "555-1013", "147 Chestnut Blvd, Springfield", "Mary Thompson", "555-9013"),
    ("MRN-10014", "Mia", "Garcia", "2003-11-22", "Female", "O-", "mia.garcia@fakeemail.com", "555-1014", "369 Beech Rd, Springfield", "Jose Garcia", "555-9014"),
    ("MRN-10015", "Benjamin", "Martinez", "1975-03-09", "Male", "A-", "ben.m@fakeemail.com", "555-1015", "741 Poplar Ave, Springfield", "Elena Martinez", "555-9015"),
    ("MRN-10016", "Charlotte", "Robinson", "1998-05-31", "Female", "AB+", "charlotte.r@fakeemail.com", "555-1016", "852 Cypress Dr, Springfield", "Jack Robinson", "555-9016"),
    ("MRN-10017", "Lucas", "Clark", "1989-12-25", "Male", "O+", "lucas.c@fakeemail.com", "555-1017", "963 Magnolia St, Springfield", "Zoe Clark", "555-9017"),
    ("MRN-10018", "Amelia", "Rodriguez", "1993-04-18", "Female", "B-", "amelia.r@fakeemail.com", "555-1018", "159 Redwood Ct, Springfield", "Mateo Rodriguez", "555-9018"),
    ("MRN-10019", "Henry", "Lewis", "1968-09-02", "Male", "A+", "henry.l@fakeemail.com", "555-1019", "357 Alder Way, Springfield", "Chloe Lewis", "555-9019"),
    ("MRN-10020", "Harper", "Lee", "2005-06-14", "Female", "O+", "harper.lee@fakeemail.com", "555-1020", "753 Larch Ln, Springfield", "Harper Sr.", "555-9020"),
    ("MRN-10021", "Alexander", "Walker", "1981-02-28", "Male", "B+", "alex.w@fakeemail.com", "555-1021", "951 Hemlock Pl, Springfield", "Lily Walker", "555-9021"),
    ("MRN-10022", "Evelyn", "Hall", "1996-10-07", "Female", "A-", "evelyn.h@fakeemail.com", "555-1022", "258 Fir St, Springfield", "Noah Hall", "555-9022"),
    ("MRN-10023", "Daniel", "Allen", "1970-07-19", "Male", "O-", "daniel.a@fakeemail.com", "555-1023", "147 Locust Ave, Springfield", "Ruth Allen", "555-9023"),
    ("MRN-10024", "Ella", "Young", "1991-03-15", "Female", "AB+", "ella.y@fakeemail.com", "555-1024", "369 Linden Rd, Springfield", "Owen Young", "555-9024"),
    ("MRN-10025", "Matthew", "King", "1987-12-01", "Male", "B+", "matthew.k@fakeemail.com", "555-1025", "741 Palm Blvd, Springfield", "Hannah King", "555-9025"),
]

APPOINTMENTS_DATA = [
    (1, 1, "2026-01-10", "09:00", "2026-01-10 09:00:00", 30, "Chest palpitations and dizziness", "COMPLETED", None, None),
    (2, 3, "2026-01-12", "10:00", "2026-01-12 10:00:00", 30, "Annual physical checkup", "COMPLETED", None, None),
    (3, 4, "2026-01-15", "14:00", "2026-01-15 14:00:00", 45, "Right knee pain after sports", "COMPLETED", None, None),
    (4, 6, "2026-01-18", "11:00", "2026-01-18 11:00:00", 30, "Skin rash evaluation", "CANCELLED", "Patient had personal emergency", "2026-01-17 15:30:00"),
    (5, 5, "2026-01-20", "09:30", "2026-01-20 09:30:00", 45, "Chronic migraine and photophobia", "COMPLETED", None, None),
    (6, 3, "2026-01-22", "11:30", "2026-01-22 11:30:00", 30, "Persistent cough and fatigue", "COMPLETED", None, None),
    (7, 1, "2026-01-25", "13:00", "2026-01-25 13:00:00", 30, "Hypertension follow-up", "COMPLETED", None, None),
    (8, 8, "2026-02-02", "10:00", "2026-02-02 10:00:00", 30, "Prenatal routine consultation", "COMPLETED", None, None),
    (9, 2, "2026-02-05", "15:00", "2026-02-05 15:00:00", 30, "Childhood immunization review", "COMPLETED", None, None),
    (10, 4, "2026-02-08", "09:00", "2026-02-08 09:00:00", 30, "Shoulder stiffness and pain", "CANCELLED", "Provider schedule conflict", "2026-02-07 08:00:00"),
    (11, 7, "2026-02-10", "14:30", "2026-02-10 14:30:00", 60, "Oncology follow-up consultation", "COMPLETED", None, None),
    (12, 3, "2026-02-12", "08:30", "2026-02-12 08:30:00", 30, "Elevated fasting glucose levels", "COMPLETED", None, None),
    (13, 1, "2026-02-16", "11:00", "2026-02-16 11:00:00", 30, "Shortness of breath on exertion", "COMPLETED", None, None),
    (14, 6, "2026-02-20", "16:00", "2026-02-20 16:00:00", 30, "Acne vulgaris consultation", "COMPLETED", None, None),
    (15, 4, "2026-02-23", "10:30", "2026-02-23 10:30:00", 45, "Lumbar spine pain radiating to hip", "COMPLETED", None, None),
    (16, 5, "2026-03-01", "10:00", "2026-03-01 10:00:00", 30, "Peripheral neuropathy assessment", "COMPLETED", None, None),
    (17, 3, "2026-03-04", "13:30", "2026-03-04 13:30:00", 30, "Acid reflux and indigestion", "COMPLETED", None, None),
    (18, 1, "2026-03-08", "09:00", "2026-03-08 09:00:00", 30, "Routine ECG review", "CANCELLED", "Transportation issues", "2026-03-07 18:00:00"),
    (19, 8, "2026-03-10", "15:00", "2026-03-10 15:00:00", 30, "Routine gynecological screening", "COMPLETED", None, None),
    (20, 2, "2026-03-15", "09:30", "2026-03-15 09:30:00", 30, "Pediatric asthma check", "COMPLETED", None, None),
    (21, 6, "2026-03-20", "14:00", "2026-03-20 14:00:00", 30, "Eczema flare-up", "COMPLETED", None, None),
    (22, 4, "2026-03-25", "11:00", "2026-03-25 11:00:00", 45, "Wrist tendonitis following strain", "COMPLETED", None, None),
    (23, 7, "2026-04-02", "10:00", "2026-04-02 10:00:00", 60, "Post-chemotherapy assessment", "COMPLETED", None, None),
    (24, 3, "2026-04-05", "09:00", "2026-04-05 09:00:00", 30, "Seasonal allergy symptoms", "COMPLETED", None, None),
    (25, 1, "2026-04-10", "15:30", "2026-04-10 15:30:00", 30, "Arrhythmia monitor setup", "COMPLETED", None, None),
    (1, 1, "2026-11-15", "09:00", "2026-11-15 09:00:00", 30, "Semi-annual cardiac review", "SCHEDULED", None, None),
    (2, 3, "2026-11-16", "10:30", "2026-11-16 10:30:00", 30, "Blood pressure monitoring", "CONFIRMED", None, None),
    (3, 4, "2026-11-17", "14:00", "2026-11-17 14:00:00", 45, "Orthopedic progress check", "SCHEDULED", None, None),
    (4, 6, "2026-11-18", "11:00", "2026-11-18 11:00:00", 30, "Mole screening", "CONFIRMED", None, None),
]

ENCOUNTERS_DATA = [
    (1, 1, 1, "OUTPATIENT", "2026-01-10 09:30:00", "Chest palpitations and dizziness", "ECG indicates occasional benign PVCs. Prescribed low-dose beta-blocker.", "I49.3", "Ventricular premature depolarization", "COMPLETED"),
    (2, 2, 3, "OUTPATIENT", "2026-01-12 10:30:00", "Annual physical checkup", "Vitals normal, BMI 22.4. Ordered standard lipid panel and metabolic profile.", "Z00.00", "General adult medical examination without abnormal findings", "COMPLETED"),
    (3, 3, 4, "OUTPATIENT", "2026-01-15 14:45:00", "Right knee pain after sports", "Physical exam shows mild medial joint line tenderness. Recommended PT and ice.", "M25.561", "Pain in right knee", "COMPLETED"),
    (5, 5, 5, "OUTPATIENT", "2026-01-20 10:15:00", "Chronic migraine and photophobia", "Patient reports weekly migraines with aura. Prescribed triptan abortive therapy.", "G43.109", "Migraine with aura, not intractable", "COMPLETED"),
    (6, 6, 3, "OUTPATIENT", "2026-01-22 12:00:00", "Persistent cough and fatigue", "Lungs clear bilaterally, symptoms consistent with viral bronchitis. Supportive care advised.", "J20.9", "Acute bronchitis, unspecified", "COMPLETED"),
    (7, 7, 1, "OUTPATIENT", "2026-01-25 13:30:00", "Hypertension follow-up", "Blood pressure 142/88 mmHg. Titrated lisinopril to 20mg daily.", "I10", "Essential (primary) hypertension", "COMPLETED"),
    (8, 8, 8, "OUTPATIENT", "2026-02-02 10:30:00", "Prenatal routine consultation", "Gestational age 18 weeks. Fetal heart rate 145 bpm. Anatomy ultrasound scheduled.", "Z34.82", "Encounter for supervision of normal pregnancy, second trimester", "COMPLETED"),
    (9, 9, 2, "OUTPATIENT", "2026-02-05 15:30:00", "Childhood immunization review", "Administered MMR and DTaP boosters. Child tolerated well.", "Z23", "Encounter for immunization", "COMPLETED"),
    (11, 11, 7, "OUTPATIENT", "2026-02-10 15:30:00", "Oncology follow-up consultation", "CBC within acceptable parameters. Remission status maintained.", "Z85.3", "Personal history of malignant neoplasm of breast", "COMPLETED"),
    (12, 12, 3, "OUTPATIENT", "2026-02-12 09:00:00", "Elevated fasting glucose levels", "HbA1c measured at 7.2%. Initiated Metformin 500mg BID and dietary counseling.", "E11.9", "Type 2 diabetes mellitus without complications", "COMPLETED"),
    (13, 13, 1, "OUTPATIENT", "2026-02-16 11:30:00", "Shortness of breath on exertion", "Echocardiogram ordered. Mild peripheral edema noted. Started furosemide.", "I50.9", "Heart failure, unspecified", "COMPLETED"),
    (14, 14, 6, "OUTPATIENT", "2026-02-20 16:30:00", "Acne vulgaris consultation", "Moderate comedonal and inflammatory acne on face. Prescribed topical retinoid.", "L70.0", "Acne vulgaris", "COMPLETED"),
    (15, 15, 4, "OUTPATIENT", "2026-02-23 11:15:00", "Lumbar spine pain radiating to hip", "Straight leg raise negative. Paravertebral muscle spasms. Prescribed cyclobenzaprine.", "M54.5", "Low back pain, unspecified", "COMPLETED"),
    (16, 16, 5, "OUTPATIENT", "2026-03-01 10:30:00", "Peripheral neuropathy assessment", "Decreased pinprick sensation in bilateral lower extremities. Started gabapentin titration.", "G62.9", "Polyneuropathy, unspecified", "COMPLETED"),
    (17, 17, 3, "OUTPATIENT", "2026-03-04 14:00:00", "Acid reflux and indigestion", "Symptoms prominent after meals. Initiated omeprazole 20mg daily for 8 weeks.", "K21.9", "Gastro-esophageal reflux disease without esophagitis", "COMPLETED"),
    (19, 19, 8, "OUTPATIENT", "2026-03-10 15:30:00", "Routine gynecological screening", "Cervical cytology collected. Pelvic exam normal.", "Z01.419", "Encounter for gynecological exam without abnormal findings", "COMPLETED"),
    (20, 20, 2, "OUTPATIENT", "2026-03-15 10:00:00", "Pediatric asthma check", "Lungs clear, peak flow 85% of predicted. Refilled albuterol inhaler.", "J45.909", "Unspecified asthma, uncomplicated", "COMPLETED"),
    (21, 21, 6, "OUTPATIENT", "2026-03-20 14:30:00", "Eczema flare-up", "Erythematous pruritic patches on antecubital fossae. Prescribed hydrocortisone 2.5%.", "L20.9", "Atopic dermatitis, unspecified", "COMPLETED"),
    (22, 22, 4, "OUTPATIENT", "2026-03-25 11:45:00", "Wrist tendonitis following strain", "Finkelstein test negative. Tenderness over wrist extensors. Splint prescribed.", "M77.9", "Enthesopathy, unspecified", "COMPLETED"),
    (23, 23, 7, "OUTPATIENT", "2026-04-02 11:00:00", "Post-chemotherapy assessment", "Fatigue improving. Restaging scans show no evidence of progression.", "Z51.11", "Encounter for antineoplastic chemotherapy", "COMPLETED"),
    (24, 24, 3, "OUTPATIENT", "2026-04-05 09:30:00", "Seasonal allergy symptoms", "Allergic rhinitis with clear rhinorrhea and itchy eyes. Prescribed cetirizine.", "J30.1", "Allergic rhinitis due to pollen", "COMPLETED"),
    (25, 25, 1, "OUTPATIENT", "2026-04-10 16:00:00", "Arrhythmia monitor setup", "Holter monitor placed for 48-hour continuous ambulatory recording.", "Z45.018", "Encounter for adjustment and management of other cardiac device", "COMPLETED"),
]

BILLING_DATA = [
    ("INV-20260110-00001", 1, 1, "2026-01-10", "2026-02-10", 250.00, 250.00, 0.00, "PAID", "INSURANCE"),
    ("INV-20260112-00002", 2, 2, "2026-01-12", "2026-02-12", 150.00, 150.00, 0.00, "PAID", "CREDIT_CARD"),
    ("INV-20260115-00003", 3, 3, "2026-01-15", "2026-02-15", 320.00, 320.00, 0.00, "PAID", "INSURANCE"),
    ("INV-20260120-00004", 5, 4, "2026-01-20", "2026-02-20", 400.00, 200.00, 200.00, "PARTIALLY_PAID", "CREDIT_CARD"),
    ("INV-20260122-00005", 6, 5, "2026-01-22", "2026-02-22", 120.00, 120.00, 0.00, "PAID", "CASH"),
    ("INV-20260125-00006", 7, 6, "2026-01-25", "2026-02-25", 180.00, 180.00, 0.00, "PAID", "DEBIT_CARD"),
    ("INV-20260202-00007", 8, 7, "2026-02-02", "2026-03-02", 220.00, 220.00, 0.00, "PAID", "INSURANCE"),
    ("INV-20260205-00008", 9, 8, "2026-02-05", "2026-03-05", 95.00, 95.00, 0.00, "PAID", "CREDIT_CARD"),
    ("INV-20260210-00009", 11, 9, "2026-02-10", "2026-03-10", 850.00, 500.00, 350.00, "PARTIALLY_PAID", "INSURANCE"),
    ("INV-20260212-00010", 12, 10, "2026-02-12", "2026-03-12", 175.00, 0.00, 175.00, "OVERDUE", None),
    ("INV-20260216-00011", 13, 11, "2026-02-16", "2026-03-16", 450.00, 0.00, 450.00, "OVERDUE", None),
    ("INV-20260220-00012", 14, 12, "2026-02-20", "2026-03-20", 130.00, 130.00, 0.00, "PAID", "CREDIT_CARD"),
    ("INV-20260223-00013", 15, 13, "2026-02-23", "2026-03-23", 280.00, 100.00, 180.00, "OVERDUE", "CASH"),
    ("INV-20260301-00014", 16, 14, "2026-03-01", "2026-04-01", 310.00, 310.00, 0.00, "PAID", "INSURANCE"),
    ("INV-20260304-00015", 17, 15, "2026-03-04", "2026-04-04", 160.00, 160.00, 0.00, "PAID", "CREDIT_CARD"),
    ("INV-20260310-00016", 19, 16, "2026-03-10", "2026-04-10", 210.00, 210.00, 0.00, "PAID", "INSURANCE"),
    ("INV-20260315-00017", 20, 17, "2026-03-15", "2026-04-15", 110.00, 110.00, 0.00, "PAID", "CASH"),
    ("INV-20260320-00018", 21, 18, "2026-03-20", "2026-04-20", 140.00, 0.00, 140.00, "PENDING", None),
    ("INV-20260325-00019", 22, 19, "2026-03-25", "2026-04-25", 290.00, 290.00, 0.00, "PAID", "DEBIT_CARD"),
    ("INV-20260402-00020", 23, 20, "2026-04-02", "2026-05-02", 920.00, 500.00, 420.00, "PARTIALLY_PAID", "INSURANCE"),
    ("INV-20260405-00021", 24, 21, "2026-04-05", "2026-05-05", 115.00, 115.00, 0.00, "PAID", "CREDIT_CARD"),
    ("INV-20260410-00022", 25, 22, "2026-04-10", "2026-05-10", 380.00, 0.00, 380.00, "PENDING", None),
]


def seed_database():
    """Populates realistic synthetic data into the database."""
    logger.info("Seeding database with synthetic records...")

    with db.get_connection() as conn:
        cursor = conn.cursor()

        # Clean existing records
        cursor.execute("DELETE FROM BILLING_RECORDS;")
        cursor.execute("DELETE FROM ENCOUNTERS;")
        cursor.execute("DELETE FROM APPOINTMENTS;")
        cursor.execute("DELETE FROM PATIENTS;")
        cursor.execute("DELETE FROM PROVIDERS;")

        # 1. Insert Providers
        prov_sql = """
            INSERT INTO PROVIDERS (first_name, last_name, specialty, license_number, email, phone, department)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        for p in PROVIDERS_DATA:
            cursor.execute(prov_sql, p)

        # 2. Insert Patients
        pat_sql = """
            INSERT INTO PATIENTS (patient_mrn, first_name, last_name, date_of_birth, gender, blood_group, email, phone, address, emergency_contact_name, emergency_contact_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for pt in PATIENTS_DATA:
            cursor.execute(pat_sql, pt)

        # 3. Insert Appointments
        appt_sql = """
            INSERT INTO APPOINTMENTS (patient_id, provider_id, appointment_date, appointment_time, appointment_datetime, duration_minutes, reason_for_visit, status, cancellation_reason, cancelled_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for ap in APPOINTMENTS_DATA:
            cursor.execute(appt_sql, ap)

        # 4. Insert Encounters
        enc_sql = """
            INSERT INTO ENCOUNTERS (appointment_id, patient_id, provider_id, encounter_type, encounter_date, chief_complaint, clinical_notes, diagnosis_code, diagnosis_description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for en in ENCOUNTERS_DATA:
            cursor.execute(enc_sql, en)

        # 5. Insert Billing Records
        bill_sql = """
            INSERT INTO BILLING_RECORDS (bill_number, patient_id, encounter_id, billing_date, due_date, total_amount, paid_amount, balance_due, status, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for bi in BILLING_DATA:
            cursor.execute(bill_sql, bi)

        conn.commit()
        cursor.close()

    logger.info(f"Seeded: {len(PROVIDERS_DATA)} Providers, {len(PATIENTS_DATA)} Patients, {len(APPOINTMENTS_DATA)} Appointments, {len(ENCOUNTERS_DATA)} Encounters, {len(BILLING_DATA)} Billing Records.")


if __name__ == "__main__":
    seed_database()
