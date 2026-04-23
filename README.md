# Pi-515-2026

## Documentation

### 🔍 Overview

**This project is an AI-powered irrigation decision support system designed to help farmers optimize water usage using environmental data. The system predicts soil moisture levels based on weather and location features and translates those predictions into actionable irrigation recommendations (**Low, Medium, High**).

This project uses a **chained modeling architecture**, where intermediate environmental variables (soil temperature) are predicted and used to improve downstream predictions (soil moisture), creating a realistic and scalable decision-making system.

---

### 🏗️ System Architecture

### Frontend (In Progress)
- User inputs:
  - Location (Latitude / Longitude)
  - Date / Date Range  
- Outputs:
  - Predicted soil moisture  
  - Irrigation recommendation  

---

### Backend (Python / Flask - Planned)
- Fetches environmental data (e.g., weather APIs)  
- Runs the chained prediction pipeline:
  1. Predict soil temperature  
  2. Predict soil moisture  
  3. Generate irrigation recommendation  

---

### Models
- Built using **XGBoost Regression**
- Stored in `src/models/`
- Includes:
  - SMOS-only models  
  - Combined (SMOS + SCAN) models  
  - Feature scalers  

---

## 🔗 Chained Model Architecture

Environmental Data → Soil Temperature → Soil Moisture → Irrigation Recommendation

### Input Features:
- Air Temperature  
- Dew Point Temperature  
- Total Precipitation  
- Location (Latitude, Longitude)  
- Time Features (Year, Month, Day)  

### Step 1: Soil Temperature Model  
Predicts soil temperature using environmental features.

### Step 2: Soil Moisture Model  
Uses:
- Environmental features  
- Predicted soil temperature  

### Step 3: Decision Layer  
Outputs irrigation level:
- **LOW** → sufficient moisture  
- **MEDIUM** → moderate irrigation needed  
- **HIGH** → urgent irrigation needed  

---

## 📁 Project Structure.

```
PI515-AI/
├── Data/
│ ├── train.csv
│ └── test.csv
│
├── app/ 
│ │ ├── app.py
│ │ ├── open_mateo.py
│ │ └── predict.py
│ │
│ ├── css/
│ │ ├── predict.css
│ │ ├── about.css
│ │ └── style.css
│ │
│ ├── templates/
│ │ ├── about.html
│ │ ├── index.html
│ │ └── predict.html
│ │
│ ├── models/ (optional deployment copies)
│ │ ├── soil_temperature_model.joblib
│ │ └── soil_moisture_model.joblib
│
├── src/
│ ├── pycache/
│ │
│ ├── Data_Preparation/
│ │ ├── soil_temp_data_preparation.ipynb
│ │ ├── soil_temp_data_preparation.py
│ │ ├── soil_moisture_data_preparation.ipynb
│ │ └── soil_moisture_data_preparation.py
│ │
│ ├── models/
│ │ ├── soil_temperature_model.joblib
│ │ └── soil_moisture_model.joblib
│ │
│ ├── notebooks/
│ │ ├── soil_temp_model.ipynb
│ │ └── soil_moisture_model.ipynb
│ │ └── EDA.ipynb
│ │
│ ├── py/
│ │ ├── soil_temp_model.py
│ │ └── soil_moisture_model.py
│ │
│
├── README.md
├── requirements.txt
```
---

## 📊 Model Performance Summary

### 🌡️ Soil Temperature Model

| Model | Dataset | R² |
|------|--------|----|
| SMOS-only | SMOS | **0.9839** |
| Combined | SMOS | **0.9768** |
| Combined | SCAN | **0.9633** |

**Insight:**  
Small drop in SMOS accuracy, but strong generalization to real-world SCAN data.

---

### 💧 Soil Moisture Model

| Model | Dataset | R² |
|------|--------|----|
| SMOS-only | SMOS | **0.6906** |
| Combined | SMOS | **0.6880** |
| Combined | SCAN | **0.6605** |

**Insight:**  
Maintains SMOS performance while enabling real-world predictions.

---

### 🌍 Generalization (Combined Model)

| Dataset | R² |
|--------|----|
| Train | 0.6865 |
| Dev | 0.6818 |
| SMOS Test | 0.6880 |
| SCAN Holdout | 0.6605 |

**Insight:**  
Consistent performance across datasets indicates strong generalization and minimal overfitting.

---

## 📌 Evaluation Metrics

- **RMSE** → Measures prediction error magnitude  
- **MAE** → Provides interpretable average error  
- **R²** → Measures explained variance  

MAPE is not used due to scaled values and sensitivity to small numbers.

---

## 🌍 Real-World Use Case

### User Inputs:
- Location  
- Date / Date Range  

### System:
- Fetches weather data  
- Runs AI models  

### Outputs:
- Soil moisture prediction  
- Irrigation recommendation  

---

## 🚀 Why This Project Matters

- 🌱 **Environmental Impact** → Reduces water waste  
- 💰 **Economic Impact** → Lowers irrigation costs  
- 🌍 **Real-World Validity** → Uses SCAN sensor data  
- 📈 **Scalability** → Works across regions  
- 👨‍🌾 **Usability** → Simple, farmer-friendly outputs  

---
