SELECT 
    payment_type, 
    COUNT(order_id) AS total_orders,
    SUM(payment_value) AS total_revenue,
    AVG(payment_value) AS avg_order_value
FROM order_payments
WHERE order_id IN (
    SELECT order_id FROM orders
    WHERE order_purchase_timestamp >= '2017-01-01'
    AND order_purchase_timestamp < '2018-09-01'
)
GROUP BY payment_type
ORDER BY total_orders DESC;