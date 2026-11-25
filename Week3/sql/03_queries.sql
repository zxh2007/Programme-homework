-- Week3 03：六项 SQL 操作（查询 / 更新 / 删除 / 关联查询）
-- 前提：已执行 01_schema.sql、02_seed.sql

USE bookshop;

-- ③ 查询：只取需要的列，按 id 排序
SELECT id, title, price, stock
FROM books
ORDER BY id;

-- ③ 查询（条件一）：库存为 0 的书（种子数据里没有，结果应为空）
SELECT title, stock
FROM books
WHERE stock = 0;

-- ③ 查询（条件二）：价格在 20~40 元之间
SELECT title, price
FROM books
WHERE price BETWEEN 20 AND 40;

-- ④ 更新：卖出一本《三体》，库存减 1；stock > 0 防止减成负数
-- 种子数据里 id = 1 就是《三体》
UPDATE books
SET stock = stock - 1
WHERE id = 1 AND stock > 0;

SELECT id, title, stock
FROM books
WHERE id = 1;

-- ⑤ 删除：先插入一条临时记录，再按标题删掉
INSERT INTO books (title, author_id, price, stock)
VALUES ('删除演示专用临时书', (SELECT id FROM authors WHERE name = '刘慈欣'), 9.90, 1);

SELECT id, title
FROM books
WHERE title = '删除演示专用临时书';

DELETE FROM books
WHERE title = '删除演示专用临时书';

-- 删除后再查一次，结果应为空
SELECT id, title
FROM books
WHERE title = '删除演示专用临时书';

-- ⑥ 关联查询：书名 + 作者名
SELECT b.title, a.name AS author, b.price
FROM books AS b
JOIN authors AS a ON b.author_id = a.id
ORDER BY b.id;

-- 选做：GROUP BY，统计每位作者几本书、平均价
SELECT a.name, COUNT(*) AS book_count, ROUND(AVG(b.price), 2) AS avg_price
FROM authors AS a
JOIN books AS b ON b.author_id = a.id
GROUP BY a.id, a.name
ORDER BY book_count DESC, a.id;
