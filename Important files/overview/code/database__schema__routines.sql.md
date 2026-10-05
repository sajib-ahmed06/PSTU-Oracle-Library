# database/schema/routines.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/routines.sql)। Snapshot 2026-10-04; 64 lines; SHA-256 `baf495639a190a5312793365785d9b2d71ce5fd5ed76a98bbf3dada4a6b6b103`।

## Function / object / element inventory

- **TRIGGER `issue_quantity_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `return_book_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **FUNCTION `check_book_available`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **VIEW `book_details`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
CREATE OR REPLACE TRIGGER issue_quantity_trigger
BEFORE INSERT ON issue_book FOR EACH ROW
DECLARE
  available_count NUMBER;
BEGIN
  SELECT available_quantity INTO available_count
  FROM book WHERE book_id = :NEW.book_id FOR UPDATE;
  IF available_count <= 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Book is not available');
  END IF;
  UPDATE book SET available_quantity = available_quantity - 1
  WHERE book_id = :NEW.book_id;
  IF :NEW.issue_date IS NULL THEN
    :NEW.issue_date := SYSDATE;
  END IF;
  IF :NEW.due_date IS NULL THEN
    :NEW.due_date := :NEW.issue_date + 15;
  END IF;
END;
/

CREATE OR REPLACE PROCEDURE return_book_proc(p_issue_id NUMBER) AS
  v_book_id NUMBER;
  v_status VARCHAR2(20);
  v_due_date DATE;
  v_fine NUMBER;
BEGIN
  SELECT book_id, status, due_date INTO v_book_id, v_status, v_due_date
  FROM issue_book WHERE issue_id = p_issue_id FOR UPDATE;
  IF v_status = 'RETURNED' THEN
    RAISE_APPLICATION_ERROR(-20002, 'Book is already returned');
  END IF;
  v_fine := GREATEST(TRUNC(SYSDATE) - TRUNC(NVL(v_due_date, SYSDATE)), 0) * 10;
  INSERT INTO return_book(issue_id, return_date, fine_amount, status)
  VALUES(p_issue_id, SYSDATE, v_fine, 'RETURNED');
  UPDATE issue_book SET status = 'RETURNED', return_date = SYSDATE
  WHERE issue_id = p_issue_id;
  UPDATE book SET available_quantity = available_quantity + 1
  WHERE book_id = v_book_id;
  IF v_fine > 0 THEN
    INSERT INTO fine(issue_id, amount, payment_status)
    VALUES(p_issue_id, v_fine, 'UNPAID');
  END IF;
END;
/

CREATE OR REPLACE FUNCTION check_book_available(p_book_id NUMBER) RETURN VARCHAR2 IS
  qty NUMBER;
BEGIN
  SELECT available_quantity INTO qty FROM book WHERE book_id = p_book_id;
  IF qty > 0 THEN
    RETURN 'AVAILABLE';
  ELSE
    RETURN 'NOT AVAILABLE';
  END IF;
END;
/

CREATE OR REPLACE VIEW book_details AS
SELECT b.book_id, b.title, a.author_name, c.category_name, b.publisher, b.quantity, b.available_quantity
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN category c ON b.category_id = c.category_id;
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>CREATE OR REPLACE TRIGGER issue_quantity_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 2 | <code>BEFORE INSERT ON issue_book FOR EACH ROW</code> | নতুন business/audit/sample row insert করার statement। |
| 3 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>  available_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  SELECT available_quantity INTO available_count</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 7 | <code>  FROM book WHERE book_id = :NEW.book_id FOR UPDATE;</code> | Concurrent changes নিয়ন্ত্রণে database lock নেয়। |
| 8 | <code>  IF available_count &lt;= 0 THEN</code> | PL/SQL condition/alternative branch। |
| 9 | <code>    RAISE_APPLICATION_ERROR(-20001, &#x27;Book is not available&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 10 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 11 | <code>  UPDATE book SET available_quantity = available_quantity - 1</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 12 | <code>  WHERE book_id = :NEW.book_id;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 13 | <code>  IF :NEW.issue_date IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 14 | <code>    :NEW.issue_date := SYSDATE;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 15 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 16 | <code>  IF :NEW.due_date IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 17 | <code>    :NEW.due_date := :NEW.issue_date + 15;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 18 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 19 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 20 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 21 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 22 | <code>CREATE OR REPLACE PROCEDURE return_book_proc(p_issue_id NUMBER) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 23 | <code>  v_book_id NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>  v_status VARCHAR2(20);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 25 | <code>  v_due_date DATE;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>  v_fine NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 28 | <code>  SELECT book_id, status, due_date INTO v_book_id, v_status, v_due_date</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 29 | <code>  FROM issue_book WHERE issue_id = p_issue_id FOR UPDATE;</code> | Concurrent changes নিয়ন্ত্রণে database lock নেয়। |
| 30 | <code>  IF v_status = &#x27;RETURNED&#x27; THEN</code> | PL/SQL condition/alternative branch। |
| 31 | <code>    RAISE_APPLICATION_ERROR(-20002, &#x27;Book is already returned&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 32 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 33 | <code>  v_fine := GREATEST(TRUNC(SYSDATE) - TRUNC(NVL(v_due_date, SYSDATE)), 0) * 10;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 34 | <code>  INSERT INTO return_book(issue_id, return_date, fine_amount, status)</code> | নতুন business/audit/sample row insert করার statement। |
| 35 | <code>  VALUES(p_issue_id, SYSDATE, v_fine, &#x27;RETURNED&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>  UPDATE issue_book SET status = &#x27;RETURNED&#x27;, return_date = SYSDATE</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 37 | <code>  WHERE issue_id = p_issue_id;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 38 | <code>  UPDATE book SET available_quantity = available_quantity + 1</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 39 | <code>  WHERE book_id = v_book_id;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>  IF v_fine &gt; 0 THEN</code> | PL/SQL condition/alternative branch। |
| 41 | <code>    INSERT INTO fine(issue_id, amount, payment_status)</code> | নতুন business/audit/sample row insert করার statement। |
| 42 | <code>    VALUES(p_issue_id, v_fine, &#x27;UNPAID&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 43 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 44 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 45 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 46 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 47 | <code>CREATE OR REPLACE FUNCTION check_book_available(p_book_id NUMBER) RETURN VARCHAR2 IS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 48 | <code>  qty NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 49 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 50 | <code>  SELECT available_quantity INTO qty FROM book WHERE book_id = p_book_id;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 51 | <code>  IF qty &gt; 0 THEN</code> | PL/SQL condition/alternative branch। |
| 52 | <code>    RETURN &#x27;AVAILABLE&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 53 | <code>  ELSE</code> | PL/SQL condition/alternative branch। |
| 54 | <code>    RETURN &#x27;NOT AVAILABLE&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 55 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 56 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 57 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 58 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 59 | <code>CREATE OR REPLACE VIEW book_details AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 60 | <code>SELECT b.book_id, b.title, a.author_name, c.category_name, b.publisher, b.quantity, b.available_quantity</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 61 | <code>FROM book b</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 62 | <code>JOIN author a ON b.author_id = a.author_id</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 63 | <code>JOIN category c ON b.category_id = c.category_id;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
