# Engineering Root Cause Analysis (RCA)

This document details three real-world engineering defects encountered and investigated during the development of the **Healthcare Data Management and Analytics System**, outlining the symptoms, root causes, technical resolutions, and preventative measures implemented.

---

## Issue 1: Cumulative Floating-Point Precision Divergence in Billing Reconciliation

### 1. Symptom & Discovery
During the initial implementation of the billing payment service, applying sequential payments (e.g., \$100.00 followed by \$100.00 on a \$200.00 balance) occasionally caused invoice statuses to stay in `PARTIALLY_PAID` with a phantom remaining balance such as `$0.00000000000000004` rather than reaching `$0.00` (`PAID`). Furthermore, database check constraints (`chk_bill_amounts`: `paid_amount + balance_due = total_amount`) failed sporadically on payment updates.

### 2. Root Cause Analysis
Python's native `float` type adheres to IEEE 754 double-precision binary floating-point arithmetic. Certain decimal values (such as `0.1`, `0.2`, `0.7`) cannot be represented accurately in base-2 binary fractions, causing micro-rounding drift. When float calculations were performed and compared against database fixed-point `NUMBER(10, 2)` columns, strict equality checks (`paid + balance == total`) evaluated to `False`.

### 3. Engineering Resolution
- Replaced all floating-point math across models, repositories, and validators with Python's standard `decimal.Decimal` module.
- Standardized quantization to two decimal places using `ROUND_HALF_UP`:
  ```python
  CENT = Decimal("0.01")
  d = Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
  ```
- Created a dedicated utility module `app/utils/decimal_utils.py` containing `validate_billing_math()` and `calculate_balance()`.
- Validated all monetary check constraints in Oracle and SQLite schemas (`CHECK (paid_amount <= total_amount AND balance_due = total_amount - paid_amount)`).

### 4. Verification
Automated unit tests (`test_exact_decimal_conversion`, `test_no_float_precision_leak`, `test_calculate_balance`, and `test_billing_paid_exceeds_total_constraint_enforced`) guarantee zero floating-point leakage.

---

## Issue 2: Concurrent Provider Schedule Overlap & Duplicate Bookings

### 1. Symptom & Discovery
When two appointment requests were submitted nearly simultaneously for the same provider at the exact same start time (e.g. Dr. Jenkins at `2026-11-15 09:00:00`), both appointments were initially granted and saved, creating an illegal double-booking condition on the provider's schedule.

### 2. Root Cause Analysis
The application initially performed an application-level `SELECT` query to check if the slot was free before issuing an `INSERT`. Under concurrent request execution, two requests read the unbooked slot simultaneously before either transaction committed, causing a classic Time-of-Check to Time-of-Use (TOCTOU) race condition.

### 3. Engineering Resolution
- Added a database-level composite unique constraint on `APPOINTMENTS`:
  ```sql
  CONSTRAINT uq_prov_slot UNIQUE (provider_id, appointment_datetime)
  ```
- In Oracle and SQLite, any simultaneous attempt to insert a duplicate timestamp for that provider is atomically aborted at the storage engine level with a unique constraint violation.
- Enhanced `DatabaseManager._handle_db_exception` in `app/repositories/db.py` to intercept Oracle error `ORA-00001` and SQLite `UNIQUE constraint failed`, transforming it into an application-level `ConflictException` with an HTTP `409 Conflict` response.
- Preserved application-layer validation `AppointmentRepository.check_conflict()` for fast pre-validation and user-friendly error messages.

### 4. Verification
Verified via `test_schedule_conflicting_appointment_fails` and `test_api_schedule_appointment_conflict`.

---

## Issue 3: Cross-Platform ISO-8601 Date Formatting Inconsistency in REST Responses

### 1. Symptom & Discovery
When querying API endpoints (e.g., `/api/patients`, `/api/appointments`), date and timestamp values returned inconsistent data types. In SQLite, timestamps were returned as plain text strings, whereas Oracle DB (`python-oracledb`) returned native `datetime.datetime` and `datetime.date` objects. This led to `TypeError: Object of type datetime is not JSON serializable` in Flask's default `jsonify`.

### 2. Root Cause Analysis
Different database drivers return different Python object representations for temporal columns:
- `sqlite3` returns raw `TEXT` unless converters are configured.
- `oracledb` returns native Python `datetime.datetime` objects.
Attempting to feed un-serialized Python datetime objects into standard JSON responses triggers serialization crashes unless explicitly formatted.

### 3. Engineering Resolution
- Engineered a recursive serialization helper `serialize_item()` inside `app/utils/response.py`:
  ```python
  def serialize_item(item):
      if isinstance(item, dict):
          return {k: serialize_item(v) for k, v in item.items()}
      elif isinstance(item, list):
          return [serialize_item(x) for x in item]
      elif isinstance(item, Decimal):
          return float(item)
      elif isinstance(item, (datetime, date)):
          return item.isoformat()
      return item
  ```
- All API routes utilize `api_success()` and `api_paginated()` which enforce `serialize_item()`, ensuring consistent ISO-8601 strings (`YYYY-MM-DD` and `YYYY-MM-DDTHH:MM:SS`) regardless of underlying database driver.

### 4. Verification
All 55 automated integration tests execute cleanly with valid JSON serialization across all endpoints.
