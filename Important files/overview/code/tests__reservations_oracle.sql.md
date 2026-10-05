# tests/reservations_oracle.sql

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/reservations_oracle.sql)। Snapshot 2026-10-04; 60 lines; SHA-256 `f738062bc945260631ed1031b73f47c0c97099faf18c9efa706abf35b38afabd`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
-- Real Oracle checks; test records, loans and holds are always rolled back.
SET SERVEROUTPUT ON
DECLARE
  v_student NUMBER; v_other NUMBER; v_book NUMBER; v_second NUMBER;
  v_third NUMBER; v_fourth NUMBER; v_author NUMBER; v_category NUMBER;
  v_copy NUMBER; v_reservation NUMBER; v_count NUMBER; v_issue NUMBER;
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
BEGIN
  SELECT MIN(author_id) INTO v_author FROM author;
  SELECT MIN(category_id) INTO v_category FROM category;
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Reservation QA','QA','09888888881','reservation-qa1@invalid.test','unused','RES-QA1','RES-REG1','2025-2026') RETURNING student_id INTO v_student;
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Reservation other QA','QA','09888888882','reservation-qa2@invalid.test','unused','RES-QA2','RES-REG2','2025-2026') RETURNING student_id INTO v_other;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 1',v_author,v_category,1,1) RETURNING book_id INTO v_book;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 2',v_author,v_category,2,2) RETURNING book_id INTO v_second;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 3',v_author,v_category,1,1) RETURNING book_id INTO v_third;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 4',v_author,v_category,1,1) RETURNING book_id INTO v_fourth;
  reserve_book_proc(v_student,v_book);
  SELECT reservation_id,copy_id INTO v_reservation,v_copy FROM book_reservation WHERE student_id=v_student AND book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE reservation_id=v_reservation AND ABS(expires_at-reserved_at-3)<1/86400;
  check_true(v_count=1,'Reservation must last exactly three days');
  BEGIN reserve_book_proc(v_other,v_book); RAISE_APPLICATION_ERROR(-20999,'Last copy reserved twice');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20001 THEN RAISE; END IF; END;
  BEGIN issue_book_proc(v_other,v_book,v_copy); RAISE_APPLICATION_ERROR(-20999,'Reserved copy issued to another member');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20031 THEN RAISE; END IF; END;
  BEGIN issue_book_proc(v_other,v_book); RAISE_APPLICATION_ERROR(-20999,'Auto selection stole reserved copy');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20001 THEN RAISE; END IF; END;
  BEGIN UPDATE book SET quantity=0,available_quantity=0 WHERE book_id=v_book; RAISE_APPLICATION_ERROR(-20999,'Reserved stock retired');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20008 THEN RAISE; END IF; END;
  reserve_book_proc(v_student,v_second);
  BEGIN reserve_book_proc(v_student,v_second); RAISE_APPLICATION_ERROR(-20999,'Duplicate title reservation accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20030 THEN RAISE; END IF; END;
  reserve_book_proc(v_student,v_third);
  BEGIN reserve_book_proc(v_student,v_fourth); RAISE_APPLICATION_ERROR(-20999,'Fourth hold accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20006 THEN RAISE; END IF; END;
  -- Pickup replaces one hold with one loan, even with three occupied slots.
  issue_book_proc(v_student,v_book);
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE reservation_id=v_reservation AND status='COLLECTED';
  check_true(v_count=1,'Pickup must collect the reservation');
  SELECT issue_id INTO v_issue FROM issue_book WHERE student_id=v_student AND book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE issue_id=v_issue AND ABS(due_date-issue_date-15)<1/86400;
  check_true(v_count=1,'Reserved pickup must create a 15-day loan');
  return_book_proc(v_issue);
  -- Effective expiry releases stock before the background job runs.
  UPDATE book_reservation SET expires_at=SYSDATE-1/86400 WHERE student_id=v_student AND book_id=v_third;
  reserve_book_proc(v_other,v_third);
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE student_id=v_student AND book_id=v_third AND status='EXPIRED';
  check_true(v_count=1,'Expired reservation must be cancelled automatically');
  UPDATE book_reservation SET status='CANCELLED' WHERE student_id=v_student AND book_id=v_second;
  reserve_book_proc(v_other,v_second);
  UPDATE student SET membership_status='DISABLED' WHERE student_id=v_student;
  BEGIN reserve_book_proc(v_student,v_fourth); RAISE_APPLICATION_ERROR(-20999,'Disabled member reserved a book');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20005 THEN RAISE; END IF; END;
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: last copy, owner protection, stock reduction, limits, pickup, expiry, cancellation, membership');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Real Oracle checks; test records, loans and holds are always rolled back.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET SERVEROUTPUT ON</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>  v_student NUMBER; v_other NUMBER; v_book NUMBER; v_second NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  v_third NUMBER; v_fourth NUMBER; v_author NUMBER; v_category NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  v_copy NUMBER; v_reservation NUMBER; v_count NUMBER; v_issue NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 8 | <code>  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 9 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>  SELECT MIN(author_id) INTO v_author FROM author;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 11 | <code>  SELECT MIN(category_id) INTO v_category FROM category;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 12 | <code>  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)</code> | নতুন business/audit/sample row insert করার statement। |
| 13 | <code>    VALUES(&#x27;Reservation QA&#x27;,&#x27;QA&#x27;,&#x27;09888888881&#x27;,&#x27;reservation-qa1@invalid.test&#x27;,&#x27;unused&#x27;,&#x27;RES-QA1&#x27;,&#x27;RES-REG1&#x27;,&#x27;2025-2026&#x27;) RETURNING student_id INTO v_student;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 14 | <code>  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)</code> | নতুন business/audit/sample row insert করার statement। |
| 15 | <code>    VALUES(&#x27;Reservation other QA&#x27;,&#x27;QA&#x27;,&#x27;09888888882&#x27;,&#x27;reservation-qa2@invalid.test&#x27;,&#x27;unused&#x27;,&#x27;RES-QA2&#x27;,&#x27;RES-REG2&#x27;,&#x27;2025-2026&#x27;) RETURNING student_id INTO v_other;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 16 | <code>  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES(&#x27;Reservation QA 1&#x27;,v_author,v_category,1,1) RETURNING book_id INTO v_book;</code> | নতুন business/audit/sample row insert করার statement। |
| 17 | <code>  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES(&#x27;Reservation QA 2&#x27;,v_author,v_category,2,2) RETURNING book_id INTO v_second;</code> | নতুন business/audit/sample row insert করার statement। |
| 18 | <code>  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES(&#x27;Reservation QA 3&#x27;,v_author,v_category,1,1) RETURNING book_id INTO v_third;</code> | নতুন business/audit/sample row insert করার statement। |
| 19 | <code>  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES(&#x27;Reservation QA 4&#x27;,v_author,v_category,1,1) RETURNING book_id INTO v_fourth;</code> | নতুন business/audit/sample row insert করার statement। |
| 20 | <code>  reserve_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>  SELECT reservation_id,copy_id INTO v_reservation,v_copy FROM book_reservation WHERE student_id=v_student AND book_id=v_book;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 22 | <code>  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE reservation_id=v_reservation AND ABS(expires_at-reserved_at-3)&lt;1/86400;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 23 | <code>  check_true(v_count=1,&#x27;Reservation must last exactly three days&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 24 | <code>  BEGIN reserve_book_proc(v_other,v_book); RAISE_APPLICATION_ERROR(-20999,&#x27;Last copy reserved twice&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 25 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20001 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 26 | <code>  BEGIN issue_book_proc(v_other,v_book,v_copy); RAISE_APPLICATION_ERROR(-20999,&#x27;Reserved copy issued to another member&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 27 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20031 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 28 | <code>  BEGIN issue_book_proc(v_other,v_book); RAISE_APPLICATION_ERROR(-20999,&#x27;Auto selection stole reserved copy&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 29 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20001 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 30 | <code>  BEGIN UPDATE book SET quantity=0,available_quantity=0 WHERE book_id=v_book; RAISE_APPLICATION_ERROR(-20999,&#x27;Reserved stock retired&#x27;);</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 31 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20008 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 32 | <code>  reserve_book_proc(v_student,v_second);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 33 | <code>  BEGIN reserve_book_proc(v_student,v_second); RAISE_APPLICATION_ERROR(-20999,&#x27;Duplicate title reservation accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 34 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20030 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 35 | <code>  reserve_book_proc(v_student,v_third);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>  BEGIN reserve_book_proc(v_student,v_fourth); RAISE_APPLICATION_ERROR(-20999,&#x27;Fourth hold accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 37 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20006 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 38 | <code>  -- Pickup replaces one hold with one loan, even with three occupied slots.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 39 | <code>  issue_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE reservation_id=v_reservation AND status=&#x27;COLLECTED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 41 | <code>  check_true(v_count=1,&#x27;Pickup must collect the reservation&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 42 | <code>  SELECT issue_id INTO v_issue FROM issue_book WHERE student_id=v_student AND book_id=v_book;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 43 | <code>  SELECT COUNT(*) INTO v_count FROM issue_book WHERE issue_id=v_issue AND ABS(due_date-issue_date-15)&lt;1/86400;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 44 | <code>  check_true(v_count=1,&#x27;Reserved pickup must create a 15-day loan&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 45 | <code>  return_book_proc(v_issue);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 46 | <code>  -- Effective expiry releases stock before the background job runs.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 47 | <code>  UPDATE book_reservation SET expires_at=SYSDATE-1/86400 WHERE student_id=v_student AND book_id=v_third;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 48 | <code>  reserve_book_proc(v_other,v_third);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 49 | <code>  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE student_id=v_student AND book_id=v_third AND status=&#x27;EXPIRED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 50 | <code>  check_true(v_count=1,&#x27;Expired reservation must be cancelled automatically&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 51 | <code>  UPDATE book_reservation SET status=&#x27;CANCELLED&#x27; WHERE student_id=v_student AND book_id=v_second;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 52 | <code>  reserve_book_proc(v_other,v_second);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 53 | <code>  UPDATE student SET membership_status=&#x27;DISABLED&#x27; WHERE student_id=v_student;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 54 | <code>  BEGIN reserve_book_proc(v_student,v_fourth); RAISE_APPLICATION_ERROR(-20999,&#x27;Disabled member reserved a book&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 55 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20005 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 56 | <code>  ROLLBACK;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 57 | <code>  DBMS_OUTPUT.PUT_LINE(&#x27;PASS: last copy, owner protection, stock reduction, limits, pickup, expiry, cancellation, membership&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 58 | <code>EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 59 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 60 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
