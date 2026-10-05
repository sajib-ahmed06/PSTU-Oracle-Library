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
