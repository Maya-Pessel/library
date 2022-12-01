-- Active: 1667488332124@@127.0.0.1@5432@Queenmtp@public
-- create a postgresql database named "library"

CREATE DATABASE library;
-- create a table named member with columns memberId, name, email, password and role

CREATE TABLE member (
    memberId SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role INTEGER NOT NULL
);

CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    birth DATE NOT NULL,
    can_borrow BOOLEAN NOT NULL
);

-- create a table named book with columns isbn (serial primary key), name, author, date, category, quantity

CREATE TABLE book (
    isbn SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    category INTEGER,
    quantity INTEGER NOT NULL
);

-- create a table named borrow with columns borrowId, memberId, isbn, date, returnedDate

CREATE TABLE borrow (
    borrowId SERIAL PRIMARY KEY,
    memberId INTEGER NOT NULL,
    isbn INTEGER NOT NULL,
    date DATE NOT NULL,
    estimatedDate DATE NOT NULL,
    returnedDate DATE,
    FOREIGN KEY (memberId) REFERENCES member(memberId),
    FOREIGN KEY (isbn) REFERENCES book(isbn)
);


-- create a table named return with columns returnId, memberId, isbn, date

CREATE TABLE return (
    returnId SERIAL PRIMARY KEY,
    memberId INTEGER NOT NULL,
    isbn INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (memberId) REFERENCES member(memberId),
    FOREIGN KEY (isbn) REFERENCES book(isbn)
);

-- create a table named category with columns categoryId, name

CREATE TABLE category (
    categoryId SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- create table named role with columns roleId, name

CREATE TABLE role (
    roleId SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- create fake data for all table

INSERT INTO member (name, email, password, role) VALUES ('Jane Doe', '111111', 'janedoe@gmail.com', 1);
INSERT INTO member (name, email, password, role) VALUES ('John Doe', '222222', 'johndoe@gmail.com', 1);
INSERT INTO member (name, email, password, role) VALUES ('Jack Doe', '333333', 'jakedoe@gmail.com', 2);


-- book table in french 
INSERT INTO book (name, author, date, category, quantity) VALUES ('Le Petit Prince', 'Antoine de Saint-Exupéry', '1943-04-06', 1, 10);
INSERT INTO book (name, author, date, category, quantity) VALUES ('Le Seigneur des Anneaux', 'J. R. R. Tolkien', '1954-07-29', 1, 10);
INSERT INTO book (name, author, date, category, quantity) VALUES ('Le Hobbit', 'J. R. R. Tolkien', '1937-09-21', 1, 10);
INSERT INTO book (name, author, date, category, quantity) VALUES ('Harry Potter et la Chambre des secrets', 'J. K. Rowling', '1998-07-02', 1, 10);

-- category table in french

INSERT INTO category (name) VALUES ('roman');
INSERT INTO category (name) VALUES ('science');
INSERT INTO category (name) VALUES ('histoire');
INSERT INTO category (name) VALUES ('poésie');
INSERT INTO category (name) VALUES ('biographie');


--role table in french

INSERT INTO role (name) VALUES ('membre');
INSERT INTO role (name) VALUES ('admin');
