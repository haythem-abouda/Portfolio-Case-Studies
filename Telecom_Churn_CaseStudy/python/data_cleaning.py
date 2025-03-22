import pandas as pd
from sqlalchemy import create_engine

#  1. Connect to PostgreSQL
engine = create_engine("postgresql://your_username:your_password@localhost:5432/telco_churn_db")

#  2. Load Data from PostgreSQL
query = "SELECT * FROM telco_churn;"
df = pd.read_sql(query, engine)

#  3. Fix Data Types & Missing Values
df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')  # Convert to float
df['total_charges'].fillna(0, inplace=True)  # Replace missing values with 0

#  4. Convert Yes/No Columns to 1/0
yes_no_cols = ['partner', 'dependents', 'phone_service', 'paperless_billing', 'churn']
for col in yes_no_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 0})

#  5. Check Final Data
print(df.info())  # Check data types
print(df.isnull().sum())  # Confirm no missing values

# 6. Save Cleaned Data to CSV (Optional)
df.to_csv("cleaned_telco_churn.csv", index=False)

print("✅ Data cleaning complete! Dataset is ready for analysis.")
