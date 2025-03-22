SELECT 
    CASE 
        WHEN tenure = 6 THEN '0-6 months'
        WHEN tenure BETWEEN 7 AND 24 THEN '7-24 months'
        WHEN tenure BETWEEN 25 AND 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_group,
    COUNT() AS total_customers,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 ELSE NULL END) AS churned_customers, -- FIXED!
    ROUND(100.0  COUNT(CASE WHEN churn = 'Yes' THEN 1 ELSE NULL END)  COUNT(), 2) AS churn_rate -- FIXED!
FROM telco_churn
GROUP BY tenure_group
ORDER BY churn_rate DESC;
