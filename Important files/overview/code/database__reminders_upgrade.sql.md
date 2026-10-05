# database/reminders_upgrade.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/reminders_upgrade.sql)। Snapshot 2026-10-04; 21 lines; SHA-256 `acf58d2ca5c4f02084102e97afb7e5d17123afcbd90bc67b6d2f249e0a4002bf`।

## Function / object / element inventory

- **TABLE `reminder_delivery`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

```sql
-- Delivery tracking only; existing loans, fines and member records are preserved.
DECLARE
  table_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO table_count FROM user_tables WHERE table_name='REMINDER_DELIVERY';
  IF table_count=0 THEN
    EXECUTE IMMEDIATE 'CREATE TABLE reminder_delivery (
      event_key VARCHAR2(120) PRIMARY KEY,
      issue_id NUMBER NOT NULL,
      channel VARCHAR2(10) NOT NULL,
      status VARCHAR2(12) DEFAULT ''PENDING'' NOT NULL,
      attempts NUMBER DEFAULT 0 NOT NULL,
      updated_at DATE DEFAULT SYSDATE NOT NULL,
      next_attempt DATE DEFAULT SYSDATE NOT NULL,
      provider_id VARCHAR2(100),
      CONSTRAINT reminder_channel_ck CHECK(channel IN (''SMS'',''EMAIL'')),
      CONSTRAINT reminder_status_ck CHECK(status IN (''PENDING'',''SENDING'',''ACCEPTED'',''FAILED'',''UNKNOWN'',''CANCELLED''))
    )';
  END IF;
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Delivery tracking only; existing loans, fines and member records are preserved.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 3 | <code>  table_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  SELECT COUNT(*) INTO table_count FROM user_tables WHERE table_name=&#x27;REMINDER_DELIVERY&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 6 | <code>  IF table_count=0 THEN</code> | PL/SQL condition/alternative branch। |
| 7 | <code>    EXECUTE IMMEDIATE &#x27;CREATE TABLE reminder_delivery (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 8 | <code>      event_key VARCHAR2(120) PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 9 | <code>      issue_id NUMBER NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>      channel VARCHAR2(10) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>      status VARCHAR2(12) DEFAULT &#x27;&#x27;PENDING&#x27;&#x27; NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 12 | <code>      attempts NUMBER DEFAULT 0 NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 13 | <code>      updated_at DATE DEFAULT SYSDATE NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 14 | <code>      next_attempt DATE DEFAULT SYSDATE NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 15 | <code>      provider_id VARCHAR2(100),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 16 | <code>      CONSTRAINT reminder_channel_ck CHECK(channel IN (&#x27;&#x27;SMS&#x27;&#x27;,&#x27;&#x27;EMAIL&#x27;&#x27;)),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 17 | <code>      CONSTRAINT reminder_status_ck CHECK(status IN (&#x27;&#x27;PENDING&#x27;&#x27;,&#x27;&#x27;SENDING&#x27;&#x27;,&#x27;&#x27;ACCEPTED&#x27;&#x27;,&#x27;&#x27;FAILED&#x27;&#x27;,&#x27;&#x27;UNKNOWN&#x27;&#x27;,&#x27;&#x27;CANCELLED&#x27;&#x27;))</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 18 | <code>    )&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 19 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 20 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
