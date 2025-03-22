SELECT 
    contract,  -- Group by contract type
    COUNT(*) AS total_customers,  -- Count total customers
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned_customers,  -- Count churned customers
    ROUND(100.0 * COUNT(CASE WHEN churn = 'Yes' THEN 1 END) / COUNT(*), 2) AS churn_rate  -- Calculate churn rate
FROM telco_churn
GROUP BY contract
ORDER BY churn_rate DESC;  -- Sort from highest to lowest churn
