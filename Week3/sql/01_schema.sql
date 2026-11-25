-- Week3 01：建库建表
-- 执行顺序：01_schema.sql → 02_seed.sql → 03_queries.sql
-- 注意：本脚本会先删除 books、authors，重复执行会清空数据。

CREATE DATABASE IF NOT EXISTS bookshop
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bookshop;

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50)  NOT NULL,
    bio        VARCHAR(255),
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE books (
    id           INT UNSIGNED  AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(100)  NOT NULL,
    author_id    INT UNSIGNED  NOT NULL,
    price        DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    stock        INT UNSIGNED  NOT NULL DEFAULT 0,
    published_at DATE,
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_books_author
        FOREIGN KEY (author_id) REFERENCES authors (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
