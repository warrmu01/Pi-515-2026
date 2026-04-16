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
