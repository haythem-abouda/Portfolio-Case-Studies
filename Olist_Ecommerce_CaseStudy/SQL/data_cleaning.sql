-- STEP 1: REMOVE INVALID ORDER DATES
DELETE FROM orders
WHERE order_purchase_timestamp < '2017-01-01' 
   OR order_purchase_timestamp >= '2018-09-01';

-- STEP 2: REMOVE DUPLICATE REVIEWS (KEEP LATEST)
DELETE FROM order_reviews
WHERE review_creation_date IN (
    SELECT review_creation_date
    FROM (
        SELECT order_id, review_creation_date, 
               ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_creation_date DESC) AS row_num
        FROM order_reviews
    ) subquery
    WHERE row_num > 1
);

-- STEP 3: REMOVE PAYMENTS WITH 0 VALUE
DELETE FROM order_payments
WHERE payment_value = 0;

-- STEP 4: REMOVE ORDERS WITH NULL DELIVERY DATES
DELETE FROM orders
WHERE order_delivered_customer_date IS NULL;

-- STEP 5: REMOVE LAST FAULTY ROW IN REVIEWS (if applicable)
DELETE FROM order_reviews
WHERE review_id IN (SELECT review_id FROM order_reviews ORDER BY review_id DESC LIMIT 1);
