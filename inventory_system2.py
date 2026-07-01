import pandas as pd
import numpy as np
from xgboost import XGBRegressor

# 1. Load the 3-year dataset
df = pd.read_excel("retail_3_years_dataset.xlsx")

# 2. Re-prepare features for the trained model
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['Day_of_Week'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month
df['Is_Weekend'] = df['Day_Type'].apply(lambda x: 1 if x in ['Saturday', 'Sunday'] else 0)

X = df[['Day_of_Week', 'Month', 'Is_Weekend', 'Current_Stock']]
y = df['Unit_sold']

# 3. Train the XGBoost Model to get active predictions
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb_model.fit(X, y)

# 4. INVENTORY OPTIMIZATION LOGIC
print("🔄 Running Automated Inventory Optimization System...")

# Step A: Predict demand for the entire dataset using our model
df['XGB_Predicted_Demand'] = xgb_model.predict(X).astype(int)

# Step B: Calculate Safety Stock (Buffer) 
df['Safety_Stock_Level'] = (df['XGB_Predicted_Demand'] * 1.2).astype(int)

# Step C: Automated Reorder Trigger Logic
df['Reorder_Status'] = np.where(df['Current_Stock'] < df['Safety_Stock_Level'], 'TRIGGER REORDER', 'STOCK SUFFICIENT')

# Step D: Calculate Suggested Reorder Quantity
df['Suggested_Reorder_Qty'] = np.where(
    df['Reorder_Status'] == 'TRIGGER REORDER', 
    (df['Safety_Stock_Level'] * 2) - df['Current_Stock'], 
    0
)
df['Suggested_Reorder_Qty'] = df['Suggested_Reorder_Qty'].clip(lower=0).astype(int)

# 5. Save the finalized Inventory Report to a new Excel file
df.to_excel("final_inventory_optimization_report.xlsx", index=False)

print("\n🎉 SUCCESS: 'final_inventory_optimization_report.xlsx' has been created!")
print("This file contains Automated Reorder Suggestions for your Power BI dashboard.")