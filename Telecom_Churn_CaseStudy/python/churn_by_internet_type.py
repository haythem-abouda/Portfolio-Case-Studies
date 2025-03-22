# Set figure size
plt.figure(figsize=(8,5))

# Create a countplot showing churn by internet service type
sns.countplot(x=df['internet_service'], hue=df['churn'], palette="viridis")

# Add title and labels
plt.title("Churn by Internet Service Type")  # Chart title
plt.xlabel("Internet Service Type")  # X-axis label
plt.ylabel("Customer Count")  # Y-axis label

# Add legend (explains which color represents churned/stayed customers)
plt.legend(title="Churn", labels=["Stayed", "Churned"])

# Show the plot
plt.show()