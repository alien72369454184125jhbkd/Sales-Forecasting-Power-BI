import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load your newly generated 3-year data
df = pd.read_excel("retail_3_years_dataset.xlsx")

# 2. Feature Engineering: Convert Date text into numeric features
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['Day_of_Week'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month

# Match the exact 'Saturday' and 'Sunday' values from your Excel sheet
df['Is_Weekend'] = df['Day_Type'].apply(lambda x: 1 if x in ['Saturday', 'Sunday'] else 0)

# 3. Define Features (X) and Target (y)
X = df[['Day_of_Week', 'Month', 'Is_Weekend', 'Current_Stock']]
y = df['Unit_sold']

# 4. Split data into Training (80%) and Testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🔄 Training Regression and Ensemble models on 3 years of data...")

# 5. Train a baseline Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)
print(f"✅ Linear Regression Error (MAE): {mean_absolute_error(y_test, lr_preds):.2f} units")

# 6. Train an Ensemble Learning Model (XGBoost)
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)
xgb_r2 = r2_score(y_test, xgb_preds) * 100

print(f"✅ XGBoost Regression Error (MAE): {mean_absolute_error(y_test, xgb_preds):.2f} units")
print(f"✅ XGBoost Model Accuracy (R² Score): {xgb_r2:.2f}%")

# 7. Predict demand for a sample upcoming day using XGBoost
sample_features = pd.DataFrame([[0, 6, 0, 300]], columns=['Day_of_Week', 'Month', 'Is_Weekend', 'Current_Stock'])
predicted_sales = xgb_model.predict(sample_features)
print(f"\n🔮 Predicted sales for a sample day using XGBoost: {int(predicted_sales[0])} units")