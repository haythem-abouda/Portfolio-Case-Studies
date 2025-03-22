# Set figure size
plt.figure(figsize=(8,5))

# Countplot of churn by tech support availability
sns.countplot(x=df['tech_support'], hue=df['churn'], palette="viridis")

# Add title and labels
plt.title("Churn by Tech Support Usage")  # Chart title
plt.xlabel("Tech Support")  # X-axis label
plt.ylabel("Customer Count")  # Y-axis label

# Add legend
plt.legend(title="Churn", labels=["Stayed", "Churned"])

# Show the plot
plt.show()
