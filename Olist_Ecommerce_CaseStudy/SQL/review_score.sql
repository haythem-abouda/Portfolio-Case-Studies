SELECT 
    review_score, 
    COUNT(review_id) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score DESC;