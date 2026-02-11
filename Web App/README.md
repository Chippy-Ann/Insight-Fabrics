# Insight Fabrics – Emotion Capture Web App (.NET 9.0)

This is a **single-page .NET 9.0 web application** that captures users' emotional events and stores them securely in an Azure SQL Database.  
It follows an **MVC-like architecture** with **Models, Views, and Controllers**.

---

## Purpose

- Capture human emotions as structured events
- Record:
  - Emotion type
  - Intensity
  - Trigger/reason
  - User information
  - Timestamp
- Provide a simple, interactive, and responsive front-end
- Store data securely in Azure SQL for downstream processing and analytics

---

## Architecture

### MVC Structure

- **Model:** Defines the structure of the emotional event (Emotion, Intensity, Reason, User, Timestamp)  
- **View:** Single-page responsive form for user input  
- **Controller:** Handles form submission, validation, and database insertion  

### Database Integration

- Connected to **Azure SQL Database** provisioned in Phase 1
- Uses **Entity Framework / SQL Connection** to store emotion events
- Secrets (connection strings) are retrieved securely from **Azure Key Vault**

---

## Front-End Interface

**User Flow / Form Fields:**

1. **Name:**  
   - Input box: “Enter your name”

2. **Emotion Selection:**  
   - Options: `Anger`, `Joy`, `Sadness`, `Disgust`, `Fear`  

3. **Trigger / Reason:**  
   - Text input: “What triggered it?”

4. **Intensity:**  
   - Dropdown: Select intensity (e.g., 1–10)

5. **Submit Button:**  
   - Saves the event to Azure SQL

---

## Example UI Layout

<img width="1916" height="976" alt="image" src="https://github.com/user-attachments/assets/ada120a0-8582-4de2-bcc1-efdd3e9c0a2b" />
<img width="1302" height="746" alt="image" src="https://github.com/user-attachments/assets/8560659d-6516-4724-b737-50c1ed14fa38" />
<img width="1303" height="137" alt="image" src="https://github.com/user-attachments/assets/965fa3de-477c-46db-8ae8-2a3c5ba5e854" />

## Output 

<img width="1918" height="916" alt="image" src="https://github.com/user-attachments/assets/0f7229e0-a0ec-4e0c-a73f-c619d95a6eec" />



