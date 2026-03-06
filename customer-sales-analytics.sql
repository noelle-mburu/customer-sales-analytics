CREATE SCHEMA olist;

-- Change data format of date columns
ALTER TABLE olist.orders
    ALTER COLUMN order_approved_at TYPE timestamp 
    USING order_approved_at::timestamp;

ALTER TABLE olist.orders
    ALTER COLUMN order_delivered_carrier_date TYPE timestamp 
    USING order_delivered_carrier_date::timestamp;

ALTER TABLE olist.orders
    ALTER COLUMN order_delivered_customer_date TYPE timestamp 
    USING order_delivered_customer_date::timestamp;

ALTER TABLE olist.orders
    ALTER COLUMN order_estimated_delivery_date TYPE timestamp 
    USING order_estimated_delivery_date::timestamp;

ALTER TABLE olist.order_items
    ALTER COLUMN shipping_limit_date TYPE timestamp 
    USING shipping_limit_date::timestamp;

SELECT column_name, data_type 
FROM information_schema.columns
WHERE table_name = 'orders'
AND table_schema = 'olist';

SELECT column_name, data_type 
FROM information_schema.columns
WHERE table_name = 'order_items'
AND table_schema = 'olist';

-- 1. Revenue & Sales - What is the total revenue? How does it trend month by month?
select 
	DATE_TRUNC('month', o.order_purchase_timestamp) as Month,
	ROUND(SUM(op.payment_value)::numeric, 2) as Total_revenue
from olist.orders o 
inner join olist.order_payments op ON o.order_id = op.order_id
group by DATE_TRUNC('month', o.order_purchase_timestamp)
order by Month;

-- 2. Products — Which product categories generate the most revenue?
select * from olist.category_translation ct;
select * from olist.products;
select * from olist.order_items;

select
	ct.product_category_name_english,
	ROUND(sum(oi.price)::numeric, 2) as total_product_revenue
from olist.order_items oi
inner join olist.products p on oi.product_id = p.product_id
inner join olist. category_translation ct on p.product_category_name = ct.product_category_name
group by ct.product_category_name_english
order by total_product_revenue desc
limit 10;
	
-- 3. Customers — Which states have the most customers?
select * from customers c;

select
	c.customer_state,
	COUNT(c.customer_state) as total_customers_per_state
from olist.customers c
group by c.customer_state
order by total_customers_per_state desc
limit 10;

-- 1. Sellers — Who are the top performing sellers?
select * from sellers;
select * from order_items;

select
	s.seller_id,
	s.seller_city,
	s.seller_state,
	ROUND(SUM(oi.price):: numeric, 2) as total_revenue_per_seller
from olist.sellers s 
inner join olist.order_items oi on s.seller_id = oi.seller_id 
group by s.seller_id, s.seller_city, s.seller_state
order by total_revenue_per_seller desc
limit 10;

-- 5. Delivery — What is the average delivery time? Are orders being delivered on time?
select * from orders o;

select 
	ROUND(AVG(DATE_PART('day',o.order_delivered_customer_date - o.order_purchase_timestamp))::numeric,1) as average_delivery_days
from olist.orders o
where o.order_status = 'delivered';

-- 6. Payments — What payment methods do customers prefer?
select * from order_payments;
select * from order_items;

select
	op.payment_type,
	COUNT(op.payment_type) as total_payments_per_type,
	ROUND(COUNT(op.payment_type) * 100.0 /(select COUNT(*) from olist.order_payments)::numeric,1) as percentage_payments
from olist.order_payments op 
group by op.payment_type
order by total_payments_per_type desc;

--7. Reviews — What is the average review score by product category?
select * from order_reviews r;
select * from products;
sele

