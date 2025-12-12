
import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================
# STEP 1: LOAD DATA FROM DATABASE
# ============================================
print("Loading data from database...")
conn = sqlite3.connect(r'C:\Users\athan\Downloads\hackathon.db')
df = pd.read_sql("SELECT * FROM customer_churn_train", conn)  # CHANGE 'your_table_name' to actual name
conn.close()

print(f"Original data shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())

#
# ============================================
# STEP 2: FEATURE ENGINEERING
# ============================================
print("\n" + "="*50)
print("STEP 3: Feature Engineering")
print("="*50)

# Engagement metrics
df['engagement_score'] = df['Usage Frequency'] * df['Total Spend']


# Customer quality indicators
df['spend_per_call'] = df['Total Spend'] / (df['Support Calls'] + 1)
df['reliable_payer'] = (df['Payment Delay'] < df['Payment Delay'].quantile(0.25)).astype(int)
df['high_value_customer'] = ((df['Total Spend'] > df['Total Spend'].median()) & 
                              (df['Support Calls'] < df['Support Calls'].median())).astype(int)

# Age-based features
df['mature_customer'] = (df['Age'] > 50).astype(int)
df['age_spend_interaction'] = df['Age'] * df['Total Spend']
df['age_usage_ratio'] = df['Age'] / (df['Usage Frequency'] + 1)

# Ratios and combinations
df['spend_to_frequency'] = df['Total Spend'] / (df['Usage Frequency'] + 1)
df['satisfaction_proxy'] = df['Total Spend'] / (df['Support Calls'] + 1)
df['frequency_age_ratio'] = df['Usage Frequency'] / (df['Age'] + 1)
df['delay_interaction_ratio'] = df['Payment Delay'] / (df['Last Interaction'] + 1)

# Polynomial features for non-linearity
df['age_squared'] = df['Age'] ** 2
df['support_calls_squared'] = df['Support Calls'] ** 2
df['total_spend_squared'] = df['Total Spend'] ** 2
df['usage_frequency_squared'] = df['Usage Frequency'] ** 2

# Binary flags
df['has_payment_delay'] = (df['Payment Delay'] > 0).astype(int)
df['frequent_support'] = (df['Support Calls'] > df['Support Calls'].median()).astype(int)
df['low_spender'] = (df['Total Spend'] < df['Total Spend'].quantile(0.25)).astype(int)
df['high_spender'] = (df['Total Spend'] > df['Total Spend'].quantile(0.75)).astype(int)

# Interaction features
df['age_payment_interaction'] = df['Age'] * df['Payment Delay']
df['spend_frequency_interaction'] = df['Total Spend'] * df['Usage Frequency']
df['calls_delay_interaction'] = df['Support Calls'] * df['Payment Delay']

print(f"Created {len(df.columns) - len(numeric_cols)} new features")
print(f"Total features now: {len(df.columns)}")

# Handle any inf or nan values created during feature engineering
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(df.median(numeric_only=True))

# ============================================
# STEP 3: PREPARE DATA FOR MODELING
# ============================================
print("\n" + "="*50)
print("STEP 4: Preparing Data for Modeling")
print("="*50)

# Separate features and target
X = df.drop(['Tenure'], axis=1)
y = df['Tenure']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"\nTarget statistics:")
print(y.describe())

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Features scaled using StandardScaler")

# ============================================
# STEP 4: MODEL TRAINING & EVALUATION
# ============================================
print("\n" + "="*50)
print("STEP 5: Model Training & Evaluation")
print("="*50)

results = {}

# 1. Random Forest
print("\n1. Training Random Forest...")
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)

rf_r2 = r2_score(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_mae = mean_absolute_error(y_test, rf_pred)

results['Random Forest'] = {'R²': rf_r2, 'RMSE': rf_rmse, 'MAE': rf_mae}
print(f"   R² Score: {rf_r2:.4f}")
print(f"   RMSE: {rf_rmse:.4f}")
print(f"   MAE: {rf_mae:.4f}")

# 2. Gradient Boosting
print("\n2. Training Gradient Boosting...")
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
gb_model.fit(X_train_scaled, y_train)
gb_pred = gb_model.predict(X_test_scaled)

gb_r2 = r2_score(y_test, gb_pred)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_mae = mean_absolute_error(y_test, gb_pred)

results['Gradient Boosting'] = {'R²': gb_r2, 'RMSE': gb_rmse, 'MAE': gb_mae}
print(f"   R² Score: {gb_r2:.4f}")
print(f"   RMSE: {gb_rmse:.4f}")
print(f"   MAE: {gb_mae:.4f}")

# 3. XGBoost
print("\n3. Training XGBoost...")
xgb_model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    random_state=42
)
xgb_model.fit(X_train_scaled, y_train)
xgb_pred = xgb_model.predict(X_test_scaled)

xgb_r2 = r2_score(y_test, xgb_pred)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
xgb_mae = mean_absolute_error(y_test, xgb_pred)

results['XGBoost'] = {'R²': xgb_r2, 'RMSE': xgb_rmse, 'MAE': xgb_mae}
print(f"   R² Score: {xgb_r2:.4f}")
print(f"   RMSE: {xgb_rmse:.4f}")
print(f"   MAE: {xgb_mae:.4f}")

# ============================================
# STEP 5: RESULTS SUMMARY
# ============================================
print("\n" + "="*50)
print("RESULTS SUMMARY")
print("="*50)

results_df = pd.DataFrame(results).T
print(results_df)

best_model = results_df['R²'].idxmax()
print(f"\nBest Model: {best_model}")
print(f"Best R² Score: {results_df.loc[best_model, 'R²']:.4f}")

# ============================================
# STEP 6: FEATURE IMPORTANCE
# ============================================
print("\n" + "="*50)
print("TOP 15 MOST IMPORTANT FEATURES")
print("="*50)

# Use the best performing model for feature importance
if best_model == 'Random Forest':
    best_model_obj = rf_model
elif best_model == 'Gradient Boosting':
    best_model_obj = gb_model
else:
    best_model_obj = xgb_model

importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': best_model_obj.feature_importances_
}).sort_values('Importance', ascending=False)

print(importance_df.head(15))

# ============================================
# STEP 7: SAVE RESULTS
# ============================================
print("\n" + "="*50)
print("SAVING RESULTS")
print("="*50)

# Save feature importance
importance_df.to_csv('feature_importance.csv', index=False)
print("Feature importance saved to: feature_importance.csv")

# Save predictions
predictions_df = pd.DataFrame({
    'Actual_Tenure': y_test,
    'Predicted_Tenure': xgb_pred,
    'Difference': y_test - xgb_pred
})
predictions_df.to_csv('predictions.csv', index=False)
print("Predictions saved to: predictions.csv")

# Save cleaned and engineered data back to database
conn = sqlite3.connect(r'C:\Users\athan\Downloads\hackathon.db')
df.to_sql('processed_data', conn, if_exists='replace', index=False)
conn.close()
print("Processed data saved to database as 'processed_data' table")

print("\n" + "="*50)
print("COMPLETE!")
print("="*50)