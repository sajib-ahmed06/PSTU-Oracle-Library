# database/schema/catalogue.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/catalogue.sql)। Snapshot 2026-10-04; 50 lines; SHA-256 `445e1195049df78bd3328bdcc5420280cd79fe71da296affa6aaefbef61a7e6a`।

## Function / object / element inventory

- **TABLE `author`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `author_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `author_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **INDEX `uq_author_name`**: Database integrity/search performance enforce করে।
- **TABLE `category`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `category_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `category_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **INDEX `uq_category_name`**: Database integrity/search performance enforce করে।
- **INDEX `uq_student_roll`**: Database integrity/search performance enforce করে।
- **INDEX `uq_student_registration`**: Database integrity/search performance enforce করে।
- **INDEX `uq_student_email`**: Database integrity/search performance enforce করে।
- **TABLE `book`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `book_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `book_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **INDEX `uq_book_identity`**: Database integrity/search performance enforce করে।

## সম্পূর্ণ original source

```sql
-- Book catalogue
CREATE TABLE author (author_id NUMBER PRIMARY KEY, author_name VARCHAR2(100) NOT NULL UNIQUE);
CREATE SEQUENCE author_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER author_trigger BEFORE INSERT ON author FOR EACH ROW
BEGIN
  IF :NEW.author_id IS NULL THEN
    SELECT author_seq.NEXTVAL INTO :NEW.author_id FROM dual;
  END IF;
END;
/

CREATE UNIQUE INDEX uq_author_name ON author(LOWER(TRIM(author_name)));

CREATE TABLE category (category_id NUMBER PRIMARY KEY, category_name VARCHAR2(100) NOT NULL UNIQUE);
CREATE SEQUENCE category_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER category_trigger BEFORE INSERT ON category FOR EACH ROW
BEGIN
  IF :NEW.category_id IS NULL THEN
    SELECT category_seq.NEXTVAL INTO :NEW.category_id FROM dual;
  END IF;
END;
/

CREATE UNIQUE INDEX uq_category_name ON category(LOWER(TRIM(category_name)));
CREATE UNIQUE INDEX uq_student_roll ON student(UPPER(TRIM(roll_no)));
CREATE UNIQUE INDEX uq_student_registration ON student(UPPER(TRIM(registration_no)));
CREATE UNIQUE INDEX uq_student_email ON student(LOWER(TRIM(email)));

CREATE TABLE book (
  book_id NUMBER PRIMARY KEY,
  title VARCHAR2(200) NOT NULL,
  author_id NUMBER NOT NULL REFERENCES author(author_id),
  category_id NUMBER NOT NULL REFERENCES category(category_id),
  publisher VARCHAR2(100),
  quantity NUMBER DEFAULT 0 NOT NULL CHECK (quantity >= 0),
  available_quantity NUMBER DEFAULT 0 NOT NULL,
  CONSTRAINT ck_book_availability
    CHECK (available_quantity >= 0 AND available_quantity <= quantity)
);
CREATE SEQUENCE book_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER book_trigger BEFORE INSERT ON book FOR EACH ROW
BEGIN
  IF :NEW.book_id IS NULL THEN
    SELECT book_seq.NEXTVAL INTO :NEW.book_id FROM dual;
  END IF;
END;
/
CREATE UNIQUE INDEX uq_book_identity
ON book(LOWER(TRIM(title)), author_id, category_id);
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Book catalogue</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>CREATE TABLE author (author_id NUMBER PRIMARY KEY, author_name VARCHAR2(100) NOT NULL UNIQUE);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 3 | <code>CREATE SEQUENCE author_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 4 | <code>CREATE OR REPLACE TRIGGER author_trigger BEFORE INSERT ON author FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 5 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  IF :NEW.author_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 7 | <code>    SELECT author_seq.NEXTVAL INTO :NEW.author_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 8 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 9 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 11 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 12 | <code>CREATE UNIQUE INDEX uq_author_name ON author(LOWER(TRIM(author_name)));</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>CREATE TABLE category (category_id NUMBER PRIMARY KEY, category_name VARCHAR2(100) NOT NULL UNIQUE);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 15 | <code>CREATE SEQUENCE category_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 16 | <code>CREATE OR REPLACE TRIGGER category_trigger BEFORE INSERT ON category FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 17 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 18 | <code>  IF :NEW.category_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 19 | <code>    SELECT category_seq.NEXTVAL INTO :NEW.category_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 20 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 21 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>CREATE UNIQUE INDEX uq_category_name ON category(LOWER(TRIM(category_name)));</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 25 | <code>CREATE UNIQUE INDEX uq_student_roll ON student(UPPER(TRIM(roll_no)));</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 26 | <code>CREATE UNIQUE INDEX uq_student_registration ON student(UPPER(TRIM(registration_no)));</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 27 | <code>CREATE UNIQUE INDEX uq_student_email ON student(LOWER(TRIM(email)));</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>CREATE TABLE book (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 30 | <code>  book_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 31 | <code>  title VARCHAR2(200) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 32 | <code>  author_id NUMBER NOT NULL REFERENCES author(author_id),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 33 | <code>  category_id NUMBER NOT NULL REFERENCES category(category_id),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 34 | <code>  publisher VARCHAR2(100),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 35 | <code>  quantity NUMBER DEFAULT 0 NOT NULL CHECK (quantity &gt;= 0),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 36 | <code>  available_quantity NUMBER DEFAULT 0 NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>  CONSTRAINT ck_book_availability</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 38 | <code>    CHECK (available_quantity &gt;= 0 AND available_quantity &lt;= quantity)</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 39 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>CREATE SEQUENCE book_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 41 | <code>CREATE OR REPLACE TRIGGER book_trigger BEFORE INSERT ON book FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 42 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 43 | <code>  IF :NEW.book_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 44 | <code>    SELECT book_seq.NEXTVAL INTO :NEW.book_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 45 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 46 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 47 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 48 | <code>CREATE UNIQUE INDEX uq_book_identity</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 49 | <code>ON book(LOWER(TRIM(title)), author_id, category_id);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 50 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
