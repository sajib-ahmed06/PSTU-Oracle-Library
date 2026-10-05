# tests/circulation_oracle.sql

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/circulation_oracle.sql)। Snapshot 2026-10-04; 104 lines; SHA-256 `297bc45b145b2789f9240e8a8115b0b1ecb1b181ee66c83b1b5d6e073e039ac2`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
-- Integration checks against Oracle. All test rows and changes are rolled back.
SET SERVEROUTPUT ON
DECLARE
  v_student NUMBER; v_book NUMBER; v_issue NUMBER; v_fine NUMBER;
  v_count NUMBER; v_total NUMBER; v_available NUMBER; v_copy NUMBER;
  v_paid NUMBER; v_status VARCHAR2(20);
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
BEGIN
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
  VALUES('Circulation rollback test','QA','09999999999','circulation-rollback-test@invalid.test','unused','QA-ROLL-TEST','QA-REG-TEST','2025-2026') RETURNING student_id INTO v_student;
  SELECT MIN(book_id) INTO v_book FROM book WHERE available_quantity>=4;
  check_true(v_book IS NOT NULL,'A book with at least four available copies is required');
  SELECT quantity,available_quantity INTO v_total,v_available FROM book WHERE book_id=v_book;
  -- Stock additions/removal must also add/retire physical copies.
  UPDATE book SET quantity=quantity+2,available_quantity=available_quantity+2 WHERE book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=v_book AND status<>'RETIRED';
  check_true(v_count=v_total+2,'Stock add mismatch');
  UPDATE book SET quantity=quantity-2,available_quantity=available_quantity-2 WHERE book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=v_book AND status<>'RETIRED';
  check_true(v_count=v_total,'Stock reduction mismatch');
  issue_book_proc(v_student,v_book);
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND ABS(due_date-issue_date-15)<1/86400;
  check_true(v_count=1,'New loan must be due 15 days after issue');
  issue_book_proc(v_student,v_book);
  issue_book_proc(v_student,v_book);
  SELECT COUNT(DISTINCT copy_id) INTO v_count FROM issue_book WHERE student_id=v_student AND status='ISSUED';
  check_true(v_count=3,'Three distinct physical copies required');
  BEGIN
    issue_book_proc(v_student,v_book);
    RAISE_APPLICATION_ERROR(-20999,'Fourth loan unexpectedly accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20006 THEN RAISE; END IF; END;
  SELECT MIN(issue_id) INTO v_issue FROM issue_book WHERE student_id=v_student;
  SELECT copy_id INTO v_copy FROM issue_book WHERE issue_id=v_issue;
  UPDATE issue_book SET due_date=TRUNC(SYSDATE)-10 WHERE issue_id=v_issue;
  return_book_proc(v_issue);
  SELECT status INTO v_status FROM book_copy WHERE copy_id=v_copy;
  check_true(v_status='AVAILABLE','Returned physical copy must become available');
  SELECT available_quantity INTO v_count FROM book WHERE book_id=v_book;
  check_true(v_count=v_available-2,'Only returned copy must restore stock');
  BEGIN
    return_book_proc(v_issue);
    RAISE_APPLICATION_ERROR(-20999,'Double return accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20002 THEN RAISE; END IF; END;
  SELECT fine_id,amount INTO v_fine,v_paid FROM fine WHERE issue_id=v_issue;
  check_true(v_paid=100,'Final overdue fine incorrect');
  BEGIN
    pay_fine_proc(v_fine,35.25,'Partial payment attempt');
    RAISE_APPLICATION_ERROR(-20999,'Partial payment accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20012 THEN RAISE; END IF; END;
  SELECT paid_amount,payment_status INTO v_paid,v_status FROM fine WHERE fine_id=v_fine;
  check_true(v_paid=0 AND v_status='UNPAID','Rejected payment changed balance');
  SELECT COUNT(*) INTO v_count FROM fine_payment WHERE fine_id=v_fine;
  check_true(v_count=0,'Rejected payment created a receipt');
  BEGIN
    pay_fine_proc(v_fine,100.01);
    RAISE_APPLICATION_ERROR(-20999,'Overpayment accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20012 THEN RAISE; END IF; END;
  BEGIN
    issue_book_proc(v_student,v_book,v_copy);
    RAISE_APPLICATION_ERROR(-20999,'Unpaid fine did not block loan');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20007 THEN RAISE; END IF; END;
  pay_fine_proc(v_fine);
  SELECT paid_amount,payment_status INTO v_paid,v_status FROM fine WHERE fine_id=v_fine;
  check_true(v_paid=100 AND v_status='PAID','Final settlement incorrect');
  SELECT COUNT(*) INTO v_count FROM fine_payment WHERE fine_id=v_fine;
  check_true(v_count=1,'One full payment receipt required');
  SELECT copy_id INTO v_count FROM issue_book WHERE issue_id=(SELECT MIN(issue_id) FROM issue_book WHERE student_id=v_student AND status='ISSUED');
  BEGIN
    issue_book_proc(v_student,v_book,v_count);
    RAISE_APPLICATION_ERROR(-20999,'Already borrowed copy accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20010 THEN RAISE; END IF; END;
  issue_book_proc(v_student,v_book,v_copy);
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND copy_id=v_copy;
  check_true(v_count=2,'Returned copy should be reusable');
  BEGIN
    pay_fine_proc(v_fine);
    RAISE_APPLICATION_ERROR(-20999,'Duplicate payment accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20011 THEN RAISE; END IF; END;
  -- A failed selection must roll back earlier issues from the same request.
  SELECT MAX(issue_id) INTO v_issue FROM issue_book WHERE student_id=v_student;
  return_book_proc(v_issue);
  SAVEPOINT batch_test;
  BEGIN
    issue_book_proc(v_student,v_book,v_copy);
    issue_book_proc(v_student,v_book);
    RAISE_APPLICATION_ERROR(-20999,'Failed batch unexpectedly accepted');
  EXCEPTION WHEN OTHERS THEN
    IF SQLCODE<>-20006 THEN RAISE; END IF;
    ROLLBACK TO batch_test;
  END;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND status='ISSUED';
  check_true(v_count=2,'Failed batch must preserve initial loans');
  SELECT status INTO v_status FROM book_copy WHERE copy_id=v_copy;
  check_true(v_status='AVAILABLE','Failed batch must restore copy availability');
  -- Direct inserts with a historical issue date also derive the deadline from that date.
  INSERT INTO issue_book(student_id,book_id,issue_date,status) VALUES(v_student,v_book,SYSDATE-2,'ISSUED') RETURNING issue_id INTO v_issue;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE issue_id=v_issue AND ABS(due_date-issue_date-15)<1/86400;
  check_true(v_count=1,'Default due date must be based on issue date, not today');
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: copies, loan limit, stock, returns, full payments, receipts');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Integration checks against Oracle. All test rows and changes are rolled back.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET SERVEROUTPUT ON</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>  v_student NUMBER; v_book NUMBER; v_issue NUMBER; v_fine NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  v_count NUMBER; v_total NUMBER; v_available NUMBER; v_copy NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  v_paid NUMBER; v_status VARCHAR2(20);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 8 | <code>  BEGIN IF NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 9 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)</code> | নতুন business/audit/sample row insert করার statement। |
| 11 | <code>  VALUES(&#x27;Circulation rollback test&#x27;,&#x27;QA&#x27;,&#x27;09999999999&#x27;,&#x27;circulation-rollback-test@invalid.test&#x27;,&#x27;unused&#x27;,&#x27;QA-ROLL-TEST&#x27;,&#x27;QA-REG-TEST&#x27;,&#x27;2025-2026&#x27;) RETURNING student_id INTO v_student;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 12 | <code>  SELECT MIN(book_id) INTO v_book FROM book WHERE available_quantity&gt;=4;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 13 | <code>  check_true(v_book IS NOT NULL,&#x27;A book with at least four available copies is required&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 14 | <code>  SELECT quantity,available_quantity INTO v_total,v_available FROM book WHERE book_id=v_book;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 15 | <code>  -- Stock additions/removal must also add/retire physical copies.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 16 | <code>  UPDATE book SET quantity=quantity+2,available_quantity=available_quantity+2 WHERE book_id=v_book;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 17 | <code>  SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=v_book AND status&lt;&gt;&#x27;RETIRED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 18 | <code>  check_true(v_count=v_total+2,&#x27;Stock add mismatch&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 19 | <code>  UPDATE book SET quantity=quantity-2,available_quantity=available_quantity-2 WHERE book_id=v_book;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 20 | <code>  SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=v_book AND status&lt;&gt;&#x27;RETIRED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 21 | <code>  check_true(v_count=v_total,&#x27;Stock reduction mismatch&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 22 | <code>  issue_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 23 | <code>  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND ABS(due_date-issue_date-15)&lt;1/86400;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 24 | <code>  check_true(v_count=1,&#x27;New loan must be due 15 days after issue&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 25 | <code>  issue_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>  issue_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>  SELECT COUNT(DISTINCT copy_id) INTO v_count FROM issue_book WHERE student_id=v_student AND status=&#x27;ISSUED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 28 | <code>  check_true(v_count=3,&#x27;Three distinct physical copies required&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 29 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 30 | <code>    issue_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 31 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Fourth loan unexpectedly accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 32 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20006 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 33 | <code>  SELECT MIN(issue_id) INTO v_issue FROM issue_book WHERE student_id=v_student;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 34 | <code>  SELECT copy_id INTO v_copy FROM issue_book WHERE issue_id=v_issue;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 35 | <code>  UPDATE issue_book SET due_date=TRUNC(SYSDATE)-10 WHERE issue_id=v_issue;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 36 | <code>  return_book_proc(v_issue);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>  SELECT status INTO v_status FROM book_copy WHERE copy_id=v_copy;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 38 | <code>  check_true(v_status=&#x27;AVAILABLE&#x27;,&#x27;Returned physical copy must become available&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 39 | <code>  SELECT available_quantity INTO v_count FROM book WHERE book_id=v_book;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 40 | <code>  check_true(v_count=v_available-2,&#x27;Only returned copy must restore stock&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 41 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 42 | <code>    return_book_proc(v_issue);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 43 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Double return accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 44 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20002 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 45 | <code>  SELECT fine_id,amount INTO v_fine,v_paid FROM fine WHERE issue_id=v_issue;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 46 | <code>  check_true(v_paid=100,&#x27;Final overdue fine incorrect&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 47 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 48 | <code>    pay_fine_proc(v_fine,35.25,&#x27;Partial payment attempt&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 49 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Partial payment accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 50 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20012 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 51 | <code>  SELECT paid_amount,payment_status INTO v_paid,v_status FROM fine WHERE fine_id=v_fine;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 52 | <code>  check_true(v_paid=0 AND v_status=&#x27;UNPAID&#x27;,&#x27;Rejected payment changed balance&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 53 | <code>  SELECT COUNT(*) INTO v_count FROM fine_payment WHERE fine_id=v_fine;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 54 | <code>  check_true(v_count=0,&#x27;Rejected payment created a receipt&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 55 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 56 | <code>    pay_fine_proc(v_fine,100.01);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 57 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Overpayment accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 58 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20012 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 59 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 60 | <code>    issue_book_proc(v_student,v_book,v_copy);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 61 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Unpaid fine did not block loan&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 62 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20007 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 63 | <code>  pay_fine_proc(v_fine);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 64 | <code>  SELECT paid_amount,payment_status INTO v_paid,v_status FROM fine WHERE fine_id=v_fine;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 65 | <code>  check_true(v_paid=100 AND v_status=&#x27;PAID&#x27;,&#x27;Final settlement incorrect&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 66 | <code>  SELECT COUNT(*) INTO v_count FROM fine_payment WHERE fine_id=v_fine;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 67 | <code>  check_true(v_count=1,&#x27;One full payment receipt required&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 68 | <code>  SELECT copy_id INTO v_count FROM issue_book WHERE issue_id=(SELECT MIN(issue_id) FROM issue_book WHERE student_id=v_student AND status=&#x27;ISSUED&#x27;);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 69 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 70 | <code>    issue_book_proc(v_student,v_book,v_count);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 71 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Already borrowed copy accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 72 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20010 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 73 | <code>  issue_book_proc(v_student,v_book,v_copy);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 74 | <code>  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND copy_id=v_copy;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 75 | <code>  check_true(v_count=2,&#x27;Returned copy should be reusable&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 76 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 77 | <code>    pay_fine_proc(v_fine);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 78 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Duplicate payment accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 79 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20011 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 80 | <code>  -- A failed selection must roll back earlier issues from the same request.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 81 | <code>  SELECT MAX(issue_id) INTO v_issue FROM issue_book WHERE student_id=v_student;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 82 | <code>  return_book_proc(v_issue);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 83 | <code>  SAVEPOINT batch_test;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 84 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 85 | <code>    issue_book_proc(v_student,v_book,v_copy);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 86 | <code>    issue_book_proc(v_student,v_book);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 87 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Failed batch unexpectedly accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 88 | <code>  EXCEPTION WHEN OTHERS THEN</code> | PL/SQL error branch; known conflict/no-data conditions handle করে। |
| 89 | <code>    IF SQLCODE&lt;&gt;-20006 THEN RAISE; END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 90 | <code>    ROLLBACK TO batch_test;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 91 | <code>  END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 92 | <code>  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND status=&#x27;ISSUED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 93 | <code>  check_true(v_count=2,&#x27;Failed batch must preserve initial loans&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 94 | <code>  SELECT status INTO v_status FROM book_copy WHERE copy_id=v_copy;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 95 | <code>  check_true(v_status=&#x27;AVAILABLE&#x27;,&#x27;Failed batch must restore copy availability&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 96 | <code>  -- Direct inserts with a historical issue date also derive the deadline from that date.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 97 | <code>  INSERT INTO issue_book(student_id,book_id,issue_date,status) VALUES(v_student,v_book,SYSDATE-2,&#x27;ISSUED&#x27;) RETURNING issue_id INTO v_issue;</code> | নতুন business/audit/sample row insert করার statement। |
| 98 | <code>  SELECT COUNT(*) INTO v_count FROM issue_book WHERE issue_id=v_issue AND ABS(due_date-issue_date-15)&lt;1/86400;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 99 | <code>  check_true(v_count=1,&#x27;Default due date must be based on issue date, not today&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 100 | <code>  ROLLBACK;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 101 | <code>  DBMS_OUTPUT.PUT_LINE(&#x27;PASS: copies, loan limit, stock, returns, full payments, receipts&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 102 | <code>EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 103 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 104 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
