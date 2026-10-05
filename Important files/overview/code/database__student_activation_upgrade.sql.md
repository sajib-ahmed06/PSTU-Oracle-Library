# database/student_activation_upgrade.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/student_activation_upgrade.sql)। Snapshot 2026-10-04; 52 lines; SHA-256 `85265f8959b1d5eae7b541ca59a1372295e0631d3d0a6d41a9ced866c6fc9b0f`।

## Function / object / element inventory

- **PROCEDURE `activate_student_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `reset_student_password_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
-- First-time student activation; preserves existing accounts and passwords.
SET DEFINE OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
DECLARE n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name='LOGIN_USER' AND column_name='MEMBER_ACTIVATED_AT';
  IF n=0 THEN EXECUTE IMMEDIATE 'ALTER TABLE login_user ADD (member_activated_at DATE)'; END IF;
END;
/
CREATE OR REPLACE PROCEDURE activate_student_proc(p_student_id NUMBER,p_phone VARCHAR2,p_password_hash VARCHAR2) AS
  v_phone VARCHAR2(11); v_membership VARCHAR2(20); v_user NUMBER;
  v_activated DATE; v_status VARCHAR2(20); v_username VARCHAR2(100);
BEGIN
  BEGIN
    SELECT phone,membership_status INTO v_phone,v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20040,'Member ID or registered phone number does not match'); END;
  IF p_phone IS NULL OR v_phone<>p_phone THEN RAISE_APPLICATION_ERROR(-20040,'Member ID or registered phone number does not match'); END IF;
  IF v_membership<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)<>'pbkdf2$' THEN RAISE_APPLICATION_ERROR(-20041,'Invalid password hash'); END IF;
  v_username:='PSTU-'||LPAD(TO_CHAR(p_student_id,'FM99999999999999999990'),GREATEST(4,LENGTH(TO_CHAR(p_student_id,'FM99999999999999999990'))),'0');
  BEGIN
    SELECT user_id,member_activated_at,account_status INTO v_user,v_activated,v_status FROM login_user WHERE student_id=p_student_id AND user_type='STUDENT' FOR UPDATE;
    IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20042,'This account is disabled. Contact the library desk'); END IF;
    IF v_activated IS NOT NULL THEN RAISE_APPLICATION_ERROR(-20043,'Account already activated. Sign in with your Member ID and password'); END IF;
    UPDATE login_user SET username=v_username,password=p_password_hash,member_activated_at=SYSDATE WHERE user_id=v_user;
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO login_user(username,password,user_type,account_status,student_id,member_activated_at)
      VALUES(v_username,p_password_hash,'STUDENT','ACTIVE',p_student_id,SYSDATE);
  END;
END;
/
CREATE OR REPLACE PROCEDURE reset_student_password_proc(p_student_id NUMBER,p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2,p_password_hash VARCHAR2) AS
  v_count NUMBER; v_lock NUMBER; v_user NUMBER; v_status VARCHAR2(20);
BEGIN
  BEGIN
    SELECT student_id INTO v_lock FROM student WHERE student_id=p_student_id FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20044,'Member details do not match'); END;
  SELECT COUNT(*) INTO v_count FROM student WHERE student_id=p_student_id
    AND UPPER(TRIM(roll_no))=UPPER(TRIM(p_roll)) AND UPPER(TRIM(registration_no))=UPPER(TRIM(p_registration))
    AND phone=p_phone AND LOWER(TRIM(email))=LOWER(TRIM(p_email));
  IF v_count<>1 THEN RAISE_APPLICATION_ERROR(-20044,'Member details do not match'); END IF;
  SELECT membership_status INTO v_status FROM student WHERE student_id=p_student_id;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  BEGIN
    SELECT user_id,account_status INTO v_user,v_status FROM login_user WHERE student_id=p_student_id AND user_type='STUDENT' FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20045,'Activate your member account before resetting its password'); END;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20042,'This account is disabled. Contact the library desk'); END IF;
  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)<>'pbkdf2$' THEN RAISE_APPLICATION_ERROR(-20041,'Invalid password hash'); END IF;
  UPDATE login_user SET password=p_password_hash,member_activated_at=NVL(member_activated_at,SYSDATE) WHERE user_id=v_user;
END;
/
COMMIT;
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- First-time student activation; preserves existing accounts and passwords.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET DEFINE OFF</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 4 | <code>DECLARE n NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name=&#x27;LOGIN_USER&#x27; AND column_name=&#x27;MEMBER_ACTIVATED_AT&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 7 | <code>  IF n=0 THEN EXECUTE IMMEDIATE &#x27;ALTER TABLE login_user ADD (member_activated_at DATE)&#x27;; END IF;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 8 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 10 | <code>CREATE OR REPLACE PROCEDURE activate_student_proc(p_student_id NUMBER,p_phone VARCHAR2,p_password_hash VARCHAR2) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 11 | <code>  v_phone VARCHAR2(11); v_membership VARCHAR2(20); v_user NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 12 | <code>  v_activated DATE; v_status VARCHAR2(20); v_username VARCHAR2(100);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 13 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 14 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 15 | <code>    SELECT phone,membership_status INTO v_phone,v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 16 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20040,&#x27;Member ID or registered phone number does not match&#x27;); END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 17 | <code>  IF p_phone IS NULL OR v_phone&lt;&gt;p_phone THEN RAISE_APPLICATION_ERROR(-20040,&#x27;Member ID or registered phone number does not match&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 18 | <code>  IF v_membership&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20005,&#x27;This membership is disabled&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 19 | <code>  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)&lt;&gt;&#x27;pbkdf2$&#x27; THEN RAISE_APPLICATION_ERROR(-20041,&#x27;Invalid password hash&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 20 | <code>  v_username:=&#x27;PSTU-&#x27;&#124;&#124;LPAD(TO_CHAR(p_student_id,&#x27;FM99999999999999999990&#x27;),GREATEST(4,LENGTH(TO_CHAR(p_student_id,&#x27;FM99999999999999999990&#x27;))),&#x27;0&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>    SELECT user_id,member_activated_at,account_status INTO v_user,v_activated,v_status FROM login_user WHERE student_id=p_student_id AND user_type=&#x27;STUDENT&#x27; FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 23 | <code>    IF v_status&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20042,&#x27;This account is disabled. Contact the library desk&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 24 | <code>    IF v_activated IS NOT NULL THEN RAISE_APPLICATION_ERROR(-20043,&#x27;Account already activated. Sign in with your Member ID and password&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 25 | <code>    UPDATE login_user SET username=v_username,password=p_password_hash,member_activated_at=SYSDATE WHERE user_id=v_user;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 26 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN</code> | PL/SQL error branch; known conflict/no-data conditions handle করে। |
| 27 | <code>    INSERT INTO login_user(username,password,user_type,account_status,student_id,member_activated_at)</code> | নতুন business/audit/sample row insert করার statement। |
| 28 | <code>      VALUES(v_username,p_password_hash,&#x27;STUDENT&#x27;,&#x27;ACTIVE&#x27;,p_student_id,SYSDATE);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 29 | <code>  END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 30 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 31 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 32 | <code>CREATE OR REPLACE PROCEDURE reset_student_password_proc(p_student_id NUMBER,p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2,p_password_hash VARCHAR2) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 33 | <code>  v_count NUMBER; v_lock NUMBER; v_user NUMBER; v_status VARCHAR2(20);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 34 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 35 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>    SELECT student_id INTO v_lock FROM student WHERE student_id=p_student_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 37 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20044,&#x27;Member details do not match&#x27;); END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 38 | <code>  SELECT COUNT(*) INTO v_count FROM student WHERE student_id=p_student_id</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 39 | <code>    AND UPPER(TRIM(roll_no))=UPPER(TRIM(p_roll)) AND UPPER(TRIM(registration_no))=UPPER(TRIM(p_registration))</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>    AND phone=p_phone AND LOWER(TRIM(email))=LOWER(TRIM(p_email));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 41 | <code>  IF v_count&lt;&gt;1 THEN RAISE_APPLICATION_ERROR(-20044,&#x27;Member details do not match&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 42 | <code>  SELECT membership_status INTO v_status FROM student WHERE student_id=p_student_id;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 43 | <code>  IF v_status&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20005,&#x27;This membership is disabled&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 44 | <code>  BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 45 | <code>    SELECT user_id,account_status INTO v_user,v_status FROM login_user WHERE student_id=p_student_id AND user_type=&#x27;STUDENT&#x27; FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 46 | <code>  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20045,&#x27;Activate your member account before resetting its password&#x27;); END;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 47 | <code>  IF v_status&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20042,&#x27;This account is disabled. Contact the library desk&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 48 | <code>  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)&lt;&gt;&#x27;pbkdf2$&#x27; THEN RAISE_APPLICATION_ERROR(-20041,&#x27;Invalid password hash&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 49 | <code>  UPDATE login_user SET password=p_password_hash,member_activated_at=NVL(member_activated_at,SYSDATE) WHERE user_id=v_user;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 50 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 51 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 52 | <code>COMMIT;</code> | Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ। |
