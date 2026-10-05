# database/circulation_audit_upgrade.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/circulation_audit_upgrade.sql)। Snapshot 2026-10-04; 71 lines; SHA-256 `c60cfb881ce28ada2262c58fe38db8e185a96c76b8c45637a52242fa495a5525`।

## Function / object / element inventory

- **TRIGGER `audit_issue_book_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_fine_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।

## সম্পূর্ণ original source

```sql
CREATE OR REPLACE TRIGGER audit_issue_book_trigger
AFTER INSERT OR UPDATE OR DELETE ON issue_book
FOR EACH ROW
DECLARE
  change_action VARCHAR2(10);
  old_snapshot VARCHAR2(4000);
  new_snapshot VARCHAR2(4000);
BEGIN
  IF INSERTING THEN change_action := 'INSERT';
  ELSIF UPDATING THEN change_action := 'UPDATE';
  ELSE change_action := 'DELETE';
  END IF;
  IF UPDATING OR DELETING THEN
    old_snapshot := '{' || '"issue_id":' || audit_json_value(TO_CHAR(:OLD.issue_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"student_id":' || audit_json_value(TO_CHAR(:OLD.student_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"book_id":' || audit_json_value(TO_CHAR(:OLD.book_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"copy_id":' || audit_json_value(TO_CHAR(:OLD.copy_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"issue_date":' || audit_json_value(TO_CHAR(:OLD.issue_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"due_date":' || audit_json_value(TO_CHAR(:OLD.due_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"return_date":' || audit_json_value(TO_CHAR(:OLD.return_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"status":' || audit_json_value(:OLD.status) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"issue_id":' || audit_json_value(TO_CHAR(:NEW.issue_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"student_id":' || audit_json_value(TO_CHAR(:NEW.student_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"book_id":' || audit_json_value(TO_CHAR(:NEW.book_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"copy_id":' || audit_json_value(TO_CHAR(:NEW.copy_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"issue_date":' || audit_json_value(TO_CHAR(:NEW.issue_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"due_date":' || audit_json_value(TO_CHAR(:NEW.due_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"return_date":' || audit_json_value(TO_CHAR(:NEW.return_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"status":' || audit_json_value(:NEW.status) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'ISSUE_BOOK',
         NVL(:NEW.issue_id, :OLD.issue_id), old_snapshot, new_snapshot);
END;
/

CREATE OR REPLACE TRIGGER audit_fine_trigger
AFTER INSERT OR UPDATE OR DELETE ON fine
FOR EACH ROW
DECLARE
  change_action VARCHAR2(10);
  old_snapshot VARCHAR2(4000);
  new_snapshot VARCHAR2(4000);
BEGIN
  IF INSERTING THEN change_action := 'INSERT';
  ELSIF UPDATING THEN change_action := 'UPDATE';
  ELSE change_action := 'DELETE';
  END IF;
  IF UPDATING OR DELETING THEN
    old_snapshot := '{' || '"fine_id":' || audit_json_value(TO_CHAR(:OLD.fine_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"issue_id":' || audit_json_value(TO_CHAR(:OLD.issue_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"amount":' || audit_json_value(TO_CHAR(:OLD.amount, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"paid_amount":' || audit_json_value(TO_CHAR(:OLD.paid_amount, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"payment_status":' || audit_json_value(:OLD.payment_status) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"fine_id":' || audit_json_value(TO_CHAR(:NEW.fine_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"issue_id":' || audit_json_value(TO_CHAR(:NEW.issue_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"amount":' || audit_json_value(TO_CHAR(:NEW.amount, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"paid_amount":' || audit_json_value(TO_CHAR(:NEW.paid_amount, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"payment_status":' || audit_json_value(:NEW.payment_status) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'FINE',
         NVL(:NEW.fine_id, :OLD.fine_id), old_snapshot, new_snapshot);
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>CREATE OR REPLACE TRIGGER audit_issue_book_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 2 | <code>AFTER INSERT OR UPDATE OR DELETE ON issue_book</code> | নতুন business/audit/sample row insert করার statement। |
| 3 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 10 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 11 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 12 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 13 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 14 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 15 | <code>    &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.student_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 16 | <code>    &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.book_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 17 | <code>    &#x27;&quot;copy_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.copy_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 18 | <code>    &#x27;&quot;issue_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 19 | <code>    &#x27;&quot;due_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.due_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 20 | <code>    &#x27;&quot;return_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.return_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 21 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 22 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 23 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 24 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 25 | <code>    &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.student_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 26 | <code>    &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.book_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 27 | <code>    &#x27;&quot;copy_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.copy_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 28 | <code>    &#x27;&quot;issue_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 29 | <code>    &#x27;&quot;due_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.due_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 30 | <code>    &#x27;&quot;return_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.return_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 31 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 32 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 33 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 34 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 35 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;ISSUE_BOOK&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>         NVL(:NEW.issue_id, :OLD.issue_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 38 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 39 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 40 | <code>CREATE OR REPLACE TRIGGER audit_fine_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 41 | <code>AFTER INSERT OR UPDATE OR DELETE ON fine</code> | নতুন business/audit/sample row insert করার statement। |
| 42 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 43 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 44 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 45 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 46 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 47 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 48 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 49 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 50 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 51 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 52 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 53 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;fine_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.fine_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 54 | <code>    &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 55 | <code>    &#x27;&quot;amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 56 | <code>    &#x27;&quot;paid_amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.paid_amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 57 | <code>    &#x27;&quot;payment_status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.payment_status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 58 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 59 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 60 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;fine_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.fine_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 61 | <code>    &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 62 | <code>    &#x27;&quot;amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 63 | <code>    &#x27;&quot;paid_amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.paid_amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 64 | <code>    &#x27;&quot;payment_status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.payment_status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 65 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 66 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 67 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 68 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;FINE&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 69 | <code>         NVL(:NEW.fine_id, :OLD.fine_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 70 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 71 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
