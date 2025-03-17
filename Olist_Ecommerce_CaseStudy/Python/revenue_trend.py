import pandas as pd

# Query to fetch revenue trends
query = """
SELECT 
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
    SUM(payment_value) AS total_revenue
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
WHERE order_purchase_timestamp >= '2017-01-01'
  AND order_purchase_timestamp < '2018-09-01'
GROUP BY year, month
ORDER BY year, month;
"""

# Run query and load into a DataFrame
df_revenue = pd.read_sql(query, engine)

df_revenue['year'] = df_revenue['year'].astype(int)  # Convert year to integer
df_revenue['month'] = df_revenue['month'].astype(int)  # Convert month to integer

# Show the first few rows to confirm
df_revenue.head()

----

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick  # Add this at the top

import os

# Convert year & month into a single date column
df_revenue['date'] = pd.to_datetime(df_revenue['year'].astype(str) + '-' + df_revenue['month'].astype(str) + '-01')

# Drop the separate year and month columns
df_revenue = df_revenue.drop(columns=['year', 'month'])

# Ensure the 'plots' folder exists
os.makedirs("plots", exist_ok=True)

# Create the plot
plt.figure(figsize=(12,6))
plt.plot(df_revenue['date'], df_revenue['total_revenue'], marker='o', linestyle='-', color='green')
plt.xlabel('Date')
plt.ylabel('Total Revenue (Millions)')
plt.title('Monthly Revenue Trend (Jan 2017 - Aug 2018)')
plt.xticks(rotation=45)
plt.grid()

# Format y-axis to show in millions
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

# Save and show the plot
plt.savefig("plots/revenue_trend.png", bbox_inches='tight', dpi=300)
plt.show()
