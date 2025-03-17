import pandas as pd

# Query to fetch revenue trends
query = """
SELECT 
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
    COUNT(o.order_id) AS total_orders,
    SUM(p.payment_value) AS total_revenue,
    SUM(p.payment_value) / COUNT(o.order_id) AS aov
FROM orders AS o
JOIN order_payments AS p ON o.order_id = p.order_id
WHERE order_purchase_timestamp >= '2017-01-01'
  AND order_purchase_timestamp < '2018-09-01'
GROUP BY year, month
ORDER BY year, month;

"""

# Run query and load into a DataFrame
df_orders_revenue = pd.read_sql(query, engine)

df_orders_revenue['year'] = df_orders_revenue['year'].astype(int)  # Convert year to integer
df_orders_revenue['month'] = df_orders_revenue['month'].astype(int)  # Convert month to integer

# Show the first few rows to confirm
df_revenue.head()

----

import matplotlib.pyplot as plt
import os

# Ensure the 'plots' folder exists
os.makedirs("plots", exist_ok=True)

# Create subplots with 3 rows, 1 column
fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

# --- 1️⃣ Total Orders ---
axes[0].plot(df_orders_revenue['date'], df_orders_revenue['total_orders'], 
             marker='o', linestyle='-', color='blue')
axes[0].set_ylabel("Total Orders")
axes[0].set_title("Monthly Total Orders (Jan 2017 - Aug 2018)")
axes[0].grid(True)

# --- 2️⃣ Total Revenue ---
axes[1].plot(df_orders_revenue['date'], df_orders_revenue['total_revenue'], 
             marker='s', linestyle='-', color='green')
axes[1].set_ylabel("Total Revenue (Millions)")
axes[1].set_title("Monthly Total Revenue (Jan 2017 - Aug 2018)")
axes[1].grid(True)

# --- 3️⃣ AOV ---
axes[2].plot(df_orders_revenue['date'], df_orders_revenue['aov'], 
             marker='D', linestyle='--', color='red')
axes[2].set_ylim(50, max(df_orders_revenue['aov']) * 1.1)  # Adjust Y-axis to start at 50

axes[2].set_ylabel("AOV (Avg Order Value)")
axes[2].set_title("Monthly AOV (Jan 2017 - Aug 2018)")
axes[2].grid(True)

# Rotate x-axis labels for clarity
plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig("plots/orders_revenue_aov_separate.png", bbox_inches='tight', dpi=300)

# Show the plots
plt.show()
