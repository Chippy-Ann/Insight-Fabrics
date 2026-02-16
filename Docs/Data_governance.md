# 🛡️ Data Governance, Lineage & Audit Design

This document explains how enterprise data governance principles are implemented
across Bronze, Silver, and Gold layers in Microsoft Fabric.

---

## 🔄 Incremental & CDC-Based Loads

- Source data is ingested incrementally into the Bronze layer.
- Each batch is tagged with:
  - `batch_id`
  - `data_ingested_on`
- Only unprocessed batches are promoted to Silver.

---

## 🧪 Data Quality & Compliance

- Invalid or non-compliant records are routed to a **Quarantine table**.
- Quarantine data is excluded from analytics layers.
- Data validation rules include:
  - Null checks
  - Range validation
  - Schema consistency

---

## 📊 Audit Logging

Batch-level audit information is captured in dedicated audit tables.

### Example:
- `bronze_batch_log`

Each batch records:
- Batch ID
- Record counts
- Processing status


This enables traceability and reprocessing if needed.

---

## 🧠 Metadata Management

A static `table_metadata` table documents:

- Table name
- Layer (Bronze / Silver / Gold)
- Grain
- Business owner
- Refresh frequency

This table is:
- Created once
- Manually maintained
- Not updated per batch

---

## 🔗 Data Lineage

- End-to-end pipeline orchestration is handled via a master pipeline.
- Fabric’s built-in lineage view is used to track:
  - Source → Bronze → Silver → Gold flow
  - Dataset and report dependencies

No custom lineage tables are required.

---

## ✅ Summary

| Capability | Implemented |
|---------|------------|
| Incremental Loads | ✔ |
| CDC Support | ✔ |
| Audit Logging | ✔ |
| Data Quality & Quarantine | ✔ |
| Metadata Management | ✔ |
| Lineage Tracking | ✔ |
