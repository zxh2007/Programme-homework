-- Week3 03：六道查询 / 更新 / 删除题
-- 前提：已执行 01_schema.sql、02_seed.sql（空库、刚导入种子数据）

USE bookshop;

-- Q1：查询库存为 0 的书名和库存。
-- 预期结果：球状闪电 0、白夜行 0
SELECT title, stock
FROM books
WHERE stock = 0;

-- Q2：按价格降序取前三本，同价时按 id 升序。
-- 预期结果：白夜行 39.50、解忧杂货店 35.00、球状闪电 32.00
SELECT id, title, price
FROM books
ORDER BY price DESC, id ASC
LIMIT 3;

-- Q3：查询价格在 20 到 40 之间的书（含边界）。
-- 预期结果：三体、球状闪电、活着、许三观卖血记、白夜行、解忧杂货店、彷徨（共 7 本）
SELECT id, title, price
FROM books
WHERE price BETWEEN 20 AND 40
ORDER BY id;

-- Q4：JOIN 查每本书的书名、作者名和价格。
-- 预期结果：8 行，顺序与 02_seed.sql 一致
SELECT b.title, a.name AS author, b.price
FROM books AS b
JOIN authors AS a ON b.author_id = a.id
ORDER BY b.id;

-- Q5：先查《三体》当前库存（12），再减 1，最后再查一次（11）。
-- stock > 0 防止库存减成负数
SELECT id, title, stock
FROM books
WHERE id = 1;

UPDATE books
SET stock = stock - 1
WHERE id = 1 AND stock > 0;

SELECT id, title, stock
FROM books
WHERE id = 1;

-- Q6：插入一条唯一标记的临时书，确认后按 id 删除它，不影响其他书。
-- 用 LAST_INSERT_ID() 拿到刚插入的 id，比按标题删更稳妥
INSERT INTO books (title, author_id, price, stock, published_at)
VALUES (
    '删除演示专用临时书',
    (SELECT id FROM authors WHERE name = '刘慈欣'),
    9.90,
    1,
    '2026-12-01'
);

SET @book_id = LAST_INSERT_ID();

SELECT id, title
FROM books
WHERE id = @book_id;

DELETE FROM books
WHERE id = @book_id;

-- 删除后再查一次，结果应为空
SELECT id, title
FROM books
WHERE id = @book_id;
