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