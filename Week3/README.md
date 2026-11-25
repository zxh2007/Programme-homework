# Week3：MySQL 图书库（bookshop）

用 MySQL 建一个 `bookshop` 库，两张表 `authors` / `books`，完成建表、插入、查询、更新、删除、关联查询六项操作。

## 任务对照

| 要求 | 位置 |
| --- | --- |
| 两张表 | `sql/01_schema.sql` |
| 四位作者、八本书 | `sql/02_seed.sql` |
| 六项 SQL 操作 | `sql/03_queries.sql` |
| 运行顺序、主外键解释、验证记录 | 本 README |

## 运行顺序

1. 打开 MySQL Workbench，连接 `root@localhost:3306`。
2. 依次执行 `sql/01_schema.sql`、`sql/02_seed.sql`、`sql/03_queries.sql`（每个文件都自带 `USE bookshop;`）。

命令行方式（在 `Week3` 目录下执行，密码按提示输入，不写进文件）：

```bash
mysql -u root -p < sql/01_schema.sql
mysql -u root -p < sql/02_seed.sql
mysql -u root -p < sql/03_queries.sql
```

> `01_schema.sql` 会先 `DROP TABLE` 再建表，重复执行会清空数据；`02_seed.sql` 只应导入一次。

## 表结构

### authors

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INT UNSIGNED | 主键，自增 |
| name | VARCHAR(50) | 作者名，非空 |
| bio | VARCHAR(255) | 简介 |
| created_at | DATETIME | 默认当前时间 |

### books

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INT UNSIGNED | 主键，自增 |
| title | VARCHAR(100) | 书名，非空 |
| author_id | INT UNSIGNED | 外键，指向 `authors.id` |
| price | DECIMAL(8,2) | 价格，默认 0.00 |
| stock | INT UNSIGNED | 库存，默认 0 |
| published_at | DATE | 出版日期，可空 |
| created_at | DATETIME | 默认当前时间 |

## 主外键解释

- `authors.id` 是主键：唯一、非空、自增，用来唯一标识一位作者。
- `books.author_id` 是外键，`REFERENCES authors(id)`，表示“这本书属于哪位作者”。
- 一个作者可以有多本书（1 : N），所以外键放在 `books` 这一侧，`authors` 不需要再存图书列表。
- 必须先插作者、再插图书，否则外键找不到父记录会报错。
- 默认的 `RESTRICT` 会阻止删除仍有图书的作者，避免出现“孤儿书”；`author_id` 上的索引也让 JOIN 更快。

## 六项 SQL 操作

| # | 操作 | 位置 |
| --- | --- | --- |
| ① | 建表（CREATE TABLE） | `01_schema.sql` |
| ② | 插入（INSERT） | `02_seed.sql` |
| ③ | 查询（SELECT / ORDER BY / WHERE / BETWEEN） | `03_queries.sql` |
| ④ | 更新（UPDATE） | `03_queries.sql` |
| ⑤ | 删除（DELETE） | `03_queries.sql` |
| ⑥ | 关联查询（JOIN） | `03_queries.sql` |

`03_queries.sql` 末尾还附了一条选做的 `GROUP BY`。

## 验证记录

执行 `03_queries.sql` 后：

1. 更新库存：`SELECT id, title, stock FROM books WHERE id = 1;`

| id | title | stock |
| --- | --- | --- |
| 1 | 三体 | 11 |

（种子数据里《三体》库存是 12，卖出一本后变成 11。）

2. 删除临时记录：插入后能查到，`DELETE` 后再查结果为空。

3. 关联查询：返回 8 行。

| title | author | price |
| --- | --- | --- |
| 三体 | 刘慈欣 | 23.00 |
| 球状闪电 | 刘慈欣 | 32.00 |
| 活着 | 余华 | 20.00 |
| 许三观卖血记 | 余华 | 28.00 |
| 白夜行 | 东野圭吾 | 39.50 |
| 解忧杂货店 | 东野圭吾 | 35.00 |
| 呐喊 | 鲁迅 | 18.00 |
| 彷徨 | 鲁迅 | 22.00 |

## 选做说明

- 已附 `GROUP BY`：每位作者几本书、平均价。
- ORM 与 Docker 未包含。
