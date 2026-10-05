# database/schema/verify.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/verify.sql)। Snapshot 2026-10-04; 10 lines; SHA-256 `ffac4c5575c2596414f3a05558b1562c91bf31148a53c5d54962ca149a98aaae`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
DECLARE
  invalid_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO invalid_count FROM user_objects WHERE status = 'INVALID';
  IF invalid_count > 0 THEN
    RAISE_APPLICATION_ERROR(-20099, 'Invalid database objects; inspect USER_ERRORS');
  END IF;
END;
/
PROMPT Library Management System setup completed.
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 2 | <code>  invalid_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 3 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>  SELECT COUNT(*) INTO invalid_count FROM user_objects WHERE status = &#x27;INVALID&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 5 | <code>  IF invalid_count &gt; 0 THEN</code> | PL/SQL condition/alternative branch। |
| 6 | <code>    RAISE_APPLICATION_ERROR(-20099, &#x27;Invalid database objects; inspect USER_ERRORS&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 7 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 8 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 10 | <code>PROMPT Library Management System setup completed.</code> | Script progress/completion message output করে। |
