# database/schema/members.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/members.sql)। Snapshot 2026-10-04; 97 lines; SHA-256 `f78178d8295c9c0562f707c599cbe798221afc72f4d875dd37af16284200682c`।

## Function / object / element inventory

- **TABLE `admin`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `admin_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `admin_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TABLE `student`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `student_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `student_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TRIGGER `student_session_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TRIGGER `student_identity_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `add_student_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
-- People and membership
CREATE TABLE admin (
  admin_id NUMBER PRIMARY KEY,
  name VARCHAR2(100) NOT NULL,
  email VARCHAR2(100) NOT NULL UNIQUE,
  password VARCHAR2(255) NOT NULL
);
CREATE SEQUENCE admin_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER admin_trigger BEFORE INSERT ON admin FOR EACH ROW
BEGIN
  IF :NEW.admin_id IS NULL THEN
    SELECT admin_seq.NEXTVAL INTO :NEW.admin_id FROM dual;
  END IF;
END;
/

CREATE TABLE student (
  student_id NUMBER PRIMARY KEY,
  name VARCHAR2(100) NOT NULL,
  department VARCHAR2(100) NOT NULL,
  phone VARCHAR2(11) NOT NULL UNIQUE,
  email VARCHAR2(100) NOT NULL UNIQUE,
  password VARCHAR2(255) NOT NULL,
  roll_no VARCHAR2(40) NOT NULL,
  registration_no VARCHAR2(40) NOT NULL,
  academic_session VARCHAR2(9) NOT NULL,
  membership_status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL,
  CONSTRAINT ck_student_membership CHECK (membership_status IN ('ACTIVE', 'DISABLED')),
  CONSTRAINT ck_student_phone CHECK (
    LENGTH(phone) = 11 AND TRIM(TRANSLATE(phone, '0123456789', ' ')) IS NULL
  )
);
CREATE SEQUENCE student_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER student_trigger BEFORE INSERT ON student FOR EACH ROW
BEGIN
  IF :NEW.student_id IS NULL THEN
    SELECT student_seq.NEXTVAL INTO :NEW.student_id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER student_session_trigger
BEFORE INSERT OR UPDATE OF academic_session ON student
FOR EACH ROW
BEGIN
  :NEW.academic_session := TRIM(:NEW.academic_session);
  IF :NEW.academic_session IS NULL THEN
    RAISE_APPLICATION_ERROR(-20022, 'Academic session is required');
  END IF;
  IF REGEXP_LIKE(:NEW.academic_session, '^[0-9]{4}-[0-9]{2}$') THEN
    IF TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1 > 9999 OR
       TO_NUMBER(SUBSTR(:NEW.academic_session,6,2)) <> MOD(TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1,100) THEN
      RAISE_APPLICATION_ERROR(-20023, 'Academic session must cover consecutive years');
    END IF;
    :NEW.academic_session := SUBSTR(:NEW.academic_session,1,5) ||
      TO_CHAR(TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1,'FM0000');
  END IF;
  IF NOT REGEXP_LIKE(:NEW.academic_session, '^[0-9]{4}-[0-9]{4}$') THEN
    RAISE_APPLICATION_ERROR(-20023, 'Academic session must use YYYY-YY or YYYY-YYYY');
  END IF;
  IF TO_NUMBER(SUBSTR(:NEW.academic_session,6,4)) <> TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1 THEN
    RAISE_APPLICATION_ERROR(-20023, 'Academic session must cover consecutive years');
  END IF;
END;
/
CREATE OR REPLACE TRIGGER student_identity_trigger
BEFORE INSERT OR UPDATE OF roll_no, registration_no ON student
FOR EACH ROW
BEGIN
  :NEW.roll_no := UPPER(TRIM(:NEW.roll_no));
  :NEW.registration_no := UPPER(TRIM(:NEW.registration_no));
  IF :NEW.roll_no IS NULL OR :NEW.registration_no IS NULL THEN
    RAISE_APPLICATION_ERROR(-20020, 'Both ID/Roll and Registration No. are required');
  END IF;
  IF NOT REGEXP_LIKE(:NEW.roll_no, '^[A-Z0-9][A-Z0-9./_-]{0,39}$') OR
     NOT REGEXP_LIKE(:NEW.registration_no, '^[A-Z0-9][A-Z0-9./_-]{0,39}$') THEN
    RAISE_APPLICATION_ERROR(-20021, 'Invalid ID/Roll or Registration No.');
  END IF;
END;
/
CREATE OR REPLACE PROCEDURE add_student_proc(
  p_name VARCHAR2,
  p_department VARCHAR2,
  p_phone VARCHAR2,
  p_email VARCHAR2,
  p_password VARCHAR2,
  p_roll_no VARCHAR2 DEFAULT NULL,
  p_registration_no VARCHAR2 DEFAULT NULL,
  p_academic_session VARCHAR2 DEFAULT NULL
) AS
BEGIN
  INSERT INTO student(name, department, phone, email, password, roll_no, registration_no, academic_session)
  VALUES(TRIM(p_name), TRIM(p_department), TRIM(p_phone), LOWER(TRIM(p_email)),
         p_password, UPPER(TRIM(p_roll_no)), UPPER(TRIM(p_registration_no)), TRIM(p_academic_session));
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- People and membership</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>CREATE TABLE admin (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 3 | <code>  admin_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 4 | <code>  name VARCHAR2(100) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  email VARCHAR2(100) NOT NULL UNIQUE,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 6 | <code>  password VARCHAR2(255) NOT NULL</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>CREATE SEQUENCE admin_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 9 | <code>CREATE OR REPLACE TRIGGER admin_trigger BEFORE INSERT ON admin FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 10 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>  IF :NEW.admin_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 12 | <code>    SELECT admin_seq.NEXTVAL INTO :NEW.admin_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 13 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 14 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 15 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>CREATE TABLE student (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 18 | <code>  student_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 19 | <code>  name VARCHAR2(100) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 20 | <code>  department VARCHAR2(100) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>  phone VARCHAR2(11) NOT NULL UNIQUE,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 22 | <code>  email VARCHAR2(100) NOT NULL UNIQUE,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 23 | <code>  password VARCHAR2(255) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>  roll_no VARCHAR2(40) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 25 | <code>  registration_no VARCHAR2(40) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>  academic_session VARCHAR2(9) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>  membership_status VARCHAR2(20) DEFAULT &#x27;ACTIVE&#x27; NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 28 | <code>  CONSTRAINT ck_student_membership CHECK (membership_status IN (&#x27;ACTIVE&#x27;, &#x27;DISABLED&#x27;)),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 29 | <code>  CONSTRAINT ck_student_phone CHECK (</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 30 | <code>    LENGTH(phone) = 11 AND TRIM(TRANSLATE(phone, &#x27;0123456789&#x27;, &#x27; &#x27;)) IS NULL</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 31 | <code>  )</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 32 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 33 | <code>CREATE SEQUENCE student_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 34 | <code>CREATE OR REPLACE TRIGGER student_trigger BEFORE INSERT ON student FOR EACH ROW</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 35 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>  IF :NEW.student_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 37 | <code>    SELECT student_seq.NEXTVAL INTO :NEW.student_id FROM dual;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 38 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 39 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 41 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 42 | <code>CREATE OR REPLACE TRIGGER student_session_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 43 | <code>BEFORE INSERT OR UPDATE OF academic_session ON student</code> | নতুন business/audit/sample row insert করার statement। |
| 44 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 45 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 46 | <code>  :NEW.academic_session := TRIM(:NEW.academic_session);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 47 | <code>  IF :NEW.academic_session IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 48 | <code>    RAISE_APPLICATION_ERROR(-20022, &#x27;Academic session is required&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 49 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 50 | <code>  IF REGEXP_LIKE(:NEW.academic_session, &#x27;^[0-9]{4}-[0-9]{2}$&#x27;) THEN</code> | PL/SQL condition/alternative branch। |
| 51 | <code>    IF TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1 &gt; 9999 OR</code> | PL/SQL condition/alternative branch। |
| 52 | <code>       TO_NUMBER(SUBSTR(:NEW.academic_session,6,2)) &lt;&gt; MOD(TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1,100) THEN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 53 | <code>      RAISE_APPLICATION_ERROR(-20023, &#x27;Academic session must cover consecutive years&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 54 | <code>    END IF;</code> | PL/SQL condition/alternative branch। |
| 55 | <code>    :NEW.academic_session := SUBSTR(:NEW.academic_session,1,5) &#124;&#124;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 56 | <code>      TO_CHAR(TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1,&#x27;FM0000&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 57 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 58 | <code>  IF NOT REGEXP_LIKE(:NEW.academic_session, &#x27;^[0-9]{4}-[0-9]{4}$&#x27;) THEN</code> | PL/SQL condition/alternative branch। |
| 59 | <code>    RAISE_APPLICATION_ERROR(-20023, &#x27;Academic session must use YYYY-YY or YYYY-YYYY&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 60 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 61 | <code>  IF TO_NUMBER(SUBSTR(:NEW.academic_session,6,4)) &lt;&gt; TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1 THEN</code> | PL/SQL condition/alternative branch। |
| 62 | <code>    RAISE_APPLICATION_ERROR(-20023, &#x27;Academic session must cover consecutive years&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 63 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 64 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 65 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 66 | <code>CREATE OR REPLACE TRIGGER student_identity_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 67 | <code>BEFORE INSERT OR UPDATE OF roll_no, registration_no ON student</code> | নতুন business/audit/sample row insert করার statement। |
| 68 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 69 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 70 | <code>  :NEW.roll_no := UPPER(TRIM(:NEW.roll_no));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 71 | <code>  :NEW.registration_no := UPPER(TRIM(:NEW.registration_no));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 72 | <code>  IF :NEW.roll_no IS NULL OR :NEW.registration_no IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 73 | <code>    RAISE_APPLICATION_ERROR(-20020, &#x27;Both ID/Roll and Registration No. are required&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 74 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 75 | <code>  IF NOT REGEXP_LIKE(:NEW.roll_no, &#x27;^[A-Z0-9][A-Z0-9./_-]{0,39}$&#x27;) OR</code> | PL/SQL condition/alternative branch। |
| 76 | <code>     NOT REGEXP_LIKE(:NEW.registration_no, &#x27;^[A-Z0-9][A-Z0-9./_-]{0,39}$&#x27;) THEN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 77 | <code>    RAISE_APPLICATION_ERROR(-20021, &#x27;Invalid ID/Roll or Registration No.&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 78 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 79 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 80 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 81 | <code>CREATE OR REPLACE PROCEDURE add_student_proc(</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 82 | <code>  p_name VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 83 | <code>  p_department VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 84 | <code>  p_phone VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 85 | <code>  p_email VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 86 | <code>  p_password VARCHAR2,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 87 | <code>  p_roll_no VARCHAR2 DEFAULT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 88 | <code>  p_registration_no VARCHAR2 DEFAULT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 89 | <code>  p_academic_session VARCHAR2 DEFAULT NULL</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 90 | <code>) AS</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 91 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 92 | <code>  INSERT INTO student(name, department, phone, email, password, roll_no, registration_no, academic_session)</code> | নতুন business/audit/sample row insert করার statement। |
| 93 | <code>  VALUES(TRIM(p_name), TRIM(p_department), TRIM(p_phone), LOWER(TRIM(p_email)),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 94 | <code>         p_password, UPPER(TRIM(p_roll_no)), UPPER(TRIM(p_registration_no)), TRIM(p_academic_session));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 95 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 96 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 97 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
