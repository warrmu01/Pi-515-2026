# Pi-515-2026

## Documentation

### 🔍 Overview

**This project is an AI-powered irrigation decision support system designed to help farmers optimize water usage using environmental data. The system predicts soil moisture levels based on weather and location features and translates those predictions into actionable irrigation recommendations (**Low, Medium, High**).

This project uses a **chained modeling architecture**, where intermediate environmental variables (soil temperature) are predicted and used to improve downstream predictions (soil moisture), creating a realistic and scalable decision-making system.

---

### 🏗️ System Architecture

- **Frontend (In Progress)**
  - Collects user inputs:
    - Location
    - Date / Date Range
  - Displays:
    - Predicted soil moisture
    - Irrigation recommendations

- **Backend (Python / Flask - Planned)**
  - Fetches environmental data (weather APIs or dataset)
  - Runs a chained prediction pipeline:
    - Predict soil temperature
    - Predict soil moisture
    - Generate irrigation recommendation

- **Models**
  - Built using **XGBoost Regression**
  - Saved as `.joblib` files in `src/models/`

---

## 🔗 Chained Model Architecture

The system follows a sequential prediction pipeline:

1. **Input Features**
   - Air Temperature  
   - Dew Point Temperature  
   - Precipitation  
   - Evaporation  
   - Runoff  
   - Location (Latitude)  
   - Time Features (Month, Year)  

2. **Model 1: Predict Soil Temperature**
   - Uses environmental features  

3. **Model 2: Predict Soil Moisture**
   - Uses environmental features + predicted soil temperature  

4. **Decision Layer: Irrigation Recommendation**
   - Converts soil moisture into:
     - **LOW** → sufficient moisture  
     - **MEDIUM** → moderate irrigation needed  
     - **HIGH** → urgent irrigation needed


---
## 📁 Project Structure.


```
PI515-AI/
├── Data/
│   └── Raw/
│       ├── Main_Data.xlsx
│       └── Main_Data_edited.xlsx
│
├── app/
│   │
│   ├── js/
│   │   ├── predict.js
│   │   └── script.js
│   │
│   ├── css/
│   │   ├── predict.css
│   │   ├── about.css
│   │   └── style.css
│   │
│   ├── models/
│   │   └── am_transparency_model.joblib
│   │   └── pm_transparency_model.joblib
│   │   └── fish_survial_model.joblib
│   │   └── spring_temp_model.joblib
│   │
│   │
│   ├── templates/
│   │   └── about.html
│   │   └── index.html
│   │   └── predict.html
│   
│ 
├── src/
│   ├── __pycache__/
│   │
│   ├── Data_Preparation/
│   │   ├── fish_survival_data_preparation.ipynb
│   │   ├── fish_survival_data_preparation.py
│   │   ├── Spring_temp_data_preparation.ipynb
│   │   ├── Spring_temp_data_preparation.py
│   │   ├── Transparency_data_preparation.ipynb
│   │   └── Transparency_data_preparation.py
│   │
│   ├── models/
│   │   └── am_transparency_model.joblib
│   │   └── pm_transparency_model.joblib
│   │   └── fish_survial_model.joblib
│   │   └── spring_temp_model.joblib
│   │
│   ├── notebooks/
│   │   ├── fish_survival_model.ipynb
│   │   ├── spring_temp_model.ipynb
│   │   └── transparency_model.ipynb
│   │
│   ├── py/
│   │   ├── fish_survival_model.py
│   │   ├── spring_temp_model.py
│   │   └── transparency_model.py
│   │
│   ├── chained_model.ipynb
│   ├── DNN.ipynb
│   ├── timeseries_utils.py
│   └── EDA.ipynb
│
├── README.md
├── requirements.txt
```

## 📊 Model Performance Summary

### 🌡️ Soil Temperature Model (XGBoost)

- **Key Insight**: Air temperature is the dominant predictor (~92% importance)

**Performance:**
- RMSE: ~0.15  
- MAE: ~0.11  
- R²: ~0.97+  

---

### 💧 Soil Moisture Model (XGBoost)

- **Key Insight**: Predicted soil temperature is the most important feature

**Performance:**
- RMSE: ~0.05  
- MAE: ~0.038  
- R²: ~0.62–0.64  

---

## 📌 Why RMSE, MAE, and R²?

- **RMSE** measures absolute prediction error magnitude  
- **MAE** provides stable, interpretable error  
- **R²** shows explained variance  

MAPE is not used because the target values are scaled and can include small values, which can distort percentage-based metrics.

---

## 🌍 Real-World Use Case

### User Inputs:
- Location  
- Date / Date Range  

### System Automatically:
- Retrieves weather data (via APIs)  
- Estimates environmental variables  
- Runs AI models  

### Outputs:
- Predicted soil moisture  
- Irrigation recommendation (Low / Medium / High)  

---

## 🚀 Why This Project Matters

- 🌱 **Environmental Impact**: Reduces water waste  
- 💰 **Economic Impact**: Lowers irrigation costs  
- 📈 **Scalability**: Works across regions and crops  
- 👨‍🌾 **Usability**: Designed for non-technical users  

---
