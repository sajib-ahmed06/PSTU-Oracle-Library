# tests/recovery_oracle.sql

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/recovery_oracle.sql)। Snapshot 2026-10-04; 39 lines; SHA-256 `f252026e83817b58e911484049b753e91174ab13fd75c8d5655109146ad0c21a`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
SET SERVEROUTPUT ON
DECLARE v_student NUMBER; v_user NUMBER; v_staff NUMBER; v_count NUMBER;
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
  PROCEDURE mismatch(p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2) IS
  BEGIN
    BEGIN reset_student_password_proc(v_student,p_roll,p_registration,p_phone,p_email,'pbkdf2$bad-attempt');
      RAISE_APPLICATION_ERROR(-20999,'Incorrect identity detail accepted');
    EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20044 THEN RAISE; END IF; END;
  END;
BEGIN
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Recovery QA','QA','09666666661','recovery-qa@invalid.test','unused','REC-QA1','REC-REG1','2025-2026') RETURNING student_id INTO v_student;
  INSERT INTO login_user(username,password,user_type) VALUES('recovery_qa_admin','staff-original','ADMIN') RETURNING user_id INTO v_staff;
  BEGIN reset_student_password_proc(v_student,'REC-QA1','REC-REG1','09666666661','recovery-qa@invalid.test','pbkdf2$new');
    RAISE_APPLICATION_ERROR(-20999,'Recovery created an account before activation');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20045 THEN RAISE; END IF; END;
  activate_student_proc(v_student,'09666666661','pbkdf2$original');
  SELECT user_id INTO v_user FROM login_user WHERE student_id=v_student;
  mismatch('wrong','REC-REG1','09666666661','recovery-qa@invalid.test');
  mismatch('REC-QA1','wrong','09666666661','recovery-qa@invalid.test');
  mismatch('REC-QA1','REC-REG1','09666666662','recovery-qa@invalid.test');
  mismatch('REC-QA1','REC-REG1','09666666661','wrong@invalid.test');
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password='pbkdf2$original';
  check_true(v_count=1,'Rejected recovery changed the password');
  reset_student_password_proc(v_student,' rec-qa1 ','rec-reg1','09666666661','RECOVERY-QA@INVALID.TEST','pbkdf2$new');
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password='pbkdf2$new' AND user_type='STUDENT';
  check_true(v_count=1,'Matching identity must reset the linked student password');
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_staff AND password='staff-original';
  check_true(v_count=1,'Recovery changed a staff password');
  UPDATE login_user SET account_status='DISABLED' WHERE user_id=v_user;
  BEGIN reset_student_password_proc(v_student,'REC-QA1','REC-REG1','09666666661','recovery-qa@invalid.test','pbkdf2$disabled');
    RAISE_APPLICATION_ERROR(-20999,'Recovery enabled a disabled account');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20042 THEN RAISE; END IF; END;
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: all identity fields, member-only recovery, account preservation, disabled guard');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>SET SERVEROUTPUT ON</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 2 | <code>DECLARE v_student NUMBER; v_user NUMBER; v_staff NUMBER; v_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 3 | <code>  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 4 | <code>  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 5 | <code>  PROCEDURE mismatch(p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2) IS</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>    BEGIN reset_student_password_proc(v_student,p_roll,p_registration,p_phone,p_email,&#x27;pbkdf2$bad-attempt&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>      RAISE_APPLICATION_ERROR(-20999,&#x27;Incorrect identity detail accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 9 | <code>    EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20044 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 10 | <code>  END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 12 | <code>  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)</code> | নতুন business/audit/sample row insert করার statement। |
| 13 | <code>    VALUES(&#x27;Recovery QA&#x27;,&#x27;QA&#x27;,&#x27;09666666661&#x27;,&#x27;recovery-qa@invalid.test&#x27;,&#x27;unused&#x27;,&#x27;REC-QA1&#x27;,&#x27;REC-REG1&#x27;,&#x27;2025-2026&#x27;) RETURNING student_id INTO v_student;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 14 | <code>  INSERT INTO login_user(username,password,user_type) VALUES(&#x27;recovery_qa_admin&#x27;,&#x27;staff-original&#x27;,&#x27;ADMIN&#x27;) RETURNING user_id INTO v_staff;</code> | নতুন business/audit/sample row insert করার statement। |
| 15 | <code>  BEGIN reset_student_password_proc(v_student,&#x27;REC-QA1&#x27;,&#x27;REC-REG1&#x27;,&#x27;09666666661&#x27;,&#x27;recovery-qa@invalid.test&#x27;,&#x27;pbkdf2$new&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 16 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Recovery created an account before activation&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 17 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20045 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 18 | <code>  activate_student_proc(v_student,&#x27;09666666661&#x27;,&#x27;pbkdf2$original&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 19 | <code>  SELECT user_id INTO v_user FROM login_user WHERE student_id=v_student;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 20 | <code>  mismatch(&#x27;wrong&#x27;,&#x27;REC-REG1&#x27;,&#x27;09666666661&#x27;,&#x27;recovery-qa@invalid.test&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>  mismatch(&#x27;REC-QA1&#x27;,&#x27;wrong&#x27;,&#x27;09666666661&#x27;,&#x27;recovery-qa@invalid.test&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>  mismatch(&#x27;REC-QA1&#x27;,&#x27;REC-REG1&#x27;,&#x27;09666666662&#x27;,&#x27;recovery-qa@invalid.test&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 23 | <code>  mismatch(&#x27;REC-QA1&#x27;,&#x27;REC-REG1&#x27;,&#x27;09666666661&#x27;,&#x27;wrong@invalid.test&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password=&#x27;pbkdf2$original&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 25 | <code>  check_true(v_count=1,&#x27;Rejected recovery changed the password&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 26 | <code>  reset_student_password_proc(v_student,&#x27; rec-qa1 &#x27;,&#x27;rec-reg1&#x27;,&#x27;09666666661&#x27;,&#x27;RECOVERY-QA@INVALID.TEST&#x27;,&#x27;pbkdf2$new&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password=&#x27;pbkdf2$new&#x27; AND user_type=&#x27;STUDENT&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 28 | <code>  check_true(v_count=1,&#x27;Matching identity must reset the linked student password&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 29 | <code>  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_staff AND password=&#x27;staff-original&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 30 | <code>  check_true(v_count=1,&#x27;Recovery changed a staff password&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 31 | <code>  UPDATE login_user SET account_status=&#x27;DISABLED&#x27; WHERE user_id=v_user;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 32 | <code>  BEGIN reset_student_password_proc(v_student,&#x27;REC-QA1&#x27;,&#x27;REC-REG1&#x27;,&#x27;09666666661&#x27;,&#x27;recovery-qa@invalid.test&#x27;,&#x27;pbkdf2$disabled&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 33 | <code>    RAISE_APPLICATION_ERROR(-20999,&#x27;Recovery enabled a disabled account&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 34 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20042 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 35 | <code>  ROLLBACK;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 36 | <code>  DBMS_OUTPUT.PUT_LINE(&#x27;PASS: all identity fields, member-only recovery, account preservation, disabled guard&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 38 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 39 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
