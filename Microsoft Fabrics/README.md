# 🧠 Employee Emotion & Burnout Analytics (Microsoft Fabric)

## 📌 Project Overview

This project implements an **end-to-end analytics solution using Microsoft Fabric** to analyze **employee emotions, sentiment, and burnout trends over time** based on textual “reason” inputs captured from upstream systems.

The solution follows a **Medallion Architecture (Bronze → Silver → Gold)** and delivers **analytics-ready datasets and Power BI dashboards** for organizational insights.

---

## 🎯 Business Objectives

- Track **emotion trends over time** (positive vs negative emotions)
- Monitor **burnout risk accumulation** using rolling metrics
- Measure **overall organizational sentiment health**
- Enable **department-level and organization-wide analysis**
- Provide **leadership-friendly KPIs** with slicers and drill-downs

---

## 🏗️ High-Level Architecture


Emotion Events (Blob Storage)
↓
Fabric Pipelines (Ingestion & Orchestration)
↓
Lakehouse (Bronze → Silver → Gold)
↓
Semantic Models (Direct Lake)
↓
Power BI Dashboards

---


---

## 🪵 Bronze Layer (Raw Ingestion)

**Purpose:**  
Store incoming emotion event data **exactly as received**, without transformations.

### Characteristics

- Raw, append-only data
- Schema-on-read
- Used for auditability and reprocessing

### Example Columns

- `created_at` (string)
- `reason_text`
- `employee_id`
- `department`

---

## 🪙 Silver Layer (Cleaned & Enriched)

**Purpose:**  
Clean, validate, standardize, and enrich emotion data for analytical use.

### Key Transformations

- Convert timestamps to `event_date`
- Standardize categorical values
- Enrichment using NLP / ML inference:
  - `emotion_type` (Joy, Anger, Sadness, etc.)
  - `intensity` (numeric scale)
  - `sentiment_bucket` (Positive / Neutral / Negative)
- Deduplicate records
- Separate **valid vs invalid data**
- Route invalid records to **Quarantine tables**

### Example Columns

- `event_date`
- `emotion_type`
- `intensity`
- `sentiment_bucket`
- `department`

---

## 🥇 Gold Layer (Analytics-Ready Tables)

Gold tables are **stable, aggregated, and optimized for BI consumption**.

---

### 1️⃣ Emotion Trend Daily  
**Table:** `emotion_trend_daily`

**Grain:**
- `event_date + emotion_type + department`

**Metrics:**
- `emotion_count`
- `avg_emotion_score`
- `emotion_percentage`

**Use Cases:**
- Emotion trend analysis
- Positive vs negative emotion distribution

---

### 2️⃣ Sentiment Daily Metrics  
**Table:** `gold_sentiment_daily`

**Grain:**
- `event_date + department + sentiment_bucket`

**Metrics:**
- `sentiment_count`
- `sentiment_percentage`

**Derived Metric:**
- Net Sentiment Score

---

### 3️⃣ Burnout Daily Metrics  
**Table:** `gold_burnout_daily_metrics`

**Concept:**  
Burnout is treated as a **derived, cumulative signal**, not a direct input.

**Inputs:**
- Daily negative emotion intensity

**Metrics:**
- `avg_negative_score`
- `rolling_7d_negative_avg`
- `burnout_level` (Low / Medium / High)

---

## 📊 Power BI Dashboard Design

### 🔹 Page 1 — Organizational Overview

<img width="1140" height="652" alt="PowrBI screenshot" src="https://github.com/user-attachments/assets/f9a62d8e-58aa-45b3-bda6-6dae68cc8598" />


#### KPI Cards

- Average Burnout Score
- High Burnout Percentage
- Average Emotion Intensity
- Positive Sentiment Percentage

> KPIs dynamically respond to **date and department slicers**

---

### 📈 Emotion Trend Over Time

- Line chart
- X-axis: `event_date`
- Y-axis: Average Emotion Intensity
- Legend: Emotion Type

Shows how **emotional climate evolves over time**.

---

### 📉 Burnout Trend Over Time

- Dual-axis line chart
- Primary axis: Average Burnout Score
- Secondary axis: High Burnout %

Highlights **burnout risk accumulation**.

---

### 🍩 Burnout Distribution

- Donut chart
- Distribution of Low / Medium / High burnout
- Fully slicer-aware

---

### 🎛️ Slicers

- Date
- Department
- Emotion Type
- Burnout Level

---

## 🧠 Key Modeling Decisions

- Gold tables are **aggregated facts**, not entity tables
- No single primary key in Gold layer
- Date used as the **analysis axis**
- Department handled via slicers, not composite keys
- Burnout calculated using **rolling windows**, not point-in-time spikes

---
## 🛡️ Data Governance, Lineage & Audit

This project implements enterprise-grade data management practices:

- Incremental and CDC-based data ingestion
- Batch-level audit logging (record counts, processing status)
- Table-level metadata for governance and ownership
- Quarantine handling for invalid data
- End-to-end pipeline orchestration with lineage visibility

---

## ⚠️ Known Limitations

- Emotion inference accuracy depends on NLP model quality
- Personal reasons may introduce noise at department level
- Burnout metrics are **indicators**, not medical diagnoses

---

## 🚀 Future Enhancements

- ML confidence scoring for emotion predictions
- Reason classification (Professional vs Personal)
- Holiday and calendar impact analysis
- Drill-through to employee-level views
- Automated alerts for sustained high burnout

---

## 🧩 Tech Stack

- **Microsoft Fabric** (Lakehouse, Pipelines)
- **PySpark** (Data Engineering & Transformations)
- **Power BI** (Direct Lake Semantic Models & Reports)


---

## ✅ Project Status

✔ Bronze → Silver → Gold implemented  
✔ Fabric pipelines orchestrated  
✔ Semantic models & dashboards completed  
🔜 Advanced ML enrichment planned  


**Platform:** Microsoft Fabric
