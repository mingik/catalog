-- Table definitions for the catalog project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS catalog;

CREATE DATABASE catalog;

\c catalog;

DROP TABLE IF EXISTS categories;

create table categories (
       id SERIAL primary key,
       name varchar(20) NOT NULL
);

INSERT INTO categories VALUES (1,'Soccer');
INSERT INTO categories VALUES (2,'Basketball');
INSERT INTO categories VALUES (3,'Baseball');
INSERT INTO categories VALUES (4,'Fresbee');
INSERT INTO categories VALUES (5,'Snowboarding');
INSERT INTO categories VALUES (6,'Rock Climbing');
INSERT INTO categories VALUES (7,'Soccer');
INSERT INTO categories VALUES (8,'Foosball');
INSERT INTO categories VALUES (9,'Skating');
INSERT INTO categories VALUES (10,'Hockey');

DROP TABLE IF EXISTS items;

create table items (
       id SERIAL primary key,
       cat_id SERIAL references categories(id),
       title varchar(20) NOT NULL,
       description varchar(100) NOT NULL
);

INSERT INTO items VALUES (1,1,'Soccer Cleats','The shoes');
INSERT INTO items VALUES (2,1,'Jersey','The shirt');
INSERT INTO items VALUES (3,3,'Bat','The bat');
INSERT INTO items VALUES (4,5,'Snowboard','Best of any terrain');
