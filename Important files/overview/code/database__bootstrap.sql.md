# database/bootstrap.sql

CONFIGURED_SCHEMA user তৈরি অথবা তার password reset/unlock করে এবং schema তৈরির privileges দেয়।

Source: [মূল file](../../database/bootstrap.sql)। Snapshot 2026-10-04; 18 lines; SHA-256 `6051b4e40dea9edcf1c853aaa2bec0c65868a2bba85c8db76d1351d272236e94`।

## Function / object / element inventory

- **VIEW `TO`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
-- Credentials are supplied as private bind variables by backend.setup_database.
SET SERVEROUTPUT ON;
WHENEVER SQLERROR EXIT SQL.SQLCODE;
DECLARE
  user_count NUMBER;
  account_name VARCHAR2(30) := DBMS_ASSERT.SIMPLE_SQL_NAME(:bootstrap_user);
  password_clause VARCHAR2(200) := ' IDENTIFIED BY "' || REPLACE(:bootstrap_password, '"', '""') || '"';
BEGIN
  SELECT COUNT(*) INTO user_count FROM dba_users WHERE username = UPPER(account_name);
  IF user_count = 0 THEN
    EXECUTE IMMEDIATE 'CREATE USER ' || account_name || password_clause;
  ELSE
    EXECUTE IMMEDIATE 'ALTER USER ' || account_name || password_clause || ' ACCOUNT UNLOCK';
  END IF;
  EXECUTE IMMEDIATE 'GRANT CONNECT, RESOURCE, CREATE VIEW TO ' || account_name;
END;
/
PROMPT Application schema is ready.
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Credentials are supplied as private bind variables by backend.setup_database.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET SERVEROUTPUT ON;</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>WHENEVER SQLERROR EXIT SQL.SQLCODE;</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 4 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  user_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  account_name VARCHAR2(30) := DBMS_ASSERT.SIMPLE_SQL_NAME(:bootstrap_user);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>  password_clause VARCHAR2(200) := &#x27; IDENTIFIED BY &quot;&#x27; &#124;&#124; REPLACE(:bootstrap_password, &#x27;&quot;&#x27;, &#x27;&quot;&quot;&#x27;) &#124;&#124; &#x27;&quot;&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>  SELECT COUNT(*) INTO user_count FROM dba_users WHERE username = UPPER(account_name);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 10 | <code>  IF user_count = 0 THEN</code> | PL/SQL condition/alternative branch। |
| 11 | <code>    EXECUTE IMMEDIATE &#x27;CREATE USER &#x27; &#124;&#124; account_name &#124;&#124; password_clause;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 12 | <code>  ELSE</code> | PL/SQL condition/alternative branch। |
| 13 | <code>    EXECUTE IMMEDIATE &#x27;ALTER USER &#x27; &#124;&#124; account_name &#124;&#124; password_clause &#124;&#124; &#x27; ACCOUNT UNLOCK&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 14 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 15 | <code>  EXECUTE IMMEDIATE &#x27;GRANT CONNECT, RESOURCE, CREATE VIEW TO &#x27; &#124;&#124; account_name;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 16 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 17 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 18 | <code>PROMPT Application schema is ready.</code> | Script progress/completion message output করে। |
