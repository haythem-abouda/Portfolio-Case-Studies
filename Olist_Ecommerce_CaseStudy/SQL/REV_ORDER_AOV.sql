SELECT 
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
    COUNT(o.order_id) AS total_orders,
    SUM(p.payment_value) AS total_revenue,
    SUM(p.payment_value) / COUNT(o.order_id) AS aov
FROM orders AS o
JOIN order_payments AS p ON o.order_id = p.order_id
WHERE order_purchase_timestamp >= '2017-01-01'
  AND order_purchase_timestamp < '2018-09-01'
GROUP BY year, month
ORDER BY year, month;