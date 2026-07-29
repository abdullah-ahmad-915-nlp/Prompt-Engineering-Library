```sql
SELECT 
    customers.customer_name,
    orders.order_date,
    orders.total_amount
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE orders.order_date > '2025-01-01'
ORDER BY orders.order_date ASC;
```