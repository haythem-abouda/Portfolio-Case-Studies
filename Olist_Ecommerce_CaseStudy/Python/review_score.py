import pandas as pd
import matplotlib.pyplot as plt
import os

# Query to fetch review score distribution
query = """
SELECT 
    review_score, 
    COUNT(review_id) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score DESC;
"""

# Run query and load into a DataFrame
df_reviews = pd.read_sql(query, engine)

# Ensure the 'plots' folder exists
os.makedirs("plots", exist_ok=True)

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(df_reviews['review_score'], df_reviews['total_reviews'], color='skyblue', edgecolor='black')

# Formatting
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")
plt.title("Distribution of Review Scores")
plt.xticks(df_reviews['review_score'])  # Ensures all review scores appear as x-axis labels
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot
plt.savefig("plots/review_score_distribution.png", bbox_inches='tight', dpi=300)

# Show the plot
plt.show()
