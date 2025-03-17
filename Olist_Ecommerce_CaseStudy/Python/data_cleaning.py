import pandas as pd
import numpy as np

# Load datasets
df_orders = pd.read_csv("olist_orders_dataset.csv")
df_order_reviews = pd.read_csv("olist_order_reviews_dataset.csv")
df_order_payments = pd.read_csv("olist_order_payments_dataset.csv")

### --- STEP 1: HANDLE DUPLICATES IN REVIEWS --- ###
# Some customers submitted multiple reviews for the same order, keep only the latest review

df_order_reviews['review_creation_date'] = pd.to_datetime(df_order_reviews['review_creation_date'])
df_order_reviews = df_order_reviews.sort_values(by=['order_id', 'review_creation_date'], ascending=[True, False])
df_order_reviews = df_order_reviews.drop_duplicates(subset=['order_id'], keep='first')

### --- STEP 2: REMOVE FAULTY DATES FROM ORDERS --- ###
# Drop months with suspiciously low order counts
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
df_orders = df_orders[
    (df_orders['order_purchase_timestamp'] >= '2017-01-01') &
    (df_orders['order_purchase_timestamp'] < '2018-09-01')
]

### --- STEP 3: FIX PAYMENT DATASET ISSUES --- ###
# Remove invalid rows with 0 payments and fix payment_type inconsistencies
df_order_payments = df_order_payments[df_order_payments['payment_value'] > 0]
df_order_payments['payment_type'] = df_order_payments['payment_type'].str.lower().str.strip()

### --- STEP 4: FIX MISSING OR INVALID DELIVERY DATES --- ###
# Convert date columns
date_cols = ['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    df_orders[col] = pd.to_datetime(df_orders[col])

# Remove rows where delivery dates are completely missing
df_orders = df_orders.dropna(subset=['order_delivered_customer_date'])

# Create delay column
df_orders['delivery_delay'] = (df_orders['order_delivered_customer_date'] - df_orders['order_estimated_delivery_date']).dt.days
df_orders['delivery_delay'] = df_orders['delivery_delay'].fillna(0).astype(int)

### --- STEP 5: CLEAN REVIEW COMMENTS & REMOVE ERRORS --- ###
# Fill NaN values in review text columns with an empty string
df_order_reviews['review_comment_title'] = df_order_reviews['review_comment_title'].fillna('')
df_order_reviews['review_comment_message'] = df_order_reviews['review_comment_message'].fillna('')

# Remove last row from review dataset if it contains an error
df_order_reviews = df_order_reviews[:-1]  

### --- STEP 6: SAVE CLEANED FILES --- ###
df_orders.to_csv("cleaned_orders.csv", index=False)
df_order_reviews.to_csv("cleaned_order_reviews.csv", index=False)
df_order_payments.to_csv("cleaned_order_payments.csv", index=False)

print("✅ Data cleaning complete. Cleaned files saved!")
