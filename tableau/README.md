# Tableau Public Interactive Analytics Dashboard

## 1. Overview

This directory provides complete instructions, data dictionaries, calculated fields, and reproduction steps for building the **HealthPulse Clinical & Revenue Analytics Dashboard** on **Tableau Public** using synthetic datasets exported from the application database.

All underlying data is fictional and synthetically generated. No protected health information (PHI), credentials, or confidential database host details are contained within or published to Tableau Public.

---

## 2. Exported Datasets

The exported datasets are generated directly from the normalized database schema via `python scripts/export_reports_to_csv.py`:

| Dataset File | Primary Table Association | Records | Purpose in Tableau |
| :--- | :--- | :--- | :--- |
| `tableau/exports/full_synthetic_dataset.csv` | Master Denormalized Query | 29 | Master data source for Tableau workbook combining appointments, patients, providers, encounters, and billing. |
| `tableau/exports/monthly_billing_summary.csv` | `VW_MONTHLY_BILLING_SUMMARY` | 4 | Monthly revenue, collections, and outstanding receivables. |
| `tableau/exports/appointment_status_summary.csv` | `VW_APPOINTMENT_ANALYTICS` | 8 | Department appointment volume and cancellation ratios. |
| `tableau/exports/provider_utilization_summary.csv` | `VW_PROVIDER_WORKLOAD` | 8 | Provider clinical completion rates and billable volume. |
| `tableau/exports/outstanding_billing_summary.csv` | `VW_OUTSTANDING_BALANCES` | 8 | Detailed overdue accounts receivable aging. |

---

## 3. Data Dictionary: `full_synthetic_dataset.csv`

| Field Name | Data Type | Role in Tableau | Description |
| :--- | :--- | :--- | :--- |
| `appointment_id` | Number (Whole) | Dimension | Unique appointment identifier |
| `appointment_date` | Date | Dimension | Date of consultation (`YYYY-MM-DD`) |
| `appointment_time` | String | Dimension | Scheduled time slot (`HH:MM`) |
| `appointment_datetime` | Date & Time | Dimension | Timestamp used for temporal grouping |
| `duration_minutes` | Number (Whole) | Measure | Appointment length in minutes |
| `reason_for_visit` | String | Dimension | Chief reason given by patient |
| `appointment_status` | String | Dimension | `SCHEDULED`, `CONFIRMED`, `COMPLETED`, `CANCELLED`, `NO_SHOW` |
| `cancellation_reason` | String | Dimension | Audit explanation for cancelled visits |
| `patient_id` | Number (Whole) | Dimension | Unique patient surrogate key |
| `patient_mrn` | String | Dimension | Medical Record Number (`MRN-XXXXX`) |
| `patient_name` | String | Dimension | Full patient name |
| `patient_gender` | String | Dimension | Patient demographic gender |
| `provider_id` | Number (Whole) | Dimension | Provider surrogate key |
| `provider_name` | String | Dimension | Attending clinician name |
| `provider_department` | String | Dimension | Clinical department |
| `provider_specialty` | String | Dimension | Clinical specialty |
| `encounter_id` | Number (Whole) | Dimension | Encounter identifier (if completed) |
| `diagnosis_code` | String | Dimension | ICD-10 diagnostic code |
| `diagnosis_description` | String | Dimension | Plain English diagnosis title |
| `billed_amount` | Number (Decimal) | Measure | Total charges invoiced ($) |
| `paid_amount` | Number (Decimal) | Measure | Total collections received ($) |
| `balance_due` | Number (Decimal) | Measure | Outstanding balance due ($) |
| `billing_status` | String | Dimension | `PAID`, `PARTIALLY_PAID`, `PENDING`, `OVERDUE` |

---

## 4. Calculated Fields Specification

Create the following calculated fields in Tableau Desktop / Tableau Public:

### 1. Collection Rate Percentage
- **Formula**:
  ```tableau
  IF SUM([billed_amount]) > 0 THEN
      (SUM([paid_amount]) / SUM([billed_amount])) * 100
  ELSE
      0
  END
  ```
- **Number Format**: Percentage, 1 decimal place.

### 2. Cancellation Rate Percentage
- **Formula**:
  ```tableau
  (COUNT(IF [appointment_status] = 'CANCELLED' THEN [appointment_id] END) / COUNT([appointment_id])) * 100
  ```
- **Number Format**: Percentage, 1 decimal place.

### 3. Provider Utilization Rate
- **Formula**:
  ```tableau
  (COUNT(IF [appointment_status] = 'COMPLETED' THEN [appointment_id] END) / COUNT([appointment_id])) * 100
  ```
- **Number Format**: Percentage, 1 decimal place.

### 4. Overdue Balance Indicator
- **Formula**:
  ```tableau
  IF [billing_status] = 'OVERDUE' OR ([billing_status] = 'PENDING' AND [balance_due] > 0) THEN
      [balance_due]
  ELSE
      0
  END
  ```

---

## 5. Dashboard Visualizations Construction

Build the following 6 visual worksheets:

### Sheet 1: Monthly Patient Visit & Encounter Trends
- **Chart Type**: Line Chart with Data Points.
- **Columns**: `MONTH([appointment_date])` (Continuous).
- **Rows**: `COUNT([appointment_id])`, `COUNT([encounter_id])`.
- **Marks**: Dual Axis (Synchronized). Blue line for Appointments, Green line for Clinical Encounters.

### Sheet 2: Appointment Status Distribution
- **Chart Type**: Donut Chart.
- **Marks**: Pie chart with `[appointment_status]` on Color and `COUNT([appointment_id])` on Angle.
- **Color Palette**:
  - `COMPLETED`: Soft Green (`#2ecc71`)
  - `CONFIRMED`: Deep Blue (`#3498db`)
  - `SCHEDULED`: Light Sky Blue (`#00c0ef`)
  - `CANCELLED`: Red Coral (`#e74c3c`)
  - `NO_SHOW`: Amber Orange (`#f39c12`)

### Sheet 3: Appointment Cancellation Trends by Department
- **Chart Type**: Horizontal Stacked Bar Chart.
- **Rows**: `[provider_department]`.
- **Columns**: `COUNT([appointment_id])`.
- **Color**: `[appointment_status]` (Filtered to show Completed vs Cancelled).

### Sheet 4: Monthly Billing & Revenue Collections
- **Chart Type**: Side-by-Side Bar Chart.
- **Columns**: `MONTH([billing_date])`.
- **Rows**: `Measure Values` (`SUM([billed_amount])`, `SUM([paid_amount])`, `SUM([balance_due])`).
- **Color**: `Measure Names` (Blue = Billed, Green = Paid, Red = Balance).

### Sheet 5: Outstanding Receivables by Provider Department
- **Chart Type**: Treemap / Bar Chart.
- **Rows**: `[provider_department]`.
- **Columns**: `SUM([balance_due])`.
- **Label**: `SUM([balance_due])` formatted as Currency.

### Sheet 6: Provider Utilization & Completion Efficiency
- **Chart Type**: Bullet Graph / Bar with Target Line.
- **Rows**: `[provider_name]`.
- **Columns**: `[Provider Utilization Rate]`.
- **Reference Line**: Institutional 80% Benchmark Line.

---

## 6. Interactive Dashboard Layout & Filters

Combine the 6 sheets onto a unified 1200x800 Dashboard Canvas:

```
+---------------------------------------------------------------------------------------+
|  HealthPulse Executive Analytics Dashboard                  [Date Filter] [Dept Filter]|
+---------------------------------------------------------------------------------------+
|  KPI: Active Patients | Total Billed: $5,860.00 | Paid: $4,005.00 | Outstanding: $1,855.00 |
+-------------------------------------------+-------------------------------------------+
|  [Sheet 1: Monthly Patient Visits Trend]  |  [Sheet 2: Appointment Status Donut]      |
|                                           |                                           |
+-------------------------------------------+-------------------------------------------+
|  [Sheet 4: Billed vs Collected Bar Chart] |  [Sheet 3: Department Cancellations]      |
|                                           |                                           |
+-------------------------------------------+-------------------------------------------+
|  [Sheet 6: Provider Utilization Ratios]   |  [Sheet 5: Outstanding Balance Breakdown] |
|                                           |                                           |
+---------------------------------------------------------------------------------------+
```

### Dashboard Interactivity & Filters:
1. **Global Date Range Filter**: `[appointment_date]` slider.
2. **Provider Department Filter**: Multi-select dropdown.
3. **Appointment Status Filter**: Multi-select dropdown.
4. **Interactive Dashboard Action**: Clicking any provider or department filters all charts synchronously.

---

## 7. How to Refresh Data and Reproduce the Dashboard

1. Run the data generator to query the latest database state and update CSVs:
   ```bash
   python scripts/export_reports_to_csv.py
   ```
2. Open **Tableau Public** or **Tableau Desktop**.
3. Select **Connect to Data** -> **Text file** -> Choose `tableau/exports/full_synthetic_dataset.csv`.
4. In Tableau, click **Data** -> **Refresh** to instantly pull the newly exported database records.
5. Save or publish to your Tableau Public profile.
