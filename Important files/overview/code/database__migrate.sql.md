# database/migrate.sql

Existing records না মুছে sequence advance, case-insensitive indexes ও member/audit upgrade চালায় এবং invalid objects পরীক্ষা করে।

Source: [মূল file](../../database/migrate.sql)। Snapshot 2026-10-04; 68 lines; SHA-256 `053a09425f1b652e14dee3cf07ddf6e68b286667f6f7197ce30ab18c3561eee8`।

## Function / object / element inventory

- **PROCEDURE `add_student_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **INDEX `uq_author_name`**: Database integrity/search performance enforce করে।
- **INDEX `uq_category_name`**: Database integrity/search performance enforce করে।
- **INDEX `uq_student_email`**: Database integrity/search performance enforce করে।
- **INDEX `uq_login_username`**: Database integrity/search performance enforce করে।
- **INDEX `ix_issue_student_status`**: Database integrity/search performance enforce করে।
- **INDEX `ix_issue_book`**: Database integrity/search performance enforce করে।
- **INDEX `ix_book_author`**: Database integrity/search performance enforce করে।
- **INDEX `ix_book_category`**: Database integrity/search performance enforce করে।

## সম্পূর্ণ original source

```sql
-- Preserve existing records while upgrading the original schema.
SET DEFINE OFF;
WHENEVER OSERROR EXIT FAILURE;
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;

-- Advance the sequence beyond IDs created by the old MAX(id) procedure.
DECLARE
  highest_id NUMBER;
  sequence_id NUMBER;
BEGIN
  SELECT NVL(MAX(student_id), 0) INTO highest_id FROM student;
  LOOP
    SELECT student_seq.NEXTVAL INTO sequence_id FROM dual;
    EXIT WHEN sequence_id > highest_id;
  END LOOP;
END;
/

CREATE OR REPLACE PROCEDURE add_student_proc(
  p_name VARCHAR2,
  p_department VARCHAR2,
  p_phone VARCHAR2,
  p_email VARCHAR2,
  p_password VARCHAR2
) AS
BEGIN
  INSERT INTO student(name, department, phone, email, password)
  VALUES(TRIM(p_name), TRIM(p_department), TRIM(p_phone), LOWER(TRIM(p_email)), p_password);
END;
/

-- Duplicate case-insensitive names must be reconciled before these indexes can be created.
DECLARE
  index_count NUMBER;
  PROCEDURE ensure_index(index_name VARCHAR2, statement VARCHAR2) IS
  BEGIN
    SELECT COUNT(*) INTO index_count FROM user_indexes WHERE user_indexes.index_name = UPPER(index_name);
    IF index_count = 0 THEN
      EXECUTE IMMEDIATE statement;
    END IF;
  END;
BEGIN
  ensure_index('uq_author_name', 'CREATE UNIQUE INDEX uq_author_name ON author(LOWER(TRIM(author_name)))');
  ensure_index('uq_category_name', 'CREATE UNIQUE INDEX uq_category_name ON category(LOWER(TRIM(category_name)))');
  ensure_index('uq_student_email', 'CREATE UNIQUE INDEX uq_student_email ON student(LOWER(TRIM(email)))');
  ensure_index('uq_login_username', 'CREATE UNIQUE INDEX uq_login_username ON login_user(LOWER(TRIM(username)))');
  ensure_index('ix_issue_student_status', 'CREATE INDEX ix_issue_student_status ON issue_book(student_id, status)');
  ensure_index('ix_issue_book', 'CREATE INDEX ix_issue_book ON issue_book(book_id)');
  ensure_index('ix_book_author', 'CREATE INDEX ix_book_author ON book(author_id)');
  ensure_index('ix_book_category', 'CREATE INDEX ix_book_category ON book(category_id)');
END;
/
-- New indexes can invalidate dependent PL/SQL objects in Oracle 10g.
ALTER TRIGGER student_trigger COMPILE;
ALTER PROCEDURE issue_book_proc COMPILE;
ALTER PROCEDURE return_book_proc COMPILE;
@@members_audit.sql

DECLARE
  invalid_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO invalid_count FROM user_objects WHERE status = 'INVALID';
  IF invalid_count > 0 THEN
    RAISE_APPLICATION_ERROR(-20099, 'Invalid database objects; inspect USER_ERRORS');
  END IF;
END;
/
PROMPT Existing library schema upgraded.
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Preserve existing records while upgrading the original schema.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET DEFINE OFF;</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>WHENEVER OSERROR EXIT FAILURE;</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 4 | <code>WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>-- Advance the sequence beyond IDs created by the old MAX(id) procedure.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 7 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>  highest_id NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>  sequence_id NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>  SELECT NVL(MAX(student_id), 0) INTO highest_id FROM student;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 12 | <code>  LOOP</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 13 | <code>    SELECT student_seq.NEXTVAL INTO sequence_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 14 | <code>    EXIT WHEN sequence_id &gt; highest_id;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 15 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 16 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 17 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 18 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 19 | <code>CREATE OR REPLACE PROCEDURE add_student_proc(</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 20 | <code>  p_name VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>  p_department VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>  p_phone VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 23 | <code>  p_email VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>  p_password VARCHAR2</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 25 | <code>) AS</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>  INSERT INTO student(name, department, phone, email, password)</code> | নতুন business/audit/sample row insert করার statement। |
| 28 | <code>  VALUES(TRIM(p_name), TRIM(p_department), TRIM(p_phone), LOWER(TRIM(p_email)), p_password);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 29 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 30 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>-- Duplicate case-insensitive names must be reconciled before these indexes can be created.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 33 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 34 | <code>  index_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 35 | <code>  PROCEDURE ensure_index(index_name VARCHAR2, statement VARCHAR2) IS</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>    SELECT COUNT(*) INTO index_count FROM user_indexes WHERE user_indexes.index_name = UPPER(index_name);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 38 | <code>    IF index_count = 0 THEN</code> | PL/SQL condition/alternative branch। |
| 39 | <code>      EXECUTE IMMEDIATE statement;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>    END IF;</code> | PL/SQL condition/alternative branch। |
| 41 | <code>  END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 42 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 43 | <code>  ensure_index(&#x27;uq_author_name&#x27;, &#x27;CREATE UNIQUE INDEX uq_author_name ON author(LOWER(TRIM(author_name)))&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 44 | <code>  ensure_index(&#x27;uq_category_name&#x27;, &#x27;CREATE UNIQUE INDEX uq_category_name ON category(LOWER(TRIM(category_name)))&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 45 | <code>  ensure_index(&#x27;uq_student_email&#x27;, &#x27;CREATE UNIQUE INDEX uq_student_email ON student(LOWER(TRIM(email)))&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 46 | <code>  ensure_index(&#x27;uq_login_username&#x27;, &#x27;CREATE UNIQUE INDEX uq_login_username ON login_user(LOWER(TRIM(username)))&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 47 | <code>  ensure_index(&#x27;ix_issue_student_status&#x27;, &#x27;CREATE INDEX ix_issue_student_status ON issue_book(student_id, status)&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 48 | <code>  ensure_index(&#x27;ix_issue_book&#x27;, &#x27;CREATE INDEX ix_issue_book ON issue_book(book_id)&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 49 | <code>  ensure_index(&#x27;ix_book_author&#x27;, &#x27;CREATE INDEX ix_book_author ON book(author_id)&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 50 | <code>  ensure_index(&#x27;ix_book_category&#x27;, &#x27;CREATE INDEX ix_book_category ON book(category_id)&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 51 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 52 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 53 | <code>-- New indexes can invalidate dependent PL/SQL objects in Oracle 10g.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 54 | <code>ALTER TRIGGER student_trigger COMPILE;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 55 | <code>ALTER PROCEDURE issue_book_proc COMPILE;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 56 | <code>ALTER PROCEDURE return_book_proc COMPILE;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 57 | <code>@@members_audit.sql</code> | Current SQL script-এর directory থেকে referenced feature script চালায়। |
| 58 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 59 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 60 | <code>  invalid_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 61 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 62 | <code>  SELECT COUNT(*) INTO invalid_count FROM user_objects WHERE status = &#x27;INVALID&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 63 | <code>  IF invalid_count &gt; 0 THEN</code> | PL/SQL condition/alternative branch। |
| 64 | <code>    RAISE_APPLICATION_ERROR(-20099, &#x27;Invalid database objects; inspect USER_ERRORS&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 65 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 66 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 67 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 68 | <code>PROMPT Existing library schema upgraded.</code> | Script progress/completion message output করে। |
