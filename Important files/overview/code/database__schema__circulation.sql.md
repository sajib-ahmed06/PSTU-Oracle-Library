# database/schema/circulation.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/circulation.sql)। Snapshot 2026-10-04; 90 lines; SHA-256 `5d347ca297a9fbc3b593a5735f061980e0b2601fb92e7ac03036ba50ca04f410`।

## Function / object / element inventory

- **TABLE `issue_book`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `issue_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `issue_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `issue_book_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TABLE `return_book`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `return_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `return_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TABLE `fine`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `fine_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `fine_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
-- Loans, returns and fines
CREATE TABLE issue_book (
  issue_id NUMBER PRIMARY KEY,
  student_id NUMBER NOT NULL REFERENCES student(student_id),
  book_id NUMBER NOT NULL REFERENCES book(book_id),
  issue_date DATE DEFAULT SYSDATE NOT NULL,
  due_date DATE,
  return_date DATE,
  status VARCHAR2(20) DEFAULT 'ISSUED' NOT NULL CHECK (status IN ('ISSUED','RETURNED'))
);
CREATE SEQUENCE issue_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER issue_trigger BEFORE INSERT ON issue_book FOR EACH ROW
BEGIN
  IF :NEW.issue_id IS NULL THEN
    SELECT issue_seq.NEXTVAL INTO :NEW.issue_id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE PROCEDURE issue_book_proc(
  p_student_id NUMBER,
  p_book_id NUMBER
) AS
  v_membership_status student.membership_status%TYPE;
  v_active_loans NUMBER;
  v_unpaid_fines NUMBER;
BEGIN
  SELECT membership_status INTO v_membership_status
  FROM student
  WHERE student_id = p_student_id
  FOR UPDATE;

  IF v_membership_status <> 'ACTIVE' THEN
    RAISE_APPLICATION_ERROR(-20005, 'This membership is disabled');
  END IF;

  SELECT COUNT(*) INTO v_active_loans
  FROM issue_book
  WHERE student_id = p_student_id AND status = 'ISSUED';

  IF v_active_loans > 0 THEN
    RAISE_APPLICATION_ERROR(-20006, 'Return the current book before issuing another book');
  END IF;

  SELECT COUNT(*) INTO v_unpaid_fines
  FROM fine f
  JOIN issue_book i ON i.issue_id = f.issue_id
  WHERE i.student_id = p_student_id AND f.payment_status = 'UNPAID';

  IF v_unpaid_fines > 0 THEN
    RAISE_APPLICATION_ERROR(-20007, 'Pay all unpaid fines before issuing another book');
  END IF;

  INSERT INTO issue_book(student_id, book_id, issue_date, due_date, status)
  VALUES(p_student_id, p_book_id, SYSDATE, SYSDATE + 15, 'ISSUED');
END;
/

CREATE TABLE return_book (
  return_id NUMBER PRIMARY KEY,
  issue_id NUMBER NOT NULL UNIQUE REFERENCES issue_book(issue_id),
  return_date DATE DEFAULT SYSDATE NOT NULL,
  fine_amount NUMBER DEFAULT 0 NOT NULL CHECK (fine_amount >= 0),
  status VARCHAR2(20) DEFAULT 'RETURNED' NOT NULL
);
CREATE SEQUENCE return_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER return_trigger BEFORE INSERT ON return_book FOR EACH ROW
BEGIN
  IF :NEW.return_id IS NULL THEN
    SELECT return_seq.NEXTVAL INTO :NEW.return_id FROM dual;
  END IF;
END;
/

CREATE TABLE fine (
  fine_id NUMBER PRIMARY KEY,
  issue_id NUMBER NOT NULL UNIQUE REFERENCES issue_book(issue_id),
  amount NUMBER DEFAULT 0 NOT NULL CHECK (amount >= 0),
  payment_status VARCHAR2(20) DEFAULT 'UNPAID' NOT NULL CHECK (payment_status IN ('PAID','UNPAID'))
);
CREATE SEQUENCE fine_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER fine_trigger BEFORE INSERT ON fine FOR EACH ROW
BEGIN
  IF :NEW.fine_id IS NULL THEN
    SELECT fine_seq.NEXTVAL INTO :NEW.fine_id FROM dual;
  END IF;
END;
/
ALTER PROCEDURE issue_book_proc COMPILE;
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Loans, returns and fines</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>CREATE TABLE issue_book (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 3 | <code>  issue_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 4 | <code>  student_id NUMBER NOT NULL REFERENCES student(student_id),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 5 | <code>  book_id NUMBER NOT NULL REFERENCES book(book_id),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 6 | <code>  issue_date DATE DEFAULT SYSDATE NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>  due_date DATE,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>  return_date DATE,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>  status VARCHAR2(20) DEFAULT &#x27;ISSUED&#x27; NOT NULL CHECK (status IN (&#x27;ISSUED&#x27;,&#x27;RETURNED&#x27;))</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 10 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>CREATE SEQUENCE issue_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 12 | <code>CREATE OR REPLACE TRIGGER issue_trigger BEFORE INSERT ON issue_book FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 13 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 14 | <code>  IF :NEW.issue_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 15 | <code>    SELECT issue_seq.NEXTVAL INTO :NEW.issue_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 16 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 17 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 18 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>CREATE OR REPLACE PROCEDURE issue_book_proc(</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 21 | <code>  p_student_id NUMBER,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>  p_book_id NUMBER</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 23 | <code>) AS</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>  v_membership_status student.membership_status%TYPE;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 25 | <code>  v_active_loans NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>  v_unpaid_fines NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 28 | <code>  SELECT membership_status INTO v_membership_status</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 29 | <code>  FROM student</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 30 | <code>  WHERE student_id = p_student_id</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 31 | <code>  FOR UPDATE;</code> | Concurrent changes নিয়ন্ত্রণে database lock নেয়। |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>  IF v_membership_status &lt;&gt; &#x27;ACTIVE&#x27; THEN</code> | PL/SQL condition/alternative branch। |
| 34 | <code>    RAISE_APPLICATION_ERROR(-20005, &#x27;This membership is disabled&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 35 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 36 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 37 | <code>  SELECT COUNT(*) INTO v_active_loans</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 38 | <code>  FROM issue_book</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 39 | <code>  WHERE student_id = p_student_id AND status = &#x27;ISSUED&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 41 | <code>  IF v_active_loans &gt; 0 THEN</code> | PL/SQL condition/alternative branch। |
| 42 | <code>    RAISE_APPLICATION_ERROR(-20006, &#x27;Return the current book before issuing another book&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 43 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 44 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 45 | <code>  SELECT COUNT(*) INTO v_unpaid_fines</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 46 | <code>  FROM fine f</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 47 | <code>  JOIN issue_book i ON i.issue_id = f.issue_id</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 48 | <code>  WHERE i.student_id = p_student_id AND f.payment_status = &#x27;UNPAID&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 49 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 50 | <code>  IF v_unpaid_fines &gt; 0 THEN</code> | PL/SQL condition/alternative branch। |
| 51 | <code>    RAISE_APPLICATION_ERROR(-20007, &#x27;Pay all unpaid fines before issuing another book&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 52 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 53 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 54 | <code>  INSERT INTO issue_book(student_id, book_id, issue_date, due_date, status)</code> | নতুন business/audit/sample row insert করার statement। |
| 55 | <code>  VALUES(p_student_id, p_book_id, SYSDATE, SYSDATE + 15, &#x27;ISSUED&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 56 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 57 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 58 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 59 | <code>CREATE TABLE return_book (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 60 | <code>  return_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 61 | <code>  issue_id NUMBER NOT NULL UNIQUE REFERENCES issue_book(issue_id),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 62 | <code>  return_date DATE DEFAULT SYSDATE NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 63 | <code>  fine_amount NUMBER DEFAULT 0 NOT NULL CHECK (fine_amount &gt;= 0),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 64 | <code>  status VARCHAR2(20) DEFAULT &#x27;RETURNED&#x27; NOT NULL</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 65 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 66 | <code>CREATE SEQUENCE return_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 67 | <code>CREATE OR REPLACE TRIGGER return_trigger BEFORE INSERT ON return_book FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 68 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 69 | <code>  IF :NEW.return_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 70 | <code>    SELECT return_seq.NEXTVAL INTO :NEW.return_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 71 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 72 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 73 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 74 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 75 | <code>CREATE TABLE fine (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 76 | <code>  fine_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 77 | <code>  issue_id NUMBER NOT NULL UNIQUE REFERENCES issue_book(issue_id),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 78 | <code>  amount NUMBER DEFAULT 0 NOT NULL CHECK (amount &gt;= 0),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 79 | <code>  payment_status VARCHAR2(20) DEFAULT &#x27;UNPAID&#x27; NOT NULL CHECK (payment_status IN (&#x27;PAID&#x27;,&#x27;UNPAID&#x27;))</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 80 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 81 | <code>CREATE SEQUENCE fine_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 82 | <code>CREATE OR REPLACE TRIGGER fine_trigger BEFORE INSERT ON fine FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 83 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 84 | <code>  IF :NEW.fine_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 85 | <code>    SELECT fine_seq.NEXTVAL INTO :NEW.fine_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 86 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 87 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 88 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 89 | <code>ALTER PROCEDURE issue_book_proc COMPILE;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 90 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
