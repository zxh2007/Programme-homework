# Week3：MySQL 图书库（bookshop）

用 MySQL 建一个 `bookshop` 库，两张表 `authors` / `books`，完成建表、插入和六道查询 / 更新 / 删除题。

## 环境

- MySQL 8.x（MySQL Workbench 或命令行）
- 数据库名：`bookshop`
- 字符集：`utf8mb4`

## 从空库复现

1. 连接 MySQL（Workbench 里连 `root@localhost:3306`，或命令行 `mysql -u root -p`）。
2. 在 `Week3` 目录下，按顺序执行：

| 顺序 | 文件 | 作用 |
| --- | --- | --- |
| 0 | `sql/00-version.sql` | 查看 MySQL 版本（可选） |
| 1 | `sql/01_schema.sql` | 建库、建 `authors` / `books` |
| 2 | `sql/02_seed.sql` | 4 位作者、8 本书 |
| 3 | `sql/03_queries.sql` | 六道题 |
| 4 | `sql/04_optional_group_by.sql` | 选做：GROUP BY |

命令行方式（密码按提示输入，不写进文件）：

```bash
mysql -u root -p < sql/00-version.sql
mysql -u root -p < sql/01_schema.sql
mysql -u root -p < sql/02_seed.sql
mysql -u root -p < sql/03_queries.sql
```

> `01_schema.sql` 会先 `DROP TABLE` 再建表，重复执行会清空数据；`02_seed.sql` 只应导入一次。

## 用 Docker 启动 MySQL（选做）

本机装了 Docker Desktop 的话，可以不用本地 MySQL：

```bash
cd Week3
cp .env.example .env          # 把 MYSQL_ROOT_PASSWORD 改成自己的密码
docker compose up -d
docker compose ps             # 等 STATUS 变成 healthy
```

然后用 Workbench 连 `127.0.0.1:3306`（用户 `root`，密码是 `.env` 里的），再按上面的顺序手动执行 SQL。

`docker-compose.yml` 故意没有把 `sql/` 挂到 `docker-entrypoint-initdb.d`，避免容器初始化和手动执行重复跑两遍。

停止：`docker compose down`；连数据一起清掉：`docker compose down -v`。
如果本机 3306 已被占用，把 `ports` 改成 `"127.0.0.1:3307:3306"`，连接端口也改成 3307。

## 表结构

### authors

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INT UNSIGNED | 主键，自增 |
| name | VARCHAR(50) | 作者名，非空 |
| bio | VARCHAR(255) | 简介，非空，默认空字符串 |
| created_at | DATETIME | 默认当前时间 |

### books

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INT UNSIGNED | 主键，自增 |
| title | VARCHAR(100) | 书名，非空 |
| author_id | INT UNSIGNED | 外键，指向 `authors.id` |
| price | DECIMAL(8,2) | 价格，默认 0.00 |
| stock | INT UNSIGNED | 库存，默认 0，不能为负 |
| published_at | DATE | 出版日期，可空 |
| created_at | DATETIME | 默认当前时间 |

## 设计解释

- **主键为什么存在**：`id` 唯一标识一行；没有主键，外键就没有可引用的目标，表之间的关系也无法表达。
- **外键引用哪张表的哪一列**：`books.author_id` 引用 `authors.id`，表示这本书属于哪位作者。
- **价格为什么用 DECIMAL**：金额需要精确小数，`DECIMAL(8,2)` 共 8 位、2 位小数，不会像浮点数那样出现 `0.1 + 0.2` 的精度误差。
- **库存为什么用 INT UNSIGNED**：库存不可能为负；配合更新时的 `stock > 0`，可以防止减成负数。

## 主外键

- `authors.id` 是主键：唯一、非空、自增。
- `books.author_id` 是外键，`REFERENCES authors(id)`；一个作者可以有多本书（1 : N），所以外键放在 `books` 这一侧。
- 必须先插作者、再插图书，否则外键找不到父记录会报错（1452）。
- 默认的 `RESTRICT` 会阻止删除仍有图书的作者；`author_id` 上的索引也让 JOIN 更快。

## 六道题

| 题 | 要求 | 预期结果 |
| --- | --- | --- |
| Q1 | 查询库存为 0 的书名和库存 | 球状闪电、白夜行 |
| Q2 | 按价格降序取前三本，同价按 id 升序 | 白夜行 39.50、解忧杂货店 35.00、球状闪电 32.00 |
| Q3 | 价格在 20~40 之间（含边界） | 7 本，不含《呐喊》 |
| Q4 | JOIN 查书名、作者名、价格 | 8 行 |
| Q5 | 《三体》库存减 1，不能减成负数 | 12 → 11 |
| Q6 | 插入临时书，确认后删除 | 删除后查询为空 |

## 验证记录

执行 `03_queries.sql` 后重点核对下面几项（结果为按种子数据推算，实际执行后请核对）：

1. Q1：

| title | stock |
| --- | --- |
| 球状闪电 | 0 |
| 白夜行 | 0 |

2. Q2：

| id | title | price |
| --- | --- | --- |
| 5 | 白夜行 | 39.50 |
| 6 | 解忧杂货店 | 35.00 |
| 2 | 球状闪电 | 32.00 |

3. Q5：《三体》库存从 12 变成 11。

| id | title | stock |
| --- | --- | --- |
| 1 | 三体 | 11 |

4. Q6：临时书插入后能按 id 查到，`DELETE` 后再查结果为空。

5. Q4 的 JOIN 结果：

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

## 排错

| 现象 | 原因 / 处理 |
| --- | --- |
| 1050 Table already exists | 之前建过表；先执行 `01_schema.sql`（会 DROP 重建），或手动删表 |
| 1452 Cannot add or update a child row | 外键找不到作者；先执行 `02_seed.sql` 插作者，再插图书 |
| 1062 Duplicate entry | `02_seed.sql` 重复导入了；先跑 `01` 重置再导一次 |
| 1045 Access denied | 用户名/密码不对；检查 Workbench 连接或 `.env` |
| 2003 Can't connect to MySQL server | MySQL 没启动，或 3306 被占用/端口不对 |

## 选做

- `04_optional_group_by.sql`：统计每位作者几本书、平均价（每人 2 本；平均价分别为 27.50、24.00、37.25、20.00）。
- `docker-compose.yml`：用 Docker 启动 MySQL 8.4。
