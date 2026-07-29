# SQL Generation Input

## Database schema:

Table: customers

Columns:
- customer_id (INTEGER)
- customer_name (VARCHAR)
- city (VARCHAR)

Table: orders

Columns:
- order_id (INTEGER)
- customer_id (INTEGER)
- order_date (DATE)
- total_amount (DECIMAL)

Relationship:
orders.customer_id = customers.customer_id

## User Request:
List the customer name, order date, and total amount for all orders placed after January 1, 2025. Sort the results by order date in ascending order.