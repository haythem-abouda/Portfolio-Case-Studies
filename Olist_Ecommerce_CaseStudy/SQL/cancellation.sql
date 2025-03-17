SELECT 
    p.payment_type, 
    COUNT(o.order_id) AS total_canceled_orders,
    SUM(p.payment_value) AS total_revenue_lost,
    total_orders.total_orders,  -- Join total orders
    ROUND((COUNT(o.order_id) * 100.0) / total_orders.total_orders, 2) AS cancellation_rate
FROM order_payments AS p  
JOIN orders AS o  
    ON o.order_id = p.order_id  
JOIN (
    -- Subquery to calculate total orders per payment type
    SELECT 
        payment_type, 
        COUNT(order_id) AS total_orders
    FROM order_payments
    WHERE order_id IN (
        SELECT order_id FROM orders
        WHERE order_purchase_timestamp >= '2017-01-01'
        AND order_purchase_timestamp < '2018-09-01'
    )
    GROUP BY payment_type
) AS total_orders
ON total_orders.payment_type = p.payment_type
WHERE o.order_status = 'canceled'  
GROUP BY p.payment_type, total_orders.total_orders
ORDER BY total_canceled_orders DESC;