# Query to analyze delivery performance per state
query = """
SELECT 
    c.customer_state,
    COUNT(o.order_id) AS total_orders,
    ROUND(AVG(EXTRACT(DAY FROM (o.order_estimated_delivery_date - o.order_delivered_customer_date))), 2) AS avg_delay_days
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY avg_delay_days DESC;
"""

# Load into DataFrame
df_delivery_delays = pd.read_sql(query, engine)

# Display first few rows
# df_delivery_delays.head()

import matplotlib.pyplot as plt

# Sort DataFrame for better visualization
df_delivery_delays = df_delivery_delays.sort_values(by="avg_delay_days", ascending=False)

# Plot
plt.figure(figsize=(12,6))
plt.bar(df_delivery_delays['customer_state'], df_delivery_delays['avg_delay_days'], color='steelblue')

# Labels & title
plt.xlabel('State')
plt.ylabel('Average Delay (Days)')
plt.title('Average Delivery Delays by State')
plt.xticks(rotation=45)

# Save & show
plt.savefig("plots/delivery_delays_by_state.png", bbox_inches='tight', dpi=300)
plt.show()

