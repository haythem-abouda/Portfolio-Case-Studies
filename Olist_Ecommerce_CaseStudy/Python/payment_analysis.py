
# Extract values from DataFrame
payment_types = df_payment_type["payment_type"].tolist()
total_orders = df_payment_type["total_orders"].tolist()
total_revenue = df_payment_type["total_revenue"].tolist()
aov = df_payment_type["avg_order_value"].tolist()

import matplotlib.pyplot as plt
import os

# Ensure the 'plots' folder exists
os.makedirs("plots", exist_ok=True)

# Create figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart for total orders per payment type
axes[0].bar(payment_types, total_orders, color='blue', alpha=0.7)
axes[0].set_title("Total Orders by Payment Type")
axes[0].set_xlabel("Payment Type")
axes[0].set_ylabel("Total Orders")
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Bar chart for AOV per payment type
axes[1].bar(payment_types, aov, color='green', alpha=0.7)
axes[1].set_title("Average Order Value (AOV) by Payment Type")
axes[1].set_xlabel("Payment Type")
axes[1].set_ylabel("AOV (€)")
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

# Save and show the plot
plt.tight_layout()
plt.savefig("plots/payment_analysis.png", bbox_inches='tight', dpi=300)
plt.show()
