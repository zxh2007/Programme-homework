-- Week3 04（选做）：GROUP BY 统计
-- 前提：已执行 01_schema.sql、02_seed.sql

USE bookshop;

-- 每位作者几本书、平均价
SELECT a.name, COUNT(*) AS book_count, ROUND(AVG(b.price), 2) AS avg_price
FROM authors AS a
JOIN books AS b ON b.author_id = a.id
GROUP BY a.id, a.name
ORDER BY book_count DESC, a.id;
