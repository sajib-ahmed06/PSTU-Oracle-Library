# database/schema/accounts.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/accounts.sql)। Snapshot 2026-10-04; 25 lines; SHA-256 `9fed13f39b6e5619a6d4576f9dc4aab5702674cd5410cfebed80e442ac3ebd29`।

## Function / object / element inventory

- **TABLE `login_user`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **INDEX `uq_login_username`**: Database integrity/search performance enforce করে।
- **INDEX `ix_issue_student_status`**: Database integrity/search performance enforce করে।
- **INDEX `ix_issue_book`**: Database integrity/search performance enforce করে।
- **INDEX `ix_book_author`**: Database integrity/search performance enforce করে।
- **INDEX `ix_book_category`**: Database integrity/search performance enforce করে।
- **SEQUENCE `login_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `login_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
-- Application accounts
CREATE TABLE login_user (
  user_id NUMBER PRIMARY KEY,
  username VARCHAR2(100) NOT NULL UNIQUE,
  password VARCHAR2(100) NOT NULL,
  user_type VARCHAR2(20) NOT NULL,
  account_status VARCHAR2(10) DEFAULT 'ACTIVE' NOT NULL,
  CONSTRAINT login_user_type_ck CHECK (user_type IN ('ADMIN','LIBRARIAN','STUDENT')),
  CONSTRAINT login_user_status_ck CHECK (account_status IN ('ACTIVE','DISABLED'))
);
CREATE UNIQUE INDEX uq_login_username ON login_user(LOWER(TRIM(username)));
CREATE INDEX ix_issue_student_status ON issue_book(student_id, status);
CREATE INDEX ix_issue_book ON issue_book(book_id);
CREATE INDEX ix_book_author ON book(author_id);
CREATE INDEX ix_book_category ON book(category_id);

CREATE SEQUENCE login_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER login_trigger BEFORE INSERT ON login_user FOR EACH ROW
BEGIN
  IF :NEW.user_id IS NULL THEN
    SELECT login_seq.NEXTVAL INTO :NEW.user_id FROM dual;
  END IF;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Application accounts</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>CREATE TABLE login_user (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 3 | <code>  user_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 4 | <code>  username VARCHAR2(100) NOT NULL UNIQUE,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 5 | <code>  password VARCHAR2(100) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  user_type VARCHAR2(20) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>  account_status VARCHAR2(10) DEFAULT &#x27;ACTIVE&#x27; NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>  CONSTRAINT login_user_type_ck CHECK (user_type IN (&#x27;ADMIN&#x27;,&#x27;LIBRARIAN&#x27;,&#x27;STUDENT&#x27;)),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 9 | <code>  CONSTRAINT login_user_status_ck CHECK (account_status IN (&#x27;ACTIVE&#x27;,&#x27;DISABLED&#x27;))</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 10 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>CREATE UNIQUE INDEX uq_login_username ON login_user(LOWER(TRIM(username)));</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 12 | <code>CREATE INDEX ix_issue_student_status ON issue_book(student_id, status);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 13 | <code>CREATE INDEX ix_issue_book ON issue_book(book_id);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 14 | <code>CREATE INDEX ix_book_author ON book(author_id);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 15 | <code>CREATE INDEX ix_book_category ON book(category_id);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>CREATE SEQUENCE login_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 18 | <code>CREATE OR REPLACE TRIGGER login_trigger BEFORE INSERT ON login_user FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 19 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 20 | <code>  IF :NEW.user_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 21 | <code>    SELECT login_seq.NEXTVAL INTO :NEW.user_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 22 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 23 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 25 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
