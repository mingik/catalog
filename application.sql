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

TRUNCATE TABLE categories CASCADE;

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
INSERT INTO categories VALUES (7,'Foosball');
INSERT INTO categories VALUES (8,'Skating');
INSERT INTO categories VALUES (9,'Hockey');

Realm of RacketTRUNCATE TABLE items;

create table items (
       id SERIAL,
       cat_id SERIAL references categories(id),
       cat_name varchar(20) NOT NULL,
       title varchar(20) NOT NULL,
       description varchar(100) NOT NULL
);

INSERT INTO items VALUES (1,1,'Soccer','Soccer Cleats','The shoes.');
INSERT INTO items VALUES (2,1,'Soccer','Jersey','The shirt with number on the back.');
INSERT INTO items VALUES (3,2,'Basketball','Air Jordan','Sneakers for jumping high.');
INSERT INTO items VALUES (4,3,'Baseball','Bat','Black bat.');
INSERT INTO items VALUES (5,4,'Fresbee','Disc','The flying disc.');
INSERT INTO items VALUES (6,5,'Snowboarding','Snowboard','Best snowboard for any terrain.');
INSERT INTO items VALUES (7,6,'Rock Climbing','Rope','Strong rope for climbing.');
INSERT INTO items VALUES (8,7,'Foosball','Ball','Little plastic ball.');
INSERT INTO items VALUES (9,8,'Skating','Board','Skating board.');
INSERT INTO items VALUES (10,9,'Hockey','Mask','Mask for goale.');
