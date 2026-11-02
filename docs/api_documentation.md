# Healthcare REST API Documentation

## 1. Overview

The **HealthPulse REST API** provides programmatic access to patient management, appointment scheduling, clinical documentation, billing transactions, and operational reports.

- **Base URL**: `http://localhost:5000/api`
- **Content-Type**: `application/json`
- **Data Serialization**: Standard ISO-8601 for dates and timestamps; fixed 2-decimal floats for currency.
- **Security**: Parameterized queries across all database access layers to eliminate SQL injection vulnerabilities.

---

## 2. Standard Response Envelope

### 2.1 Success Response (`200 OK`, `201 Created`)
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_records": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

### 2.2 Error Response (`400`, `404`, `409`, `500`)
```json
{
  "success": false,
  "error": "Descriptive human-readable error message",
  "details": {
    "field_name": "Specific validation failure"
  }
}
```

---

## 3. Endpoints Directory

| Category | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **System** | `GET` | `/api/health` | Health check & active DB engine info |
| **Patients** | `GET` | `/api/patients` | Search & list patients (paginated) |
| **Patients** | `POST` | `/api/patients` | Register new patient |
| **Patients** | `GET` | `/api/patients/<id>` | Retrieve patient by ID |
| **Patients** | `PUT` | `/api/patients/<id>` | Update patient details |
| **Patients** | `DELETE`| `/api/patients/<id>` | Soft-delete / deactivate patient |
| **Patients** | `GET` | `/api/patients/<id>/balance` | Calculate patient outstanding balance |
| **Appointments** | `GET` | `/api/appointments` | Filter & list appointments |
| **Appointments** | `POST` | `/api/appointments` | Schedule appointment (conflict check) |
| **Appointments** | `GET` | `/api/appointments/<id>` | Retrieve appointment details |
| **Appointments** | `PUT` | `/api/appointments/<id>/cancel` | Cancel scheduled appointment |
| **Encounters** | `GET` | `/api/encounters` | List clinical encounters |
| **Encounters** | `POST` | `/api/encounters` | Record clinical encounter & bill |
| **Encounters** | `GET` | `/api/encounters/<id>` | Retrieve encounter details |
| **Billing** | `GET` | `/api/billing` | List billing invoices |
| **Billing** | `POST` | `/api/billing` | Create billing invoice |
| **Billing** | `GET` | `/api/billing/<id>` | Retrieve invoice details |
| **Billing** | `POST` | `/api/billing/<id>/payment` | Process payment against invoice |
| **Reports** | `GET` | `/api/reports/monthly-billing` | Report 1: Monthly billing summary |
| **Reports** | `GET` | `/api/reports/appointment-status` | Report 2: Appointment status breakdown |
| **Reports** | `GET` | `/api/reports/patient-visit-history/<id>` | Report 3: Patient visit timeline |
| **Reports** | `GET` | `/api/reports/provider-utilization` | Report 4: Provider utilization report |
| **Reports** | `GET` | `/api/reports/outstanding-billing` | Report 5: Accounts receivable aging |
| **Reports** | `GET` | `/api/reports/export/<name>` | Export report data to CSV |
| **Dashboard** | `GET` | `/api/dashboard/stats` | Executive KPI summary cards |
| **Providers** | `GET` | `/api/providers` | List clinical providers |

---

## 4. Detailed Endpoint Specifications

### 4.1 `POST /api/patients` (Register Patient)
Registers a new synthetic patient with validation and unique MRN assignment.

#### Request Body
```json
{
  "first_name": "Eleanor",
  "last_name": "Vance",
  "date_of_birth": "1994-06-18",
  "gender": "Female",
  "blood_group": "A+",
  "email": "eleanor.vance@fakehospital.org",
  "phone": "555-0188",
  "address": "742 Evergreen Terrace, Springfield",
  "emergency_contact_name": "Thomas Vance",
  "emergency_contact_phone": "555-0189"
}
```

#### Response (`201 Created`)
```json
{
  "success": true,
  "message": "Patient registered successfully",
  "data": {
    "patient_id": 26,
    "patient_mrn": "MRN-10026",
    "first_name": "Eleanor",
    "last_name": "Vance",
    "date_of_birth": "1994-06-18",
    "gender": "Female",
    "blood_group": "A+",
    "email": "eleanor.vance@fakehospital.org",
    "phone": "555-0188",
    "address": "742 Evergreen Terrace, Springfield",
    "emergency_contact_name": "Thomas Vance",
    "emergency_contact_phone": "555-0189",
    "is_active": 1,
    "created_at": "2026-11-02T12:00:00"
  }
}
```

---

### 4.2 `POST /api/appointments` (Schedule Appointment)
Schedules an appointment. Returns `409 Conflict` if the provider has an existing appointment at the requested datetime.

#### Request Body
```json
{
  "patient_id": 1,
  "provider_id": 3,
  "appointment_date": "2026-11-20",
  "appointment_time": "14:00",
  "duration_minutes": 30,
  "reason_for_visit": "Annual health checkup"
}
```

#### Response (`201 Created`)
```json
{
  "success": true,
  "message": "Appointment scheduled successfully",
  "data": {
    "appointment_id": 30,
    "patient_id": 1,
    "provider_id": 3,
    "appointment_date": "2026-11-20",
    "appointment_time": "14:00",
    "appointment_datetime": "2026-11-20 14:00:00",
    "duration_minutes": 30,
    "reason_for_visit": "Annual health checkup",
    "status": "SCHEDULED",
    "patient_name": "John Doe",
    "provider_name": "Elena Rostova",
    "provider_specialty": "General Medicine"
  }
}
```

#### Conflict Error (`409 Conflict`)
```json
{
  "success": false,
  "error": "Scheduling conflict: Dr. Rostova already has an active appointment at 2026-11-20 14:00:00."
}
```

---

### 4.3 `PUT /api/appointments/<id>/cancel` (Cancel Appointment)
Cancels a scheduled appointment. Validates that the appointment is not already completed.

#### Request Body
```json
{
  "cancellation_reason": "Patient had transport difficulties"
}
```

#### Response (`200 OK`)
```json
{
  "success": true,
  "message": "Appointment cancelled successfully",
  "data": {
    "appointment_id": 30,
    "status": "CANCELLED",
    "cancellation_reason": "Patient had transport difficulties",
    "cancelled_at": "2026-11-02T12:10:00"
  }
}
```

---

### 4.4 `POST /api/encounters` (Record Clinical Encounter)
Logs clinical progress notes, sets ICD-10 diagnosis code, marks linked appointment as `COMPLETED`, and automatically triggers billing invoice creation.

#### Request Body
```json
{
  "patient_id": 1,
  "provider_id": 1,
  "appointment_id": 1,
  "encounter_type": "OUTPATIENT",
  "chief_complaint": "Arrhythmia check and dizziness",
  "clinical_notes": "ECG confirms sinus rhythm with benign PVCs. Continued current regimen.",
  "diagnosis_code": "I49.3",
  "diagnosis_description": "Ventricular premature depolarization",
  "billing_amount": 250.00
}
```

#### Response (`201 Created`)
```json
{
  "success": true,
  "message": "Clinical encounter recorded successfully",
  "data": {
    "encounter_id": 23,
    "patient_id": 1,
    "provider_id": 1,
    "appointment_id": 1,
    "encounter_type": "OUTPATIENT",
    "chief_complaint": "Arrhythmia check and dizziness",
    "diagnosis_code": "I49.3",
    "diagnosis_description": "Ventricular premature depolarization",
    "status": "COMPLETED",
    "billed_total": 250.0,
    "balance_due": 250.0,
    "billing_status": "PENDING"
  }
}
```

---

### 4.5 `POST /api/billing/<id>/payment` (Record Payment)
Applies a payment to an invoice. Recalculates `balance_due` and updates invoice status (`PAID` or `PARTIALLY_PAID`).

#### Request Body
```json
{
  "payment_amount": 150.00,
  "payment_method": "CREDIT_CARD"
}
```

#### Response (`200 OK`)
```json
{
  "success": true,
  "message": "Payment applied successfully",
  "data": {
    "bill_id": 4,
    "bill_number": "INV-20260120-00004",
    "total_amount": 400.0,
    "paid_amount": 350.0,
    "balance_due": 50.0,
    "status": "PARTIALLY_PAID",
    "payment_applied": 150.0
  }
}
```

#### Overpayment Error (`400 Bad Request`)
```json
{
  "success": false,
  "error": "Payment amount ($500.00) exceeds remaining balance ($200.00)."
}
```

---

### 4.6 `GET /api/reports/monthly-billing` (Monthly Billing Summary)
#### Query Parameters
- `year` *(optional, integer)*: Calendar year filter (e.g. `2026`).

#### Response (`200 OK`)
```json
{
  "success": true,
  "message": "Monthly billing report generated",
  "data": [
    {
      "billing_month": "2026-01",
      "total_bills": 6,
      "total_billed": 1420.0,
      "total_collected": 1220.0,
      "total_outstanding": 200.0,
      "collection_rate_pct": 85.92,
      "paid_count": 5,
      "pending_count": 1,
      "overdue_count": 0
    }
  ]
}
```
