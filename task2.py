import pandas as pd
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2023, 6, 1)
end_date = datetime(2026, 6, 1)
total_days = (end_date - start_date).days
np.random.seed(42)

products = [
    (101, "Wireless Mouse", 25), (102, "Mechanical Keyboard", 60), 
    (103, "Bluetooth Speaker", 45), (104, "Gaming Headset", 50),
    (105, "USB-C Hub", 30), (106, "1080p Webcam", 40), 
    (107, "Ergonomic Chair", 180), (108, "Desk Mat", 15),
    (109, "LED Desk Lamp", 28), (110, "External SSD 1TB", 95), 
    (111, "Laptop Stand", 35), (112, "HDMI Cable 6ft", 10),
    (113, "Wireless Charger", 22), (114, "Noise Cancelling Earbuds", 80), 
    (115, "Monitor Arm", 45), (116, "Smart Power Strip", 25),
    (117, "Microfiber Cloth", 8), (118, "Compressed Air", 12), 
    (119, "Graphic Tablet", 70), (120, "AA Batteries", 18)
]

rows = []
for i in range(total_days):
    current_date = start_date + timedelta(days=i)
    date_str = current_date.strftime("%d-%m-%Y")
    day_name = current_date.strftime("%A")
    month = current_date.month
    season_factor = 1.3 if month in [10, 11, 12] else 1.0
    
    if day_name in ["Saturday", "Sunday"]:
        day_type = day_name
        sales_baseline = int(np.random.randint(80, 96))
    else:
        day_type = "Weekday"
        sales_baseline = 45

    for prod_id, prod_name, base_price in products:
        product_variance = np.random.randint(-5, 10)
        unit_sold = int((sales_baseline + product_variance) * season_factor)
        unit_sold = max(5, unit_sold)
        unit_price = base_price + np.random.choice([-1, 0, 1])
        revenue = unit_sold * unit_price
        current_stock = int(np.random.randint(30, 550))
        
        rows.append([date_str, prod_id, prod_name, unit_sold, unit_price, revenue, current_stock, day_type])

columns = ["Date", "Product_ID", "Product_Name", "Unit_sold", "Unit_Price", "Revenue", "Current_Stock", "Day_Type"]
df = pd.DataFrame(rows, columns=columns)
df.to_excel("retail_3_years_dataset.xlsx", index=False)
print("--- SUCCESS: EXCEL FILE CREATED ---")