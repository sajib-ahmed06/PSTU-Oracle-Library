# database/schema/reset.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/reset.sql)। Snapshot 2026-10-04; 28 lines; SHA-256 `bc38b2fefffda566d125588f7df80ab723aa2d46ad44b6ece2e1ff6905e6674d`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
-- PSTU Library: fresh schema and sample data.
-- Run through Setup-Database.bat; this script resets the project tables.

SET DEFINE OFF;
SET SERVEROUTPUT ON;
WHENEVER OSERROR EXIT FAILURE;
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;

BEGIN
  FOR scheduled_job IN (SELECT job FROM user_jobs WHERE what='expire_reservations_proc;') LOOP
    DBMS_JOB.REMOVE(scheduled_job.job);
  END LOOP;
  FOR object_name IN (SELECT object_name, object_type FROM user_objects
    WHERE object_name IN ('AUDIT_JSON_VALUE','RETURN_BOOK_PROC','CHECK_BOOK_AVAILABLE','BOOK_DETAILS','RETURN_QUANTITY_TRIGGER','ISSUE_QUANTITY_TRIGGER','LOGIN_TRIGGER','RETURN_TRIGGER','ISSUE_TRIGGER','BOOK_TRIGGER','CATEGORY_TRIGGER','AUTHOR_TRIGGER','STUDENT_TRIGGER','ADMIN_TRIGGER')) LOOP
    BEGIN
      EXECUTE IMMEDIATE 'DROP ' || object_name.object_type || ' ' || object_name.object_name;
    EXCEPTION WHEN OTHERS THEN NULL;
    END;
  END LOOP;
  FOR table_name IN (SELECT table_name FROM user_tables WHERE table_name IN ('REMINDER_DELIVERY','BOOK_RESERVATION','FINE_PAYMENT','BOOK_COPY','AUDIT_LOG','FINE','RETURN_BOOK','ISSUE_BOOK','BOOK','CATEGORY','AUTHOR','LOGIN_USER','STUDENT','ADMIN')) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || table_name.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
  FOR sequence_name IN (SELECT sequence_name FROM user_sequences WHERE sequence_name IN ('RESERVATION_SEQ','PAYMENT_SEQ','COPY_SEQ','AUDIT_SEQ','FINE_SEQ','RETURN_SEQ','ISSUE_SEQ','BOOK_SEQ','CATEGORY_SEQ','AUTHOR_SEQ','LOGIN_SEQ','STUDENT_SEQ','ADMIN_SEQ')) LOOP
    EXECUTE IMMEDIATE 'DROP SEQUENCE ' || sequence_name.sequence_name;
  END LOOP;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- PSTU Library: fresh schema and sample data.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>-- Run through Setup-Database.bat; this script resets the project tables.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 3 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 4 | <code>SET DEFINE OFF;</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 5 | <code>SET SERVEROUTPUT ON;</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 6 | <code>WHENEVER OSERROR EXIT FAILURE;</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 7 | <code>WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>  FOR scheduled_job IN (SELECT job FROM user_jobs WHERE what=&#x27;expire_reservations_proc;&#x27;) LOOP</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 11 | <code>    DBMS_JOB.REMOVE(scheduled_job.job);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 12 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 13 | <code>  FOR object_name IN (SELECT object_name, object_type FROM user_objects</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 14 | <code>    WHERE object_name IN (&#x27;AUDIT_JSON_VALUE&#x27;,&#x27;RETURN_BOOK_PROC&#x27;,&#x27;CHECK_BOOK_AVAILABLE&#x27;,&#x27;BOOK_DETAILS&#x27;,&#x27;RETURN_QUANTITY_TRIGGER&#x27;,&#x27;ISSUE_QUANTITY_TRIGGER&#x27;,&#x27;LOGIN_TRIGGER&#x27;,&#x27;RETURN_TRIGGER&#x27;,&#x27;ISSUE_TRIGGER&#x27;,&#x27;BOOK_TRIGGER&#x27;,&#x27;CATEGORY_TRIGGER&#x27;,&#x27;AUTHOR_TRIGGER&#x27;,&#x27;STUDENT_TRIGGER&#x27;,&#x27;ADMIN_TRIGGER&#x27;)) LOOP</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 15 | <code>    BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 16 | <code>      EXECUTE IMMEDIATE &#x27;DROP &#x27; &#124;&#124; object_name.object_type &#124;&#124; &#x27; &#x27; &#124;&#124; object_name.object_name;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 17 | <code>    EXCEPTION WHEN OTHERS THEN NULL;</code> | PL/SQL error branch; known conflict/no-data conditions handle করে। |
| 18 | <code>    END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 19 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 20 | <code>  FOR table_name IN (SELECT table_name FROM user_tables WHERE table_name IN (&#x27;REMINDER_DELIVERY&#x27;,&#x27;BOOK_RESERVATION&#x27;,&#x27;FINE_PAYMENT&#x27;,&#x27;BOOK_COPY&#x27;,&#x27;AUDIT_LOG&#x27;,&#x27;FINE&#x27;,&#x27;RETURN_BOOK&#x27;,&#x27;ISSUE_BOOK&#x27;,&#x27;BOOK&#x27;,&#x27;CATEGORY&#x27;,&#x27;AUTHOR&#x27;,&#x27;LOGIN_USER&#x27;,&#x27;STUDENT&#x27;,&#x27;ADMIN&#x27;)) LOOP</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 21 | <code>    EXECUTE IMMEDIATE &#x27;DROP TABLE &#x27; &#124;&#124; table_name.table_name &#124;&#124; &#x27; CASCADE CONSTRAINTS&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 23 | <code>  FOR sequence_name IN (SELECT sequence_name FROM user_sequences WHERE sequence_name IN (&#x27;RESERVATION_SEQ&#x27;,&#x27;PAYMENT_SEQ&#x27;,&#x27;COPY_SEQ&#x27;,&#x27;AUDIT_SEQ&#x27;,&#x27;FINE_SEQ&#x27;,&#x27;RETURN_SEQ&#x27;,&#x27;ISSUE_SEQ&#x27;,&#x27;BOOK_SEQ&#x27;,&#x27;CATEGORY_SEQ&#x27;,&#x27;AUTHOR_SEQ&#x27;,&#x27;LOGIN_SEQ&#x27;,&#x27;STUDENT_SEQ&#x27;,&#x27;ADMIN_SEQ&#x27;)) LOOP</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 24 | <code>    EXECUTE IMMEDIATE &#x27;DROP SEQUENCE &#x27; &#124;&#124; sequence_name.sequence_name;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 25 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
