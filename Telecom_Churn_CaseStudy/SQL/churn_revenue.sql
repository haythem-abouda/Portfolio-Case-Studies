SELECT 
    SUM(monthly_charges) AS total_revenue,
    SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE NULL END) AS lost_revenue,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE NULL END) / SUM(monthly_charges), 2) AS revenue_loss_percent
FROM telco_churn;
