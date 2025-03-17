import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import text


# Ensure the 'plots' folder exists
os.makedirs("plots", exist_ok=True)

# SQL Query to fetch review themes
query = """
SELECT 
    CASE 
        WHEN review_comment_message ILIKE ANY (ARRAY['%produto%', '%veio%', '%nada%', '%apenas%']) 
        THEN 'Product Issues'
        WHEN review_comment_message ILIKE ANY (ARRAY['%entrega%', '%entregue%', '%prazo%', '%chegou%', '%ainda%']) 
        THEN 'Delivery Issues'
        WHEN review_comment_message ILIKE ANY (ARRAY['%pedido%', '%compra%', '%loja%']) 
        THEN 'Order Process Issues'
        WHEN review_comment_message ILIKE ANY (ARRAY['%quero%', '%agora%']) 
        THEN 'Customer Support Issues'
        ELSE 'Other'
    END AS review_theme,
    COUNT(*) AS total_reviews,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM order_reviews WHERE review_score = 1), 2) AS percentage
FROM order_reviews
WHERE review_score = 1
GROUP BY review_theme
ORDER BY total_reviews DESC;
"""

# Run query and load into a DataFrame
df_reviews = pd.read_sql(text(query), con=engine)

# Plot the results
plt.figure(figsize=(10, 5))
plt.barh(df_reviews['review_theme'], df_reviews['percentage'], color=['red', 'orange', 'blue', 'green', 'purple'])
plt.xlabel("Percentage of 1-Star Reviews (%)")
plt.ylabel("Review Theme")
plt.title("Top Complaints in 1-Star Reviews")
plt.gca().invert_yaxis()  # Invert for better readability
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Save the plot
plt.savefig("plots/review_issues.png", bbox_inches='tight', dpi=300)
plt.show()
