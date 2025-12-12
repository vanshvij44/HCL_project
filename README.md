# Machine Learning regression analysis used for predictive analysis

## Team members

### Vansh Vij
### Atharva Patil
### Ramkishan Suthar
## Project Overview


<img width="1163" height="679" alt="image" src="https://github.com/user-attachments/assets/c9d987da-1ae1-43f0-9540-c1b30aec3034" />

## 1. Column Renaming
Many column names contained spaces or special characters. They were renamed for readability and ML compatibility.

```
EXEC sp_rename 'customer__churn.[Usage Frequency]', 'Usage_freq', 'COLUMN';
EXEC sp_rename 'customer__churn.[Payment Delay]', 'PaymentDelay', 'COLUMN';
EXEC sp_rename 'customer__churn.[Support Calls]', 'SupportCalls', 'COLUMN';
EXEC sp_rename 'customer__churn.[Subscription Type]', 'Subscription_Type', 'COLUMN';
EXEC sp_rename 'customer__churn.[Contract Length]', 'Contract_Length', 'COLUMN';
EXEC sp_rename 'customer__churn.[Total spend]', 'Total_spend', 'COLUMN';
EXEC sp_rename 'customer__churn.[Last Interaction]', 'Last_Interaction', 'COLUMN';
```

## 2. Missing Value Check
The dataset was scanned for missing values:
```
SELECT * FROM customer__churn WHERE 
Age IS NULL OR Gender IS NULL OR Usage_freq IS NULL OR SupportCalls IS NULL;
```

## 3. Duplicate Check
To verify CustomerID uniqueness:
```
SELECT CustomerID, COUNT(*) 
FROM customer__churn 
GROUP BY CustomerID 
HAVING COUNT(*) > 1;
```

## 4. Data Type Conversion
Converted all numeric columns to FLOAT for ML compatibility.

## 5. Removing Blank Rows
Rows with blank categorical fields were removed.

## 6. Outlier Detection (IQR)
Applied IQR for Age, Usage Frequency, Support Calls, Payment Delay, Total Spend, Last Interaction.

## 7. Encoding Categorical Columns
### Label Encoding (Gender)
```
UPDATE customer__churn SET Gender_Label = CASE WHEN Gender='Male' THEN 1 ELSE 0 END;
```

### One-Hot Encoding (Subscription Type)
Created Sub_Basic, Sub_Standard, Sub_Premium.

### Contract Length Conversion(Standardization)
Converted Annual→12, Quarterly→3, Monthly→1.

## Conclusion
Dataset is now clean, encoded, and fully machine-learning-ready.
=======
### EDA and Regression 
Data cleaning and preprocessing
Univariate and bivariate analysis
Correlation and feature relationship studies
Creation of engineered features
Regression and classification model development
Model evaluation and interpretation

1. Data Quality
No missing values after removing invalid CustomerID entries
No duplicate rows
Features separated into numerical and categorical groups for analysis
2. Variable Distributions
Age, Usage Frequency, Support Calls, and Payment Delay show smooth unimodal distributions

Tenure appears uniformly distributed without strong patterns
Churn is imbalanced, with more non-churners than churners

3. Correlation Analysis
Most features have very weak correlation with Tenure
Behavioral factors such as Support Calls, Payment Delay, and Total Spend show stronger relevance to Churn
The correlation heatmap confirms limited linear relationships for regression tasks
Classification (Predicting Churn) displays clearer feature influence than regression (Predicting Tenure)

4. Feature Engineering
The following engineered variables were created to enhance modeling:


Engagement Score=
Usage Frequency + Total Spend – Payment Delay – Support Calls

Risk Score=
Payment Delay + Support Calls – Last Interaction

Spend Per Month=
Total Spend / Contract Length

Encoded categorical variables for Subscription Type, Contract Type, and Gender

These features improved churn prediction but did not significantly improve tenure prediction due to the weak underlying relationships.

5. Graph Analysis
   Graph Explanations from EDA
      1. KDE Plot of Age
      
      What it shows:
      A Kernel Density Estimate (KDE) plot visualizing the distribution of customer ages.
      
      Interpretation:
      
      The distribution appears smooth and unimodal.
      
      Most customers fall in the middle-age range (around 30–50).
      
      Very few customers are extremely young or extremely old.
      
      Why it matters:
      Helps understand the age demographics of customers and check whether age is balanced or skewed.
      
      2. Churn Value Counts (Bar Plot)
      
      What it shows:
      A simple bar chart showing the number of churned vs non-churned customers.
      
      Interpretation:
      
      Non-churners significantly outnumber churners.
      
      The dataset is imbalanced, which affects classification performance and requires careful model evaluation.
      
      Why it matters:
      Imbalanced datasets need techniques like class weighting or resampling for fair modeling.
      
      3. Gender vs Churn (Grouped Bar Chart)
      
      What it shows:
      A bar graph comparing how many males and females churned or did not churn.
      
      Interpretation:
      
      Churn count is roughly similar between genders.
      
      No strong pattern indicates that gender is not a dominant predictor of churn.
      
      Why it matters:
      Helps check whether churn behavior differs across genders.
      
      4. Multiple KDE Plots for Numerical Columns
      
      Columns plotted include:
      
      Age
      
      Usage Frequency
      
      Support Calls
      
      Payment Delay
      
      Total Spend
      
      Last Interaction
      
      Interpretation:
      
      Most numerical features show unimodal smooth distributions.
      
      Some features like Support Calls & Payment Delay have long tails, showing varied customer behavior.
      
      None show strong visual relationship with Tenure.
      
      Why it matters:
      Helps detect skewness, outliers, and the general behavior of numeric variables.
      
      5. Correlation Heatmap
      
      What it shows:
      A heatmap showing correlation values between all numerical features and the target variables.
      
      Interpretation:
      
      Tenure has extremely weak correlations (between –0.03 and +0.07) with almost every feature.
      
      Features like Support Calls, Payment Delay, and Engagement Score show stronger correlations with Churn, not Tenure.
      
      Very few linear relationships exist overall.
      
      Why it matters:
      This explains why regression models for Tenure performed poorly (low R² score).
      
      6. KDE Plots of Numerical Columns Against Churn
      
      Example:
      
      Age vs Churn
      
      Usage Frequency vs Churn
      
      Support Calls vs Churn
      
      Interpretation:
      
      KDE curves for churned vs non-churned customers show visible separation for some features.
      
      This indicates some features behave differently for churners, improving classification models.
      
      Why it matters:
      Confirms that the dataset is more suitable for churn prediction than tenure estimation.
      
      7. Box Plots for Numerical Columns
      
      Plotted for:
      
      Age
      
      Usage Frequency
      
      Support Calls
      
      Interpretation:
      
      Helps identify outliers and spread.
      
      Support Calls has visible outliers (customers with exceptionally high call counts).
      
      Variability in Usage Frequency suggests different usage patterns across customers.
      
      Why it matters:
      Outliers can influence models; understanding spread is key for preprocessing.
      
      8. KDE Plot of Engagement Score
      
      What it shows:
      Distribution of the engineered Engagement Score.
      
      Interpretation:
      
      The score ranges widely, centered around moderate values.

Outliers on both negative and positive sides show high variability in engagement.

Why it matters:
Checks if the engineered feature has meaningful variation for prediction.

9. KDE Plot of Risk Score

What it shows:
Distribution of the engineered Risk Score.

Interpretation:

Strong right skew due to high Payment Delay + Support Calls for some customers.

Many customers have low or moderate risk.

Why it matters:
Helps in identifying high-risk behavioral patterns related to churn.

10. Subscription Type vs Churn (Bar Plot)

What it shows:
Comparison of churn rates across subscription types (Basic, Standard, Premium, etc.).

Interpretation:

Certain subscription categories may have higher churn.

Shows customer dissatisfaction differences between plans.

Why it matters:
Guides business actions such as improving weaker subscription plans.

Reason for the Low R² Score in Tenure Prediction

The regression models produced a low R² score(0.0074), and this is consistent with EDA findings:

1. Weak Correlation Between Features and Tenure

The correlations between numerical features and Tenure ranged roughly between –0.03 and +0.07.
Such weak relationships limit any model’s ability to explain variance in Tenure.

2. Features Are More Predictive of Churn Than Tenure

Behavioral attributes (e.g., support calls, delays, spending patterns) influence customer dissatisfaction and churn, not how long they have already stayed.
Thus the dataset is naturally structured for classification, not regression.

3. Missing Important Factors for Tenure

Tenure typically depends on information not present in the dataset, such as:

Customer start date

Offer history

Service lifecycle stage

Retention interventions

The absence of these variables restricts model performance.

4. High Noise in Inputs

Behavioral features show high variance without a direct linear trend with Tenure, further lowering predictive accuracy.

Conclusion:
The dataset provides meaningful signals for churn classification, but insufficient information to accurately model tenure, resulting in a low R² score.

==================
## Regression analysis using feature engineered features:(main.py)
 The biggest challenge we encountered using the given features predicting the tenure for which the customer will stay with the company was that the tenure target variable was showing very less correlation with the feature variables which indicates that the tenure of a customer was largely independent of the feature variables and mostly random. The R2 score for this analysis was around 0.0027
 To solve this, we engineered some other features which are related to other features but can increase the correlation with the target variable. We analyses 2 approaches
 - The engineered features which depended on the target variable itself, this lead to R2 score of 1 which meant perfect prediction but this was obviously due to data leakage and the model was "cheating".
 - The engineered features which did'nt depend on target variable and this gave us a R2 score of 0.0042,
 a slight increase.
 - The eda and the training part was similar to that of EDA.ipynb


## Classification analysis

We also tried to predict whether the customer would churn or not using ANN classification analysis. The data preprocessing was done based on the ideation file. The neural network parameters summary is as follows:
model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ layer1 (Dense)                  │ (None, 64)             │           832 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ layer2 (Dense)                  │ (None, 32)             │         2,080 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ layer3 (Dense)                  │ (None, 1)              │            33 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 2,945 (11.50 KB)
 Trainable params: 2,945 (11.50 KB)
 Non-trainable params: 0 (0.00 B)
 
 Then the model was hosted on streamlit.
![alt text](image-2.png)

============================
Web Display description using react and fastapi

W# Backend README (Flask + XGBoost)

## Overview
This backend exposes REST API endpoints to predict customer tenure and churn using trained XGBoost ML models.

## Features
- Accepts JSON input from frontend
- Performs feature engineering
- Arranges features in correct order for the model
- Returns predictions as JSON
- CORS enabled for frontend communication

## Tech Stack
- Python 3
- Flask
- NumPy
- XGBoost
- Pickle (for model loading)
- Flask-CORS

## How to Run
```bash
cd backend
python app.py
```

Server runs at:
```
http://127.0.0.1:5000
```

## API Endpoints
### ✔ `GET /`
Returns backend health message.

### ✔ `POST /predict`
Accepts customer data and returns:
```json
{
  "tenure_prediction": 12
}
```

### ✔ `POST /predict_churn` (if added)
Returns:
```json
{
  "churn_prediction": 1
}
```

## Folder Structure
```
backend/
  ├── app.py
  ├── model/
  │    └── xgb_model.pkl
```

## Requirements
Install dependencies:
```bash
pip install flask flask-cors numpy xgboost
```

# Frontend README (React + TailwindCSS)

## Overview
This frontend is built using React and TailwindCSS. It provides a clean UI for predicting customer tenure and churn by sending user inputs to a Flask backend.

## Features
- User-friendly form inputs
- Encodes form data for ML model
- API communication using Fetch
- Displays prediction in a styled UI card

## Tech Stack
- React.js
- Vite
- TailwindCSS
- JavaScript Fetch API

## How to Run
```bash
cd my-react-app
npm install
npm run dev
```

App runs at:
```
http://localhost:5173
```

## Folder Structure
```
my-react-app/
  └── src/
      ├── components/
      │   └── Home.jsx
      ├── App.jsx
      ├── main.jsx
```

## Environment Requirements
- Node.js 16+  
- npm or yarn  

## API Endpoints Used
- `GET /` → Check backend health  
- `POST /predict` → Predict tenure  
- `POST /predict_churn` (if added) → Predict churn  


![WhatsApp Image 2025-12-12 at 20 04 31_3d666a10](https://github.com/user-attachments/assets/206cdbf3-d3b5-454e-8e42-12ac761c8bcb)
![WhatsApp Image 2025-12-12 at 20 04 31_194febe1](https://github.com/user-attachments/assets/a1c3804f-c603-4d4c-b46d-caa06a7410b5)
