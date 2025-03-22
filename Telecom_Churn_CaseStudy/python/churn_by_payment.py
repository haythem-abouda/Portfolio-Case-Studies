# Set figure size
plt.figure(figsize=(8,5))

# Create a countplot for churn based on payment method
sns.countplot(x=df['payment_method'], hue=df['churn'], palette="viridis")

# Rotate x-axis labels for readability
plt.xticks(rotation=45)

# Add title and labels
plt.title("Churn by Payment Method")  # Chart title
plt.xlabel("Payment Method")  # X-axis label
plt.ylabel("Customer Count")  # Y-axis label

# Add legend
plt.legend(title="Churn", labels=["Stayed", "Churned"])

# Show the plot
plt.show()
