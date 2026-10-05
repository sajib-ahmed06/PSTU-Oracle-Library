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
