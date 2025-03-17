import pandas as pd
import matplotlib.pyplot as plt
import os

# Query to fetch cancellation data
query = """
SELECT 
    p.payment_type, 
    COUNT(o.order_id) AS total_canceled_orders,
    SUM(p.payment_value) AS total_revenue_lost,
    total_orders.total_orders,  -- Join total orders
    ROUND((COUNT(o.order_id) * 100.0) / total_orders.total_orders, 2) AS cancellation_rate
FROM order_payments AS p  
JOIN orders AS o  
    ON o.order_id = p.order_id  
JOIN (
    -- Subquery to calculate total orders per payment type
    SELECT 
        payment_type, 
        COUNT(order_id) AS total_orders
    FROM order_payments
    WHERE order_id IN (
        SELECT order_id FROM orders
        WHERE order_purchase_timestamp >= '2017-01-01'
        AND order_purchase_timestamp < '2018-09-01'
    )
    GROUP BY payment_type
) AS total_orders
ON total_orders.payment_type = p.payment_type
WHERE o.order_status = 'canceled'  
GROUP BY p.payment_type, total_orders.total_orders
ORDER BY total_canceled_orders DESC;
"""

# Run query and load into a DataFrame
df_canceled = pd.read_sql(query, engine)

# Remove the last row (assuming it's erroneous)
df_canceled = df_canceled.iloc[:-1]

# Ensure 'plots' directory exists
os.makedirs("plots", exist_ok=True)

## 🎨 **Plot 1: Cancellation Rate per Payment Type**
plt.figure(figsize=(10, 5))
plt.bar(df_canceled['payment_type'], df_canceled['cancellation_rate'], color='red', alpha=0.7)
plt.xlabel("Payment Type")
plt.ylabel("Cancellation Rate (%)")
plt.title("Cancellation Rate by Payment Method")
plt.ylim(0, max(df_canceled['cancellation_rate']) * 1.2)  # Adjust Y limit for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("plots/cancellation_rate.png", bbox_inches='tight', dpi=300)
plt.show()

## 💰 **Plot 2: Revenue Lost per Payment Type**
plt.figure(figsize=(10, 5))
plt.bar(df_canceled['payment_type'], df_canceled['total_revenue_lost'] / 1_000_000, color='blue', alpha=0.7)
plt.xlabel("Payment Type")
plt.ylabel("Revenue Lost (Millions)")
plt.title("Revenue Lost from Canceled Orders by Payment Method")
plt.ylim(0, max(df_canceled['total_revenue_lost'] / 1_000_000) * 1.2)  # Adjust Y limit for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("plots/revenue_lost.png", bbox_inches='tight', dpi=300)
plt.show()
