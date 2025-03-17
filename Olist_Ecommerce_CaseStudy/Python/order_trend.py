import pandas as pd

# Query to fetch order trends
query = """
SELECT 
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
    COUNT(order_id) AS total_orders
FROM orders
WHERE order_purchase_timestamp >= '2017-01-01'
  AND order_purchase_timestamp < '2018-09-01' -- Stops at August 2018
GROUP BY year, month
ORDER BY year, month;
"""

# Run query and load into a DataFrame
df_orders = pd.read_sql(query, engine)

# Show the first few rows
df_orders

---------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_orders['year'] = df_orders['year'].astype(int)  # Convert year to integer
df_orders['month'] = df_orders['month'].astype(int)  # Convert month to integer

# Convert 'year' and 'month' into a single datetime column
df_orders['date'] = pd.to_datetime(df_orders['year'].astype(str) + '-' + df_orders['month'].astype(str) + '-01')

# Sort by date (important to ensure correct order)
df_orders = df_orders.sort_values('date')

# Set figure size
plt.figure(figsize=(12, 6))

# Plot line chart with correct x-axis
sns.lineplot(data=df_orders, x='date', y='total_orders', marker='o')

# Format labels
plt.xlabel("Time (Months)")
plt.ylabel("Total Orders")
plt.title("Order Growth Trend (Jan 2017 - Aug 2018)")

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Show the plot
plt.savefig("plots/order_trend.png", dpi=300, bbox_inches='tight')
plt.show()