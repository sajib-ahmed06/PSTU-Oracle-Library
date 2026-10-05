# database/members_audit.sql

Roll/registration fields ও uniqueness, student identity validation, transactional audit triggers এবং initial snapshots তৈরি করে।

Source: [মূল file](../../database/members_audit.sql)। Snapshot 2026-10-04; 325 lines; SHA-256 `54ab4e6b6d143229f7506d60e15e372de6d9d381414d46e85148f2236071c978`।

## Function / object / element inventory

- **TABLE `audit_log`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `audit_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **INDEX `ix_audit_entity`**: Database integrity/search performance enforce করে।
- **INDEX `ix_audit_time`**: Database integrity/search performance enforce করে।
- **FUNCTION `audit_json_value`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TRIGGER `audit_student_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_book_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_author_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_category_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_issue_book_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_return_book_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_fine_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_login_user_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।
- **TRIGGER `audit_admin_trigger`**: প্রতিটি insert/update/delete-এর before/after snapshot একই transaction-এ audit_log-এ লিখে।

## সম্পূর্ণ original source

```sql
-- Transactional change history for the fresh library schema.
CREATE TABLE audit_log (
  audit_id NUMBER PRIMARY KEY,
  occurred_at TIMESTAMP NOT NULL,
  actor VARCHAR2(100) NOT NULL,
  action VARCHAR2(10) NOT NULL CHECK (action IN ('INSERT','UPDATE','DELETE','SNAPSHOT')),
  entity VARCHAR2(30) NOT NULL,
  record_id NUMBER NOT NULL,
  before_data VARCHAR2(4000),
  after_data VARCHAR2(4000)
);
CREATE SEQUENCE audit_seq START WITH 1 INCREMENT BY 1;
CREATE INDEX ix_audit_entity ON audit_log(entity, record_id);
CREATE INDEX ix_audit_time ON audit_log(occurred_at);

CREATE OR REPLACE FUNCTION audit_json_value(p_value VARCHAR2) RETURN VARCHAR2 IS
  escaped VARCHAR2(4000);
BEGIN
  IF p_value IS NULL THEN RETURN 'null'; END IF;
  escaped := REPLACE(p_value, CHR(92), CHR(92) || CHR(92));
  escaped := REPLACE(escaped, CHR(34), CHR(92) || CHR(34));
  FOR character_code IN 0..31 LOOP
    escaped := REPLACE(escaped, CHR(character_code), CHR(92) || 'u00' || LPAD(TO_CHAR(character_code, 'FMXX'), 2, '0'));
  END LOOP;
  RETURN CHR(34) || escaped || CHR(34);
END;
/

CREATE OR REPLACE TRIGGER audit_student_trigger
AFTER INSERT OR UPDATE OR DELETE ON student
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
    old_snapshot := '{' || '"student_id":' || audit_json_value(TO_CHAR(:OLD.student_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"name":' || audit_json_value(:OLD.name) || ',' ||
    '"department":' || audit_json_value(:OLD.department) || ',' ||
    '"phone":' || audit_json_value(:OLD.phone) || ',' ||
    '"email":' || audit_json_value(:OLD.email) || ',' ||
    '"membership_status":' || audit_json_value(:OLD.membership_status) || ',' ||
    '"roll_no":' || audit_json_value(:OLD.roll_no) || ',' ||
    '"registration_no":' || audit_json_value(:OLD.registration_no) || ',' ||
    '"academic_session":' || audit_json_value(:OLD.academic_session) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"student_id":' || audit_json_value(TO_CHAR(:NEW.student_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"name":' || audit_json_value(:NEW.name) || ',' ||
    '"department":' || audit_json_value(:NEW.department) || ',' ||
    '"phone":' || audit_json_value(:NEW.phone) || ',' ||
    '"email":' || audit_json_value(:NEW.email) || ',' ||
    '"membership_status":' || audit_json_value(:NEW.membership_status) || ',' ||
    '"roll_no":' || audit_json_value(:NEW.roll_no) || ',' ||
    '"registration_no":' || audit_json_value(:NEW.registration_no) || ',' ||
    '"academic_session":' || audit_json_value(:NEW.academic_session) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'STUDENT',
         NVL(:NEW.student_id, :OLD.student_id), old_snapshot, new_snapshot);
END;
/

CREATE OR REPLACE TRIGGER audit_book_trigger
AFTER INSERT OR UPDATE OR DELETE ON book
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
    old_snapshot := '{' || '"book_id":' || audit_json_value(TO_CHAR(:OLD.book_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"title":' || audit_json_value(:OLD.title) || ',' ||
    '"author_id":' || audit_json_value(TO_CHAR(:OLD.author_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"category_id":' || audit_json_value(TO_CHAR(:OLD.category_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"publisher":' || audit_json_value(:OLD.publisher) || ',' ||
    '"quantity":' || audit_json_value(TO_CHAR(:OLD.quantity, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"available_quantity":' || audit_json_value(TO_CHAR(:OLD.available_quantity, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"book_id":' || audit_json_value(TO_CHAR(:NEW.book_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"title":' || audit_json_value(:NEW.title) || ',' ||
    '"author_id":' || audit_json_value(TO_CHAR(:NEW.author_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"category_id":' || audit_json_value(TO_CHAR(:NEW.category_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"publisher":' || audit_json_value(:NEW.publisher) || ',' ||
    '"quantity":' || audit_json_value(TO_CHAR(:NEW.quantity, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"available_quantity":' || audit_json_value(TO_CHAR(:NEW.available_quantity, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'BOOK',
         NVL(:NEW.book_id, :OLD.book_id), old_snapshot, new_snapshot);
END;
/

CREATE OR REPLACE TRIGGER audit_author_trigger
AFTER INSERT OR UPDATE OR DELETE ON author
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
    old_snapshot := '{' || '"author_id":' || audit_json_value(TO_CHAR(:OLD.author_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"author_name":' || audit_json_value(:OLD.author_name) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"author_id":' || audit_json_value(TO_CHAR(:NEW.author_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"author_name":' || audit_json_value(:NEW.author_name) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'AUTHOR',
         NVL(:NEW.author_id, :OLD.author_id), old_snapshot, new_snapshot);
END;
/

CREATE OR REPLACE TRIGGER audit_category_trigger
AFTER INSERT OR UPDATE OR DELETE ON category
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
    old_snapshot := '{' || '"category_id":' || audit_json_value(TO_CHAR(:OLD.category_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"category_name":' || audit_json_value(:OLD.category_name) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"category_id":' || audit_json_value(TO_CHAR(:NEW.category_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"category_name":' || audit_json_value(:NEW.category_name) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'CATEGORY',
         NVL(:NEW.category_id, :OLD.category_id), old_snapshot, new_snapshot);
END;
/

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

CREATE OR REPLACE TRIGGER audit_return_book_trigger
AFTER INSERT OR UPDATE OR DELETE ON return_book
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
    old_snapshot := '{' || '"return_id":' || audit_json_value(TO_CHAR(:OLD.return_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"issue_id":' || audit_json_value(TO_CHAR(:OLD.issue_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"return_date":' || audit_json_value(TO_CHAR(:OLD.return_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"fine_amount":' || audit_json_value(TO_CHAR(:OLD.fine_amount, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"status":' || audit_json_value(:OLD.status) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"return_id":' || audit_json_value(TO_CHAR(:NEW.return_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"issue_id":' || audit_json_value(TO_CHAR(:NEW.issue_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"return_date":' || audit_json_value(TO_CHAR(:NEW.return_date, 'YYYY-MM-DD HH24:MI:SS')) || ',' ||
    '"fine_amount":' || audit_json_value(TO_CHAR(:NEW.fine_amount, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"status":' || audit_json_value(:NEW.status) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'RETURN_BOOK',
         NVL(:NEW.return_id, :OLD.return_id), old_snapshot, new_snapshot);
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

CREATE OR REPLACE TRIGGER audit_login_user_trigger
AFTER INSERT OR UPDATE OR DELETE ON login_user
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
    old_snapshot := '{' || '"user_id":' || audit_json_value(TO_CHAR(:OLD.user_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"username":' || audit_json_value(:OLD.username) || ',' ||
    '"user_type":' || audit_json_value(:OLD.user_type) || ',' ||
    '"account_status":' || audit_json_value(:OLD.account_status) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"user_id":' || audit_json_value(TO_CHAR(:NEW.user_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"username":' || audit_json_value(:NEW.username) || ',' ||
    '"user_type":' || audit_json_value(:NEW.user_type) || ',' ||
    '"account_status":' || audit_json_value(:NEW.account_status) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'LOGIN_USER',
         NVL(:NEW.user_id, :OLD.user_id), old_snapshot, new_snapshot);
END;
/

CREATE OR REPLACE TRIGGER audit_admin_trigger
AFTER INSERT OR UPDATE OR DELETE ON admin
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
    old_snapshot := '{' || '"admin_id":' || audit_json_value(TO_CHAR(:OLD.admin_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"name":' || audit_json_value(:OLD.name) || ',' ||
    '"email":' || audit_json_value(:OLD.email) || '}';
  END IF;
  IF INSERTING OR UPDATING THEN
    new_snapshot := '{' || '"admin_id":' || audit_json_value(TO_CHAR(:NEW.admin_id, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''')) || ',' ||
    '"name":' || audit_json_value(:NEW.name) || ',' ||
    '"email":' || audit_json_value(:NEW.email) || '}';
  END IF;
  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)
  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),
         NVL(SYS_CONTEXT('USERENV', 'CLIENT_INFO'), USER), change_action, 'ADMIN',
         NVL(:NEW.admin_id, :OLD.admin_id), old_snapshot, new_snapshot);
END;
/
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Transactional change history for the fresh library schema.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>CREATE TABLE audit_log (</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 3 | <code>  audit_id NUMBER PRIMARY KEY,</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 4 | <code>  occurred_at TIMESTAMP NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>  actor VARCHAR2(100) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  action VARCHAR2(10) NOT NULL CHECK (action IN (&#x27;INSERT&#x27;,&#x27;UPDATE&#x27;,&#x27;DELETE&#x27;,&#x27;SNAPSHOT&#x27;)),</code> | Schema integrity rule: record identity, foreign key, domain বা uniqueness checks। |
| 7 | <code>  entity VARCHAR2(30) NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 8 | <code>  record_id NUMBER NOT NULL,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 9 | <code>  before_data VARCHAR2(4000),</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 10 | <code>  after_data VARCHAR2(4000)</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 11 | <code>);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 12 | <code>CREATE SEQUENCE audit_seq START WITH 1 INCREMENT BY 1;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 13 | <code>CREATE INDEX ix_audit_entity ON audit_log(entity, record_id);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 14 | <code>CREATE INDEX ix_audit_time ON audit_log(occurred_at);</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>CREATE OR REPLACE FUNCTION audit_json_value(p_value VARCHAR2) RETURN VARCHAR2 IS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 17 | <code>  escaped VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 18 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 19 | <code>  IF p_value IS NULL THEN RETURN &#x27;null&#x27;; END IF;</code> | PL/SQL condition/alternative branch। |
| 20 | <code>  escaped := REPLACE(p_value, CHR(92), CHR(92) &#124;&#124; CHR(92));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 21 | <code>  escaped := REPLACE(escaped, CHR(34), CHR(92) &#124;&#124; CHR(34));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>  FOR character_code IN 0..31 LOOP</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 23 | <code>    escaped := REPLACE(escaped, CHR(character_code), CHR(92) &#124;&#124; &#x27;u00&#x27; &#124;&#124; LPAD(TO_CHAR(character_code, &#x27;FMXX&#x27;), 2, &#x27;0&#x27;));</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 25 | <code>  RETURN CHR(34) &#124;&#124; escaped &#124;&#124; CHR(34);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 26 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>CREATE OR REPLACE TRIGGER audit_student_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 30 | <code>AFTER INSERT OR UPDATE OR DELETE ON student</code> | নতুন business/audit/sample row insert করার statement। |
| 31 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 32 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 33 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 34 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 35 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 38 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 39 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 40 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 41 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 42 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.student_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 43 | <code>    &#x27;&quot;name&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.name) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 44 | <code>    &#x27;&quot;department&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.department) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 45 | <code>    &#x27;&quot;phone&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.phone) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 46 | <code>    &#x27;&quot;email&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.email) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 47 | <code>    &#x27;&quot;membership_status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.membership_status) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 48 | <code>    &#x27;&quot;roll_no&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.roll_no) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 49 | <code>    &#x27;&quot;registration_no&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.registration_no) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 50 | <code>    &#x27;&quot;academic_session&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.academic_session) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 51 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 52 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 53 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.student_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 54 | <code>    &#x27;&quot;name&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.name) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 55 | <code>    &#x27;&quot;department&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.department) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 56 | <code>    &#x27;&quot;phone&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.phone) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 57 | <code>    &#x27;&quot;email&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.email) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 58 | <code>    &#x27;&quot;membership_status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.membership_status) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 59 | <code>    &#x27;&quot;roll_no&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.roll_no) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 60 | <code>    &#x27;&quot;registration_no&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.registration_no) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 61 | <code>    &#x27;&quot;academic_session&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.academic_session) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 62 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 63 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 64 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 65 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;STUDENT&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 66 | <code>         NVL(:NEW.student_id, :OLD.student_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 67 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 68 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 69 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 70 | <code>CREATE OR REPLACE TRIGGER audit_book_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 71 | <code>AFTER INSERT OR UPDATE OR DELETE ON book</code> | নতুন business/audit/sample row insert করার statement। |
| 72 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 73 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 74 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 75 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 76 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 77 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 78 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 79 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 80 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 81 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 82 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 83 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.book_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 84 | <code>    &#x27;&quot;title&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.title) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 85 | <code>    &#x27;&quot;author_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.author_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 86 | <code>    &#x27;&quot;category_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.category_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 87 | <code>    &#x27;&quot;publisher&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.publisher) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 88 | <code>    &#x27;&quot;quantity&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.quantity, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 89 | <code>    &#x27;&quot;available_quantity&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.available_quantity, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 90 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 91 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 92 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.book_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 93 | <code>    &#x27;&quot;title&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.title) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 94 | <code>    &#x27;&quot;author_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.author_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 95 | <code>    &#x27;&quot;category_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.category_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 96 | <code>    &#x27;&quot;publisher&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.publisher) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 97 | <code>    &#x27;&quot;quantity&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.quantity, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 98 | <code>    &#x27;&quot;available_quantity&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.available_quantity, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 99 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 100 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 101 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 102 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;BOOK&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 103 | <code>         NVL(:NEW.book_id, :OLD.book_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 104 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 105 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 106 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 107 | <code>CREATE OR REPLACE TRIGGER audit_author_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 108 | <code>AFTER INSERT OR UPDATE OR DELETE ON author</code> | নতুন business/audit/sample row insert করার statement। |
| 109 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 110 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 111 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 112 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 113 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 114 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 115 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 116 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 117 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 118 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 119 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 120 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;author_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.author_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 121 | <code>    &#x27;&quot;author_name&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.author_name) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 122 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 123 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 124 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;author_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.author_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 125 | <code>    &#x27;&quot;author_name&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.author_name) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 126 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 127 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 128 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 129 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;AUTHOR&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 130 | <code>         NVL(:NEW.author_id, :OLD.author_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 131 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 132 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 133 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 134 | <code>CREATE OR REPLACE TRIGGER audit_category_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 135 | <code>AFTER INSERT OR UPDATE OR DELETE ON category</code> | নতুন business/audit/sample row insert করার statement। |
| 136 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 137 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 138 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 139 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 140 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 141 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 142 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 143 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 144 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 145 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 146 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 147 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;category_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.category_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 148 | <code>    &#x27;&quot;category_name&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.category_name) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 149 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 150 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 151 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;category_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.category_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 152 | <code>    &#x27;&quot;category_name&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.category_name) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 153 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 154 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 155 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 156 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;CATEGORY&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 157 | <code>         NVL(:NEW.category_id, :OLD.category_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 158 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 159 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 160 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 161 | <code>CREATE OR REPLACE TRIGGER audit_issue_book_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 162 | <code>AFTER INSERT OR UPDATE OR DELETE ON issue_book</code> | নতুন business/audit/sample row insert করার statement। |
| 163 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 164 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 165 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 166 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 167 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 168 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 169 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 170 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 171 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 172 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 173 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 174 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 175 | <code>    &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.student_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 176 | <code>    &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.book_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 177 | <code>    &#x27;&quot;copy_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.copy_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 178 | <code>    &#x27;&quot;issue_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 179 | <code>    &#x27;&quot;due_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.due_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 180 | <code>    &#x27;&quot;return_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.return_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 181 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 182 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 183 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 184 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 185 | <code>    &#x27;&quot;student_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.student_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 186 | <code>    &#x27;&quot;book_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.book_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 187 | <code>    &#x27;&quot;copy_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.copy_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 188 | <code>    &#x27;&quot;issue_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 189 | <code>    &#x27;&quot;due_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.due_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 190 | <code>    &#x27;&quot;return_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.return_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 191 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 192 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 193 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 194 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 195 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;ISSUE_BOOK&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 196 | <code>         NVL(:NEW.issue_id, :OLD.issue_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 197 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 198 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 199 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 200 | <code>CREATE OR REPLACE TRIGGER audit_return_book_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 201 | <code>AFTER INSERT OR UPDATE OR DELETE ON return_book</code> | নতুন business/audit/sample row insert করার statement। |
| 202 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 203 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 204 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 205 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 206 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 207 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 208 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 209 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 210 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 211 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 212 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 213 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;return_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.return_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 214 | <code>    &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 215 | <code>    &#x27;&quot;return_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.return_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 216 | <code>    &#x27;&quot;fine_amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.fine_amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 217 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 218 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 219 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 220 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;return_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.return_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 221 | <code>    &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 222 | <code>    &#x27;&quot;return_date&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.return_date, &#x27;YYYY-MM-DD HH24:MI:SS&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 223 | <code>    &#x27;&quot;fine_amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.fine_amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 224 | <code>    &#x27;&quot;status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 225 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 226 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 227 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 228 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;RETURN_BOOK&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 229 | <code>         NVL(:NEW.return_id, :OLD.return_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 230 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 231 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 232 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 233 | <code>CREATE OR REPLACE TRIGGER audit_fine_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 234 | <code>AFTER INSERT OR UPDATE OR DELETE ON fine</code> | নতুন business/audit/sample row insert করার statement। |
| 235 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 236 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 237 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 238 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 239 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 240 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 241 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 242 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 243 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 244 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 245 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 246 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;fine_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.fine_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 247 | <code>    &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 248 | <code>    &#x27;&quot;amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 249 | <code>    &#x27;&quot;paid_amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.paid_amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 250 | <code>    &#x27;&quot;payment_status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.payment_status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 251 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 252 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 253 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;fine_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.fine_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 254 | <code>    &#x27;&quot;issue_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.issue_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 255 | <code>    &#x27;&quot;amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 256 | <code>    &#x27;&quot;paid_amount&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.paid_amount, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 257 | <code>    &#x27;&quot;payment_status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.payment_status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 258 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 259 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 260 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 261 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;FINE&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 262 | <code>         NVL(:NEW.fine_id, :OLD.fine_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 263 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 264 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 265 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 266 | <code>CREATE OR REPLACE TRIGGER audit_login_user_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 267 | <code>AFTER INSERT OR UPDATE OR DELETE ON login_user</code> | নতুন business/audit/sample row insert করার statement। |
| 268 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 269 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 270 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 271 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 272 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 273 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 274 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 275 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 276 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 277 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 278 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 279 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;user_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.user_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 280 | <code>    &#x27;&quot;username&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.username) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 281 | <code>    &#x27;&quot;user_type&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.user_type) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 282 | <code>    &#x27;&quot;account_status&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.account_status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 283 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 284 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 285 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;user_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.user_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 286 | <code>    &#x27;&quot;username&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.username) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 287 | <code>    &#x27;&quot;user_type&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.user_type) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 288 | <code>    &#x27;&quot;account_status&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.account_status) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 289 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 290 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 291 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 292 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;LOGIN_USER&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 293 | <code>         NVL(:NEW.user_id, :OLD.user_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 294 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 295 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 296 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 297 | <code>CREATE OR REPLACE TRIGGER audit_admin_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 298 | <code>AFTER INSERT OR UPDATE OR DELETE ON admin</code> | নতুন business/audit/sample row insert করার statement। |
| 299 | <code>FOR EACH ROW</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 300 | <code>DECLARE</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 301 | <code>  change_action VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 302 | <code>  old_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 303 | <code>  new_snapshot VARCHAR2(4000);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 304 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 305 | <code>  IF INSERTING THEN change_action := &#x27;INSERT&#x27;;</code> | PL/SQL condition/alternative branch। |
| 306 | <code>  ELSIF UPDATING THEN change_action := &#x27;UPDATE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 307 | <code>  ELSE change_action := &#x27;DELETE&#x27;;</code> | PL/SQL condition/alternative branch। |
| 308 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 309 | <code>  IF UPDATING OR DELETING THEN</code> | PL/SQL condition/alternative branch। |
| 310 | <code>    old_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;admin_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:OLD.admin_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 311 | <code>    &#x27;&quot;name&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.name) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 312 | <code>    &#x27;&quot;email&quot;:&#x27; &#124;&#124; audit_json_value(:OLD.email) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 313 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 314 | <code>  IF INSERTING OR UPDATING THEN</code> | PL/SQL condition/alternative branch। |
| 315 | <code>    new_snapshot := &#x27;{&#x27; &#124;&#124; &#x27;&quot;admin_id&quot;:&#x27; &#124;&#124; audit_json_value(TO_CHAR(:NEW.admin_id, &#x27;TM9&#x27;, &#x27;NLS_NUMERIC_CHARACTERS=&#x27;&#x27;.,&#x27;&#x27;&#x27;)) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 316 | <code>    &#x27;&quot;name&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.name) &#124;&#124; &#x27;,&#x27; &#124;&#124;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 317 | <code>    &#x27;&quot;email&quot;:&#x27; &#124;&#124; audit_json_value(:NEW.email) &#124;&#124; &#x27;}&#x27;;</code> | Field value JSON-safe representation-এ নিয়ে before/after snapshot গঠন করে। |
| 318 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 319 | <code>  INSERT INTO audit_log(audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data)</code> | নতুন business/audit/sample row insert করার statement। |
| 320 | <code>  VALUES(audit_seq.NEXTVAL, SYS_EXTRACT_UTC(SYSTIMESTAMP),</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 321 | <code>         NVL(SYS_CONTEXT(&#x27;USERENV&#x27;, &#x27;CLIENT_INFO&#x27;), USER), change_action, &#x27;ADMIN&#x27;,</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 322 | <code>         NVL(:NEW.admin_id, :OLD.admin_id), old_snapshot, new_snapshot);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 323 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 324 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 325 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
