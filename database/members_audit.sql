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

