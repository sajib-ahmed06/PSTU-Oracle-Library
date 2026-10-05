# database/reservations_audit_upgrade.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/reservations_audit_upgrade.sql)। Snapshot 2026-10-04; 48 lines; SHA-256 `90574fa34217c0e33f04a323dba60a523b7a9a0147eda3b397113f930fe0aab8`।

## Function / object / element inventory

- **TRIGGER `audit_reservation_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।

## সম্পূর্ণ original source

```sql
CREATE OR REPLACE TRIGGER audit_reservation_trigger
AFTER INSERT OR UPDATE OR DELETE ON book_reservation FOR EACH ROW
DECLARE
  change_action VARCHAR2(10);
  old_snapshot VARCHAR2(4000);
  new_snapshot VARCHAR2(4000);
BEGIN
  IF INSERTING THEN
    change_action:='INSERT';
  ELSIF UPDATING THEN
    change_action:='UPDATE';
  ELSE
    change_action:='DELETE';
  END IF;

  IF UPDATING OR DELETING THEN
    old_snapshot := '{' || '"reservation_id":' || audit_json_value(TO_CHAR(:OLD.reservation_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"student_id":' || audit_json_value(TO_CHAR(:OLD.student_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"book_id":' || audit_json_value(TO_CHAR(:OLD.book_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"copy_id":' || audit_json_value(TO_CHAR(:OLD.copy_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"status":' || audit_json_value(:OLD.status) || ',' ||
    '"reserved_at":' || audit_json_value(TO_CHAR(:OLD.reserved_at,'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"expires_at":' || audit_json_value(TO_CHAR(:OLD.expires_at,'YYYY-MM-DD HH24:MI:SS')) || '}';
  END IF;

  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"reservation_id":' || audit_json_value(TO_CHAR(:NEW.reservation_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"student_id":' || audit_json_value(TO_CHAR(:NEW.student_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"book_id":' || audit_json_value(TO_CHAR(:NEW.book_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"copy_id":' || audit_json_value(TO_CHAR(:NEW.copy_id,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"status":' || audit_json_value(:NEW.status) || ',' ||
    '"reserved_at":' || audit_json_value(TO_CHAR(:NEW.reserved_at,'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"expires_at":' || audit_json_value(TO_CHAR(:NEW.expires_at,'YYYY-MM-DD HH24:MI:SS')) || '}';
  END IF;

  INSERT INTO audit_log(audit_id,occurred_at,actor,action,entity,record_id,before_data,after_data)
  VALUES(
    audit_seq.NEXTVAL,
    SYS_EXTRACT_UTC(SYSTIMESTAMP),
    NVL(SYS_CONTEXT('USERENV','CLIENT_INFO'),USER),
    change_action,
    'BOOK_RESERVATION',
    NVL(:NEW.reservation_id,:OLD.reservation_id),
    old_snapshot,
    new_snapshot
  );
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>CREATE OR REPLACE TRIGGER audit_reservation_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 2 | <code>AFTER INSERT OR UPDATE OR DELETE ON book_reservation FOR EACH ROW</code> | নতুন business/audit/sample row insert করার statement। |
| 3 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 4 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 7 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>  IF INSERTING THEN</code> | PL/SQL condition/alternative branch। |
| 9 | <code>    change_action:=&#x27;INSERT&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>  ELSIF UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 11 | <code>    change_action:=&#x27;UPDATE&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 12 | <code>  ELSE</code> | PL/SQL condition/alternative branch। |
| 13 | <code>    change_action:=&#x27;DELETE&#x27;;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 14 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 17 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;reservation_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.reservation_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 18 | <code>    &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.student_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 19 | <code>    &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.book_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 20 | <code>    &#x27;&quot;copy_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.copy_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 21 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.status) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 22 | <code>    &#x27;&quot;reserved_at&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.reserved_at,&#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 23 | <code>    &#x27;&quot;expires_at&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.expires_at,&#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 24 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 25 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 26 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 27 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;reservation_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.reservation_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 28 | <code>    &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.student_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 29 | <code>    &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.book_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 30 | <code>    &#x27;&quot;copy_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.copy_id,&#x27;TM9&#x27;,&#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 31 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.status) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 32 | <code>    &#x27;&quot;reserved_at&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.reserved_at,&#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 33 | <code>    &#x27;&quot;expires_at&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.expires_at,&#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 34 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 35 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 36 | <code>  INSERT INTO audit_log(audit_id,occurred_at,actor,action,entity,record_id,before_data,after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 37 | <code>  VALUES(</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 38 | <code>    audit_seq.NEXTVAL,</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 39 | <code>    SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 40 | <code>    NVL(SYS_CONTEXT(&#x27;USERENV&#x27;,&#x27;CLIENT_INFO&#x27;),USER),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 41 | <code>    change_action,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 42 | <code>    &#x27;BOOK_RESERVATION&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 43 | <code>    NVL(:NEW.reservation_id,:OLD.reservation_id),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 44 | <code>    old_snapshot,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 45 | <code>    new_snapshot</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 46 | <code>  );</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 47 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 48 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
