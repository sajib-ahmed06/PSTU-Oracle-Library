# tests/activation_oracle.sql

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/activation_oracle.sql)। Snapshot 2026-10-04; 38 lines; SHA-256 `da142a1935bc55c2c7927fec112d7f87d0f9260a34041010935cc5bc3bf89ddb`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
SET SERVEROUTPUT ON
DECLARE v_student NUMBER; v_count NUMBER; v_user NUMBER; v_hash VARCHAR2(255):='pbkdf2$activation-rollback-test';
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
BEGIN
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Activation QA','QA','09777777771','activation-qa@invalid.test','unused','ACT-QA1','ACT-REG1','2025-2026') RETURNING student_id INTO v_student;
  BEGIN activate_student_proc(v_student,'09777777772',v_hash); RAISE_APPLICATION_ERROR(-20999,'Wrong phone accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20040 THEN RAISE; END IF; END;
  BEGIN activate_student_proc(v_student,NULL,v_hash); RAISE_APPLICATION_ERROR(-20999,'Missing phone accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20040 THEN RAISE; END IF; END;
  BEGIN activate_student_proc(-1,'09777777771',v_hash); RAISE_APPLICATION_ERROR(-20999,'Unknown member accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20040 THEN RAISE; END IF; END;
  UPDATE student SET membership_status='DISABLED' WHERE student_id=v_student;
  BEGIN activate_student_proc(v_student,'09777777771',v_hash); RAISE_APPLICATION_ERROR(-20999,'Disabled member accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20005 THEN RAISE; END IF; END;
  UPDATE student SET membership_status='ACTIVE' WHERE student_id=v_student;
  activate_student_proc(v_student,'09777777771',v_hash);
  SELECT user_id INTO v_user FROM login_user WHERE student_id=v_student;
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND member_activated_at IS NOT NULL AND user_type='STUDENT' AND account_status='ACTIVE' AND password=v_hash;
  check_true(v_count=1,'Activation must create an active linked student account');
  BEGIN activate_student_proc(v_student,'09777777771','pbkdf2$replacement'); RAISE_APPLICATION_ERROR(-20999,'Repeat activation changed password');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20043 THEN RAISE; END IF; END;
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password=v_hash;
  check_true(v_count=1,'Original password must survive repeated activation');
  -- A pre-existing linked account is reused, preserving its ID.
  UPDATE login_user SET member_activated_at=NULL,password='old-password' WHERE user_id=v_user;
  activate_student_proc(v_student,'09777777771',v_hash);
  SELECT COUNT(*) INTO v_count FROM login_user WHERE student_id=v_student AND user_id=v_user AND password=v_hash;
  check_true(v_count=1,'Existing linked account must be reused');
  UPDATE login_user SET member_activated_at=NULL,account_status='DISABLED' WHERE user_id=v_user;
  BEGIN activate_student_proc(v_student,'09777777771',v_hash); RAISE_APPLICATION_ERROR(-20999,'Activation enabled a disabled account');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20042 THEN RAISE; END IF; END;
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: member/phone matching, one-time activation, disabled guards, existing account preservation');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>SET SERVEROUTPUT ON</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 2 | <code>DECLARE v_student NUMBER; v_count NUMBER; v_user NUMBER; v_hash VARCHAR2(255):=&#x27;pbkdf2$activation-rollback-test&#x27;;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 3 | <code>  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 4 | <code>  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 5 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)</code> | নতুন business/audit/sample row insert করার statement। |
| 7 | <code>    VALUES(&#x27;Activation QA&#x27;,&#x27;QA&#x27;,&#x27;09777777771&#x27;,&#x27;activation-qa@invalid.test&#x27;,&#x27;unused&#x27;,&#x27;ACT-QA1&#x27;,&#x27;ACT-REG1&#x27;,&#x27;2025-2026&#x27;) RETURNING student_id INTO v_student;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>  BEGIN activate_student_proc(v_student,&#x27;09777777772&#x27;,v_hash); RAISE_APPLICATION_ERROR(-20999,&#x27;Wrong phone accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 9 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20040 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 10 | <code>  BEGIN activate_student_proc(v_student,NULL,v_hash); RAISE_APPLICATION_ERROR(-20999,&#x27;Missing phone accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 11 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20040 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 12 | <code>  BEGIN activate_student_proc(-1,&#x27;09777777771&#x27;,v_hash); RAISE_APPLICATION_ERROR(-20999,&#x27;Unknown member accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 13 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20040 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 14 | <code>  UPDATE student SET membership_status=&#x27;DISABLED&#x27; WHERE student_id=v_student;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 15 | <code>  BEGIN activate_student_proc(v_student,&#x27;09777777771&#x27;,v_hash); RAISE_APPLICATION_ERROR(-20999,&#x27;Disabled member accepted&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 16 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20005 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 17 | <code>  UPDATE student SET membership_status=&#x27;ACTIVE&#x27; WHERE student_id=v_student;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 18 | <code>  activate_student_proc(v_student,&#x27;09777777771&#x27;,v_hash);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 19 | <code>  SELECT user_id INTO v_user FROM login_user WHERE student_id=v_student;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 20 | <code>  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND member_activated_at IS NOT NULL AND user_type=&#x27;STUDENT&#x27; AND account_status=&#x27;ACTIVE&#x27; AND password=v_hash;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 21 | <code>  check_true(v_count=1,&#x27;Activation must create an active linked student account&#x27;);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 22 | <code>  BEGIN activate_student_proc(v_student,&#x27;09777777771&#x27;,&#x27;pbkdf2$replacement&#x27;); RAISE_APPLICATION_ERROR(-20999,&#x27;Repeat activation changed password&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 23 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20043 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 24 | <code>  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password=v_hash;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 25 | <code>  check_true(v_count=1,&#x27;Original password must survive repeated activation&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 26 | <code>  -- A pre-existing linked account is reused, preserving its ID.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 27 | <code>  UPDATE login_user SET member_activated_at=NULL,password=&#x27;old-password&#x27; WHERE user_id=v_user;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 28 | <code>  activate_student_proc(v_student,&#x27;09777777771&#x27;,v_hash);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 29 | <code>  SELECT COUNT(*) INTO v_count FROM login_user WHERE student_id=v_student AND user_id=v_user AND password=v_hash;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 30 | <code>  check_true(v_count=1,&#x27;Existing linked account must be reused&#x27;);</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 31 | <code>  UPDATE login_user SET member_activated_at=NULL,account_status=&#x27;DISABLED&#x27; WHERE user_id=v_user;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 32 | <code>  BEGIN activate_student_proc(v_student,&#x27;09777777771&#x27;,v_hash); RAISE_APPLICATION_ERROR(-20999,&#x27;Activation enabled a disabled account&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 33 | <code>  EXCEPTION WHEN OTHERS THEN IF SQLCODE&lt;&gt;-20042 THEN RAISE; END IF; END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 34 | <code>  ROLLBACK;</code> | Uncommitted business/audit changes undo করে; sequence values ফেরত যায় না। |
| 35 | <code>  DBMS_OUTPUT.PUT_LINE(&#x27;PASS: member/phone matching, one-time activation, disabled guards, existing account preservation&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 37 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 38 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
