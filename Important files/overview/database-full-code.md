# Complete fresh database SQL

bootstrap creates the Oracle account. setup is the ordered entry point for schema modules, feature upgrades, audit objects and sample records. Schema modules are not standalone upgrades. Use Setup-Database.bat only when you intend to reset the data; use backend.upgrade_circulation for an existing installation.

## database/bootstrap.sql

Source: [মূল ফাইল](../../database/bootstrap.sql)

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

## database/circulation_audit_upgrade.sql

Source: [মূল ফাইল](../../database/circulation_audit_upgrade.sql)

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

## database/circulation_upgrade.sql

Source: [মূল ফাইল](../../database/circulation_upgrade.sql)

```sql
-- Non-destructive, rerunnable upgrade. Run as CONFIGURED_SCHEMA while the app is stopped.
SET DEFINE OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
DECLARE n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM user_tables WHERE table_name='BOOK_COPY';
  IF n=0 THEN
    EXECUTE IMMEDIATE 'CREATE TABLE book_copy (copy_id NUMBER PRIMARY KEY, book_id NUMBER NOT NULL REFERENCES book(book_id), copy_no NUMBER NOT NULL, status VARCHAR2(10) DEFAULT ''AVAILABLE'' NOT NULL CHECK(status IN (''AVAILABLE'',''ISSUED'',''RETIRED'')), UNIQUE(book_id,copy_no), UNIQUE(book_id,copy_id))';
    EXECUTE IMMEDIATE 'CREATE SEQUENCE copy_seq';
  END IF;
  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name='ISSUE_BOOK' AND column_name='COPY_ID';
  IF n=0 THEN
    EXECUTE IMMEDIATE 'ALTER TABLE issue_book ADD (copy_id NUMBER)';
    EXECUTE IMMEDIATE 'ALTER TABLE issue_book ADD CONSTRAINT issue_copy_fk FOREIGN KEY(book_id,copy_id) REFERENCES book_copy(book_id,copy_id)';
    EXECUTE IMMEDIATE 'CREATE UNIQUE INDEX uq_active_copy ON issue_book(CASE WHEN status=''ISSUED'' THEN copy_id END)';
  END IF;
  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name='FINE' AND column_name='PAID_AMOUNT';
  IF n=0 THEN
    EXECUTE IMMEDIATE 'ALTER TABLE fine ADD (paid_amount NUMBER(12,2) DEFAULT 0 NOT NULL)';
    EXECUTE IMMEDIATE 'UPDATE fine SET paid_amount=amount WHERE payment_status=''PAID''';
    EXECUTE IMMEDIATE 'ALTER TABLE fine ADD CONSTRAINT fine_paid_ck CHECK(paid_amount>=0 AND paid_amount<=amount)';
  END IF;
  SELECT COUNT(*) INTO n FROM user_tables WHERE table_name='FINE_PAYMENT';
  IF n=0 THEN
    EXECUTE IMMEDIATE 'CREATE TABLE fine_payment (payment_id NUMBER PRIMARY KEY, fine_id NUMBER NOT NULL REFERENCES fine(fine_id), amount NUMBER(12,2) NOT NULL CHECK(amount>0), paid_at DATE DEFAULT SYSDATE NOT NULL, actor VARCHAR2(100) NOT NULL, note VARCHAR2(300))';
    EXECUTE IMMEDIATE 'CREATE SEQUENCE payment_seq';
  END IF;
END;
/
-- Assign numbers to existing stock. Historical returned loans have no known copy.
DECLARE v_copy NUMBER; v_count NUMBER; v_max NUMBER;
BEGIN
  FOR b IN (SELECT book_id,quantity FROM book ORDER BY book_id FOR UPDATE) LOOP
    SELECT COUNT(*),NVL(MAX(copy_no),0) INTO v_count,v_max FROM book_copy WHERE book_id=b.book_id AND status<>'RETIRED';
    IF v_count < b.quantity THEN
      FOR j IN 1..(b.quantity-v_count) LOOP
        INSERT INTO book_copy(copy_id,book_id,copy_no) VALUES(copy_seq.NEXTVAL,b.book_id,v_max+j);
      END LOOP;
    END IF;
    FOR i IN (SELECT issue_id FROM issue_book WHERE book_id=b.book_id AND status='ISSUED' AND copy_id IS NULL ORDER BY issue_id) LOOP
      SELECT MIN(copy_id) INTO v_copy FROM book_copy WHERE book_id=b.book_id AND status='AVAILABLE';
      IF v_copy IS NULL THEN RAISE_APPLICATION_ERROR(-20009,'Existing loans exceed stock'); END IF;
      UPDATE book_copy SET status='ISSUED' WHERE copy_id=v_copy;
      UPDATE issue_book SET copy_id=v_copy WHERE issue_id=i.issue_id;
    END LOOP;
  END LOOP;
  COMMIT;
END;
/
CREATE OR REPLACE TRIGGER book_copy_stock_trigger
AFTER INSERT OR UPDATE OF quantity ON book FOR EACH ROW
DECLARE v_max NUMBER; v_delta NUMBER; v_count NUMBER;
BEGIN
  v_delta := :NEW.quantity - NVL(:OLD.quantity,0);
  IF v_delta>0 THEN
    SELECT NVL(MAX(copy_no),0) INTO v_max FROM book_copy WHERE book_id=:NEW.book_id;
    FOR j IN 1..v_delta LOOP
      INSERT INTO book_copy(copy_id,book_id,copy_no) VALUES(copy_seq.NEXTVAL,:NEW.book_id,v_max+j);
    END LOOP;
  ELSIF v_delta<0 THEN
    SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=:NEW.book_id AND status='AVAILABLE';
    IF v_count < -v_delta THEN RAISE_APPLICATION_ERROR(-20008,'Only available copies can be removed'); END IF;
    UPDATE book_copy SET status='RETIRED' WHERE copy_id IN
      (SELECT copy_id FROM (SELECT copy_id FROM book_copy WHERE book_id=:NEW.book_id AND status='AVAILABLE' ORDER BY copy_no DESC) WHERE ROWNUM<=-v_delta);
  END IF;
END;
/
CREATE OR REPLACE TRIGGER issue_quantity_trigger
BEFORE INSERT ON issue_book FOR EACH ROW
DECLARE v_available NUMBER; v_status VARCHAR2(10);
BEGIN
  SELECT available_quantity INTO v_available FROM book WHERE book_id=:NEW.book_id FOR UPDATE;
  IF v_available<=0 THEN RAISE_APPLICATION_ERROR(-20001,'Book is not available'); END IF;
  IF :NEW.copy_id IS NULL THEN
    SELECT MIN(copy_id) INTO :NEW.copy_id FROM book_copy WHERE book_id=:NEW.book_id AND status='AVAILABLE';
  END IF;
  SELECT status INTO v_status FROM book_copy WHERE copy_id=:NEW.copy_id AND book_id=:NEW.book_id FOR UPDATE;
  IF v_status<>'AVAILABLE' THEN RAISE_APPLICATION_ERROR(-20010,'This copy is not available'); END IF;
  UPDATE book_copy SET status='ISSUED' WHERE copy_id=:NEW.copy_id;
  UPDATE book SET available_quantity=available_quantity-1 WHERE book_id=:NEW.book_id;
  IF :NEW.issue_date IS NULL THEN :NEW.issue_date:=SYSDATE; END IF;
  IF :NEW.due_date IS NULL THEN :NEW.due_date:=:NEW.issue_date+15; END IF;
END;
/
CREATE OR REPLACE PROCEDURE issue_book_proc(p_student_id NUMBER,p_book_id NUMBER,p_copy_id NUMBER DEFAULT NULL) AS
  v_membership VARCHAR2(20); v_count NUMBER;
BEGIN
  SELECT membership_status INTO v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;
  IF v_membership<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=p_student_id AND status='ISSUED';
  IF v_count>=3 THEN RAISE_APPLICATION_ERROR(-20006,'A member may borrow at most 3 copies at a time'); END IF;
  SELECT COUNT(*) INTO v_count FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id WHERE i.student_id=p_student_id AND f.amount>f.paid_amount;
  IF v_count>0 THEN RAISE_APPLICATION_ERROR(-20007,'Pay all outstanding fines before issuing another book'); END IF;
  INSERT INTO issue_book(student_id,book_id,copy_id,issue_date,due_date,status)
  VALUES(p_student_id,p_book_id,p_copy_id,SYSDATE,SYSDATE+15,'ISSUED');
END;
/
CREATE OR REPLACE PROCEDURE return_book_proc(p_issue_id NUMBER) AS
  v_book NUMBER; v_copy NUMBER; v_status VARCHAR2(20); v_due DATE; v_fine NUMBER;
BEGIN
  SELECT book_id,copy_id,status,due_date INTO v_book,v_copy,v_status,v_due FROM issue_book WHERE issue_id=p_issue_id FOR UPDATE;
  IF v_status='RETURNED' THEN RAISE_APPLICATION_ERROR(-20002,'Book is already returned'); END IF;
  v_fine:=GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(v_due,SYSDATE)),0)*10;
  INSERT INTO return_book(issue_id,return_date,fine_amount,status) VALUES(p_issue_id,SYSDATE,v_fine,'RETURNED');
  UPDATE issue_book SET status='RETURNED',return_date=SYSDATE WHERE issue_id=p_issue_id;
  UPDATE book SET available_quantity=available_quantity+1 WHERE book_id=v_book;
  UPDATE book_copy SET status='AVAILABLE' WHERE copy_id=v_copy;
  IF v_fine>0 THEN INSERT INTO fine(issue_id,amount,payment_status) VALUES(p_issue_id,v_fine,'UNPAID'); END IF;
END;
/
CREATE OR REPLACE PROCEDURE pay_fine_proc(p_fine_id NUMBER,p_amount NUMBER DEFAULT NULL,p_note VARCHAR2 DEFAULT NULL) AS
  v_amount NUMBER; v_paid NUMBER; v_balance NUMBER;
BEGIN
  SELECT amount,paid_amount INTO v_amount,v_paid FROM fine WHERE fine_id=p_fine_id FOR UPDATE;
  v_balance := v_amount-v_paid;
  IF v_balance<=0 THEN RAISE_APPLICATION_ERROR(-20011,'This fine is already paid'); END IF;
  IF p_amount IS NOT NULL AND p_amount<>v_balance THEN
    RAISE_APPLICATION_ERROR(-20012,'The full outstanding fine must be paid');
  END IF;
  INSERT INTO fine_payment(payment_id,fine_id,amount,actor,note)
  VALUES(payment_seq.NEXTVAL,p_fine_id,v_balance,NVL(SYS_CONTEXT('USERENV','CLIENT_INFO'),USER),p_note);
  UPDATE fine SET paid_amount=v_amount,payment_status='PAID' WHERE fine_id=p_fine_id;
END;
/
COMMIT;
```

## database/members_audit.sql

Source: [মূল ফাইল](../../database/members_audit.sql)

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

## database/reminders_upgrade.sql

Source: [মূল ফাইল](../../database/reminders_upgrade.sql)

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

## database/reservations_audit_upgrade.sql

Source: [মূল ফাইল](../../database/reservations_audit_upgrade.sql)

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

## database/reservations_upgrade.sql

Source: [মূল ফাইল](../../database/reservations_upgrade.sql)

```sql
-- Data-preserving student access and three-day physical-copy reservations.
SET DEFINE OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
DECLARE n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name='LOGIN_USER' AND column_name='STUDENT_ID';
  IF n=0 THEN
    EXECUTE IMMEDIATE 'ALTER TABLE login_user ADD (student_id NUMBER REFERENCES student(student_id) UNIQUE)';
    EXECUTE IMMEDIATE 'ALTER TABLE login_user ADD CONSTRAINT login_student_role_ck CHECK(student_id IS NULL OR user_type=''STUDENT'')';
  END IF;
  SELECT COUNT(*) INTO n FROM user_tables WHERE table_name='BOOK_RESERVATION';
  IF n=0 THEN
    EXECUTE IMMEDIATE 'CREATE TABLE book_reservation (reservation_id NUMBER PRIMARY KEY, student_id NUMBER NOT NULL REFERENCES student(student_id), book_id NUMBER NOT NULL, copy_id NUMBER NOT NULL, reserved_at DATE DEFAULT SYSDATE NOT NULL, expires_at DATE DEFAULT SYSDATE+3 NOT NULL, status VARCHAR2(12) DEFAULT ''ACTIVE'' NOT NULL CHECK(status IN (''ACTIVE'',''EXPIRED'',''CANCELLED'',''COLLECTED'')), CONSTRAINT reservation_copy_fk FOREIGN KEY(book_id,copy_id) REFERENCES book_copy(book_id,copy_id))';
    EXECUTE IMMEDIATE 'CREATE SEQUENCE reservation_seq';
    EXECUTE IMMEDIATE 'CREATE UNIQUE INDEX uq_reserved_copy ON book_reservation(CASE WHEN status=''ACTIVE'' THEN copy_id END)';
    EXECUTE IMMEDIATE 'CREATE INDEX ix_reservation_member ON book_reservation(student_id,status,expires_at)';
  END IF;
END;
/
CREATE OR REPLACE PROCEDURE expire_reservations_proc AS
BEGIN
  UPDATE book_reservation SET status='EXPIRED' WHERE status='ACTIVE' AND expires_at<=SYSDATE;
END;
/
CREATE OR REPLACE PROCEDURE reserve_book_proc(p_student_id NUMBER,p_book_id NUMBER) AS
  v_status VARCHAR2(20); v_count NUMBER; v_copy NUMBER; v_book NUMBER;
BEGIN
  SELECT membership_status INTO v_status FROM student WHERE student_id=p_student_id FOR UPDATE;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  SELECT book_id INTO v_book FROM book WHERE book_id=p_book_id FOR UPDATE;
  expire_reservations_proc;
  SELECT COUNT(*) INTO v_count FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id WHERE i.student_id=p_student_id AND f.amount>f.paid_amount;
  IF v_count>0 THEN RAISE_APPLICATION_ERROR(-20007,'Pay all outstanding fines before reserving a book'); END IF;
  SELECT (SELECT COUNT(*) FROM issue_book WHERE student_id=p_student_id AND status='ISSUED')+
         (SELECT COUNT(*) FROM book_reservation WHERE student_id=p_student_id AND status='ACTIVE' AND expires_at>SYSDATE)
  INTO v_count FROM dual;
  IF v_count>=3 THEN RAISE_APPLICATION_ERROR(-20006,'A member may have at most 3 loans and reservations together'); END IF;
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE student_id=p_student_id AND book_id=p_book_id AND status='ACTIVE';
  IF v_count>0 THEN RAISE_APPLICATION_ERROR(-20030,'You already reserved this title'); END IF;
  SELECT MIN(c.copy_id) INTO v_copy FROM book_copy c WHERE c.book_id=p_book_id AND c.status='AVAILABLE'
    AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status='ACTIVE' AND r.expires_at>SYSDATE);
  IF v_copy IS NULL THEN RAISE_APPLICATION_ERROR(-20001,'No available copy to reserve'); END IF;
  INSERT INTO book_reservation(reservation_id,student_id,book_id,copy_id) VALUES(reservation_seq.NEXTVAL,p_student_id,p_book_id,v_copy);
END;
/
CREATE OR REPLACE TRIGGER issue_quantity_trigger
BEFORE INSERT ON issue_book FOR EACH ROW
DECLARE v_available NUMBER; v_status VARCHAR2(10); v_owner NUMBER;
BEGIN
  SELECT available_quantity INTO v_available FROM book WHERE book_id=:NEW.book_id FOR UPDATE;
  IF v_available<=0 THEN RAISE_APPLICATION_ERROR(-20001,'Book is not available'); END IF;
  IF :NEW.copy_id IS NULL THEN
    SELECT MIN(c.copy_id) INTO :NEW.copy_id FROM book_copy c WHERE c.book_id=:NEW.book_id AND c.status='AVAILABLE'
      AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status='ACTIVE' AND r.expires_at>SYSDATE);
  END IF;
  IF :NEW.copy_id IS NULL THEN RAISE_APPLICATION_ERROR(-20001,'All available copies are reserved'); END IF;
  SELECT status INTO v_status FROM book_copy WHERE copy_id=:NEW.copy_id AND book_id=:NEW.book_id FOR UPDATE;
  IF v_status<>'AVAILABLE' THEN RAISE_APPLICATION_ERROR(-20010,'This copy is not available'); END IF;
  SELECT MAX(student_id) INTO v_owner FROM book_reservation WHERE copy_id=:NEW.copy_id AND status='ACTIVE' AND expires_at>SYSDATE;
  IF v_owner IS NOT NULL AND v_owner<>:NEW.student_id THEN RAISE_APPLICATION_ERROR(-20031,'This copy is reserved for another member'); END IF;
  UPDATE book_reservation SET status='COLLECTED' WHERE copy_id=:NEW.copy_id AND student_id=:NEW.student_id AND status='ACTIVE' AND expires_at>SYSDATE;
  UPDATE book_copy SET status='ISSUED' WHERE copy_id=:NEW.copy_id;
  UPDATE book SET available_quantity=available_quantity-1 WHERE book_id=:NEW.book_id;
  IF :NEW.issue_date IS NULL THEN :NEW.issue_date:=SYSDATE; END IF;
  IF :NEW.due_date IS NULL THEN :NEW.due_date:=:NEW.issue_date+15; END IF;
END;
/
CREATE OR REPLACE PROCEDURE issue_book_proc(p_student_id NUMBER,p_book_id NUMBER,p_copy_id NUMBER DEFAULT NULL) AS
  v_membership VARCHAR2(20); v_count NUMBER; v_copy NUMBER:=p_copy_id;
BEGIN
  SELECT membership_status INTO v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;
  IF v_membership<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  IF v_copy IS NULL THEN
    SELECT MIN(copy_id) INTO v_copy FROM book_reservation WHERE student_id=p_student_id AND book_id=p_book_id AND status='ACTIVE' AND expires_at>SYSDATE;
  END IF;
  SELECT (SELECT COUNT(*) FROM issue_book WHERE student_id=p_student_id AND status='ISSUED')+
    (SELECT COUNT(*) FROM book_reservation WHERE student_id=p_student_id AND status='ACTIVE' AND expires_at>SYSDATE AND (v_copy IS NULL OR copy_id<>v_copy))
  INTO v_count FROM dual;
  IF v_count>=3 THEN RAISE_APPLICATION_ERROR(-20006,'A member may have at most 3 loans and reservations together'); END IF;
  SELECT COUNT(*) INTO v_count FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id WHERE i.student_id=p_student_id AND f.amount>f.paid_amount;
  IF v_count>0 THEN RAISE_APPLICATION_ERROR(-20007,'Pay all outstanding fines before issuing another book'); END IF;
  INSERT INTO issue_book(student_id,book_id,copy_id,issue_date,due_date,status) VALUES(p_student_id,p_book_id,v_copy,SYSDATE,SYSDATE+15,'ISSUED');
END;
/
CREATE OR REPLACE TRIGGER book_copy_stock_trigger
AFTER INSERT OR UPDATE OF quantity ON book FOR EACH ROW
DECLARE v_max NUMBER; v_delta NUMBER; v_count NUMBER;
BEGIN
  v_delta:=:NEW.quantity-NVL(:OLD.quantity,0);
  IF v_delta>0 THEN
    SELECT NVL(MAX(copy_no),0) INTO v_max FROM book_copy WHERE book_id=:NEW.book_id;
    FOR j IN 1..v_delta LOOP INSERT INTO book_copy(copy_id,book_id,copy_no) VALUES(copy_seq.NEXTVAL,:NEW.book_id,v_max+j); END LOOP;
  ELSIF v_delta<0 THEN
    SELECT COUNT(*) INTO v_count FROM book_copy c WHERE c.book_id=:NEW.book_id AND c.status='AVAILABLE'
      AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status='ACTIVE' AND r.expires_at>SYSDATE);
    IF v_count < -v_delta THEN RAISE_APPLICATION_ERROR(-20008,'Only unreserved available copies can be removed'); END IF;
    UPDATE book_copy SET status='RETIRED' WHERE copy_id IN
      (SELECT copy_id FROM (SELECT c.copy_id FROM book_copy c WHERE c.book_id=:NEW.book_id AND c.status='AVAILABLE'
        AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status='ACTIVE' AND r.expires_at>SYSDATE)
        ORDER BY c.copy_no DESC) WHERE ROWNUM<=-v_delta);
  END IF;
END;
/
-- Oracle performs expiry even while the web server is stopped. Reads and issue
-- guards also treat the exact three-day deadline as expired between job runs.
DECLARE n NUMBER; v_job NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM user_jobs WHERE what='expire_reservations_proc;';
  IF n=0 THEN DBMS_JOB.SUBMIT(v_job,'expire_reservations_proc;',SYSDATE,'SYSDATE+1/1440'); END IF;
  COMMIT;
END;
/
```

## database/schema/accounts.sql

Source: [মূল ফাইল](../../database/schema/accounts.sql)

```sql
-- Application accounts
CREATE TABLE login_user (
  user_id NUMBER PRIMARY KEY,
  username VARCHAR2(100) NOT NULL UNIQUE,
  password VARCHAR2(100) NOT NULL,
  user_type VARCHAR2(20) NOT NULL,
  account_status VARCHAR2(10) DEFAULT 'ACTIVE' NOT NULL,
  CONSTRAINT login_user_type_ck CHECK (user_type IN ('ADMIN','LIBRARIAN','STUDENT')),
  CONSTRAINT login_user_status_ck CHECK (account_status IN ('ACTIVE','DISABLED'))
);
CREATE UNIQUE INDEX uq_login_username ON login_user(LOWER(TRIM(username)));
CREATE INDEX ix_issue_student_status ON issue_book(student_id, status);
CREATE INDEX ix_issue_book ON issue_book(book_id);
CREATE INDEX ix_book_author ON book(author_id);
CREATE INDEX ix_book_category ON book(category_id);

CREATE SEQUENCE login_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER login_trigger BEFORE INSERT ON login_user FOR EACH ROW
BEGIN
  IF :NEW.user_id IS NULL THEN
    SELECT login_seq.NEXTVAL INTO :NEW.user_id FROM dual;
  END IF;
END;
/
```

## database/schema/catalogue.sql

Source: [মূল ফাইল](../../database/schema/catalogue.sql)

```sql
-- Book catalogue
CREATE TABLE author (author_id NUMBER PRIMARY KEY, author_name VARCHAR2(100) NOT NULL UNIQUE);
CREATE SEQUENCE author_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER author_trigger BEFORE INSERT ON author FOR EACH ROW
BEGIN
  IF :NEW.author_id IS NULL THEN
    SELECT author_seq.NEXTVAL INTO :NEW.author_id FROM dual;
  END IF;
END;
/

CREATE UNIQUE INDEX uq_author_name ON author(LOWER(TRIM(author_name)));

CREATE TABLE category (category_id NUMBER PRIMARY KEY, category_name VARCHAR2(100) NOT NULL UNIQUE);
CREATE SEQUENCE category_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER category_trigger BEFORE INSERT ON category FOR EACH ROW
BEGIN
  IF :NEW.category_id IS NULL THEN
    SELECT category_seq.NEXTVAL INTO :NEW.category_id FROM dual;
  END IF;
END;
/

CREATE UNIQUE INDEX uq_category_name ON category(LOWER(TRIM(category_name)));
CREATE UNIQUE INDEX uq_student_roll ON student(UPPER(TRIM(roll_no)));
CREATE UNIQUE INDEX uq_student_registration ON student(UPPER(TRIM(registration_no)));
CREATE UNIQUE INDEX uq_student_email ON student(LOWER(TRIM(email)));

CREATE TABLE book (
  book_id NUMBER PRIMARY KEY,
  title VARCHAR2(200) NOT NULL,
  author_id NUMBER NOT NULL REFERENCES author(author_id),
  category_id NUMBER NOT NULL REFERENCES category(category_id),
  publisher VARCHAR2(100),
  quantity NUMBER DEFAULT 0 NOT NULL CHECK (quantity >= 0),
  available_quantity NUMBER DEFAULT 0 NOT NULL,
  CONSTRAINT ck_book_availability
    CHECK (available_quantity >= 0 AND available_quantity <= quantity)
);
CREATE SEQUENCE book_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER book_trigger BEFORE INSERT ON book FOR EACH ROW
BEGIN
  IF :NEW.book_id IS NULL THEN
    SELECT book_seq.NEXTVAL INTO :NEW.book_id FROM dual;
  END IF;
END;
/
CREATE UNIQUE INDEX uq_book_identity
ON book(LOWER(TRIM(title)), author_id, category_id);
```

## database/schema/circulation.sql

Source: [মূল ফাইল](../../database/schema/circulation.sql)

```sql
-- Loans, returns and fines
CREATE TABLE issue_book (
  issue_id NUMBER PRIMARY KEY,
  student_id NUMBER NOT NULL REFERENCES student(student_id),
  book_id NUMBER NOT NULL REFERENCES book(book_id),
  issue_date DATE DEFAULT SYSDATE NOT NULL,
  due_date DATE,
  return_date DATE,
  status VARCHAR2(20) DEFAULT 'ISSUED' NOT NULL CHECK (status IN ('ISSUED','RETURNED'))
);
CREATE SEQUENCE issue_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER issue_trigger BEFORE INSERT ON issue_book FOR EACH ROW
BEGIN
  IF :NEW.issue_id IS NULL THEN
    SELECT issue_seq.NEXTVAL INTO :NEW.issue_id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE PROCEDURE issue_book_proc(
  p_student_id NUMBER,
  p_book_id NUMBER
) AS
  v_membership_status student.membership_status%TYPE;
  v_active_loans NUMBER;
  v_unpaid_fines NUMBER;
BEGIN
  SELECT membership_status INTO v_membership_status
  FROM student
  WHERE student_id = p_student_id
  FOR UPDATE;

  IF v_membership_status <> 'ACTIVE' THEN
    RAISE_APPLICATION_ERROR(-20005, 'This membership is disabled');
  END IF;

  SELECT COUNT(*) INTO v_active_loans
  FROM issue_book
  WHERE student_id = p_student_id AND status = 'ISSUED';

  IF v_active_loans > 0 THEN
    RAISE_APPLICATION_ERROR(-20006, 'Return the current book before issuing another book');
  END IF;

  SELECT COUNT(*) INTO v_unpaid_fines
  FROM fine f
  JOIN issue_book i ON i.issue_id = f.issue_id
  WHERE i.student_id = p_student_id AND f.payment_status = 'UNPAID';

  IF v_unpaid_fines > 0 THEN
    RAISE_APPLICATION_ERROR(-20007, 'Pay all unpaid fines before issuing another book');
  END IF;

  INSERT INTO issue_book(student_id, book_id, issue_date, due_date, status)
  VALUES(p_student_id, p_book_id, SYSDATE, SYSDATE + 15, 'ISSUED');
END;
/

CREATE TABLE return_book (
  return_id NUMBER PRIMARY KEY,
  issue_id NUMBER NOT NULL UNIQUE REFERENCES issue_book(issue_id),
  return_date DATE DEFAULT SYSDATE NOT NULL,
  fine_amount NUMBER DEFAULT 0 NOT NULL CHECK (fine_amount >= 0),
  status VARCHAR2(20) DEFAULT 'RETURNED' NOT NULL
);
CREATE SEQUENCE return_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER return_trigger BEFORE INSERT ON return_book FOR EACH ROW
BEGIN
  IF :NEW.return_id IS NULL THEN
    SELECT return_seq.NEXTVAL INTO :NEW.return_id FROM dual;
  END IF;
END;
/

CREATE TABLE fine (
  fine_id NUMBER PRIMARY KEY,
  issue_id NUMBER NOT NULL UNIQUE REFERENCES issue_book(issue_id),
  amount NUMBER DEFAULT 0 NOT NULL CHECK (amount >= 0),
  payment_status VARCHAR2(20) DEFAULT 'UNPAID' NOT NULL CHECK (payment_status IN ('PAID','UNPAID'))
);
CREATE SEQUENCE fine_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER fine_trigger BEFORE INSERT ON fine FOR EACH ROW
BEGIN
  IF :NEW.fine_id IS NULL THEN
    SELECT fine_seq.NEXTVAL INTO :NEW.fine_id FROM dual;
  END IF;
END;
/
ALTER PROCEDURE issue_book_proc COMPILE;
```

## database/schema/members.sql

Source: [মূল ফাইল](../../database/schema/members.sql)

```sql
-- People and membership
CREATE TABLE admin (
  admin_id NUMBER PRIMARY KEY,
  name VARCHAR2(100) NOT NULL,
  email VARCHAR2(100) NOT NULL UNIQUE,
  password VARCHAR2(255) NOT NULL
);
CREATE SEQUENCE admin_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER admin_trigger BEFORE INSERT ON admin FOR EACH ROW
BEGIN
  IF :NEW.admin_id IS NULL THEN
    SELECT admin_seq.NEXTVAL INTO :NEW.admin_id FROM dual;
  END IF;
END;
/

CREATE TABLE student (
  student_id NUMBER PRIMARY KEY,
  name VARCHAR2(100) NOT NULL,
  department VARCHAR2(100) NOT NULL,
  phone VARCHAR2(11) NOT NULL UNIQUE,
  email VARCHAR2(100) NOT NULL UNIQUE,
  password VARCHAR2(255) NOT NULL,
  roll_no VARCHAR2(40) NOT NULL,
  registration_no VARCHAR2(40) NOT NULL,
  academic_session VARCHAR2(9) NOT NULL,
  membership_status VARCHAR2(20) DEFAULT 'ACTIVE' NOT NULL,
  CONSTRAINT ck_student_membership CHECK (membership_status IN ('ACTIVE', 'DISABLED')),
  CONSTRAINT ck_student_phone CHECK (
    LENGTH(phone) = 11 AND TRIM(TRANSLATE(phone, '0123456789', ' ')) IS NULL
  )
);
CREATE SEQUENCE student_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER student_trigger BEFORE INSERT ON student FOR EACH ROW
BEGIN
  IF :NEW.student_id IS NULL THEN
    SELECT student_seq.NEXTVAL INTO :NEW.student_id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER student_session_trigger
BEFORE INSERT OR UPDATE OF academic_session ON student
FOR EACH ROW
BEGIN
  :NEW.academic_session := TRIM(:NEW.academic_session);
  IF :NEW.academic_session IS NULL THEN
    RAISE_APPLICATION_ERROR(-20022, 'Academic session is required');
  END IF;
  IF REGEXP_LIKE(:NEW.academic_session, '^[0-9]{4}-[0-9]{2}$') THEN
    IF TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1 > 9999 OR
       TO_NUMBER(SUBSTR(:NEW.academic_session,6,2)) <> MOD(TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1,100) THEN
      RAISE_APPLICATION_ERROR(-20023, 'Academic session must cover consecutive years');
    END IF;
    :NEW.academic_session := SUBSTR(:NEW.academic_session,1,5) ||
      TO_CHAR(TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1,'FM0000');
  END IF;
  IF NOT REGEXP_LIKE(:NEW.academic_session, '^[0-9]{4}-[0-9]{4}$') THEN
    RAISE_APPLICATION_ERROR(-20023, 'Academic session must use YYYY-YY or YYYY-YYYY');
  END IF;
  IF TO_NUMBER(SUBSTR(:NEW.academic_session,6,4)) <> TO_NUMBER(SUBSTR(:NEW.academic_session,1,4))+1 THEN
    RAISE_APPLICATION_ERROR(-20023, 'Academic session must cover consecutive years');
  END IF;
END;
/
CREATE OR REPLACE TRIGGER student_identity_trigger
BEFORE INSERT OR UPDATE OF roll_no, registration_no ON student
FOR EACH ROW
BEGIN
  :NEW.roll_no := UPPER(TRIM(:NEW.roll_no));
  :NEW.registration_no := UPPER(TRIM(:NEW.registration_no));
  IF :NEW.roll_no IS NULL OR :NEW.registration_no IS NULL THEN
    RAISE_APPLICATION_ERROR(-20020, 'Both ID/Roll and Registration No. are required');
  END IF;
  IF NOT REGEXP_LIKE(:NEW.roll_no, '^[A-Z0-9][A-Z0-9./_-]{0,39}$') OR
     NOT REGEXP_LIKE(:NEW.registration_no, '^[A-Z0-9][A-Z0-9./_-]{0,39}$') THEN
    RAISE_APPLICATION_ERROR(-20021, 'Invalid ID/Roll or Registration No.');
  END IF;
END;
/
CREATE OR REPLACE PROCEDURE add_student_proc(
  p_name VARCHAR2,
  p_department VARCHAR2,
  p_phone VARCHAR2,
  p_email VARCHAR2,
  p_password VARCHAR2,
  p_roll_no VARCHAR2 DEFAULT NULL,
  p_registration_no VARCHAR2 DEFAULT NULL,
  p_academic_session VARCHAR2 DEFAULT NULL
) AS
BEGIN
  INSERT INTO student(name, department, phone, email, password, roll_no, registration_no, academic_session)
  VALUES(TRIM(p_name), TRIM(p_department), TRIM(p_phone), LOWER(TRIM(p_email)),
         p_password, UPPER(TRIM(p_roll_no)), UPPER(TRIM(p_registration_no)), TRIM(p_academic_session));
END;
/
```

## database/schema/reset.sql

Source: [মূল ফাইল](../../database/schema/reset.sql)

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

## database/schema/routines.sql

Source: [মূল ফাইল](../../database/schema/routines.sql)

```sql
CREATE OR REPLACE TRIGGER issue_quantity_trigger
BEFORE INSERT ON issue_book FOR EACH ROW
DECLARE
  available_count NUMBER;
BEGIN
  SELECT available_quantity INTO available_count
  FROM book WHERE book_id = :NEW.book_id FOR UPDATE;
  IF available_count <= 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Book is not available');
  END IF;
  UPDATE book SET available_quantity = available_quantity - 1
  WHERE book_id = :NEW.book_id;
  IF :NEW.issue_date IS NULL THEN
    :NEW.issue_date := SYSDATE;
  END IF;
  IF :NEW.due_date IS NULL THEN
    :NEW.due_date := :NEW.issue_date + 15;
  END IF;
END;
/

CREATE OR REPLACE PROCEDURE return_book_proc(p_issue_id NUMBER) AS
  v_book_id NUMBER;
  v_status VARCHAR2(20);
  v_due_date DATE;
  v_fine NUMBER;
BEGIN
  SELECT book_id, status, due_date INTO v_book_id, v_status, v_due_date
  FROM issue_book WHERE issue_id = p_issue_id FOR UPDATE;
  IF v_status = 'RETURNED' THEN
    RAISE_APPLICATION_ERROR(-20002, 'Book is already returned');
  END IF;
  v_fine := GREATEST(TRUNC(SYSDATE) - TRUNC(NVL(v_due_date, SYSDATE)), 0) * 10;
  INSERT INTO return_book(issue_id, return_date, fine_amount, status)
  VALUES(p_issue_id, SYSDATE, v_fine, 'RETURNED');
  UPDATE issue_book SET status = 'RETURNED', return_date = SYSDATE
  WHERE issue_id = p_issue_id;
  UPDATE book SET available_quantity = available_quantity + 1
  WHERE book_id = v_book_id;
  IF v_fine > 0 THEN
    INSERT INTO fine(issue_id, amount, payment_status)
    VALUES(p_issue_id, v_fine, 'UNPAID');
  END IF;
END;
/

CREATE OR REPLACE FUNCTION check_book_available(p_book_id NUMBER) RETURN VARCHAR2 IS
  qty NUMBER;
BEGIN
  SELECT available_quantity INTO qty FROM book WHERE book_id = p_book_id;
  IF qty > 0 THEN
    RETURN 'AVAILABLE';
  ELSE
    RETURN 'NOT AVAILABLE';
  END IF;
END;
/

CREATE OR REPLACE VIEW book_details AS
SELECT b.book_id, b.title, a.author_name, c.category_name, b.publisher, b.quantity, b.available_quantity
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN category c ON b.category_id = c.category_id;
```

## database/schema/sample_data.sql

Source: [মূল ফাইল](../../database/schema/sample_data.sql)

```sql
-- Sample members use the example session 2023-2024.
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Rahim','CSE','01700000001','rahim@gmail.com',DBMS_RANDOM.STRING('X',30),'2300001','11700','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Karim','EEE','01700000002','karim@gmail.com',DBMS_RANDOM.STRING('X',30),'2300002','11701','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Sadia','BBA','01700000003','sadia@gmail.com',DBMS_RANDOM.STRING('X',30),'2300003','11702','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Nusrat Jahan','CSE','01700000004','nusrat@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300004','11703','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Tanvir Hasan','Agriculture','01700000005','tanvir@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300005','11704','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Mehedi Islam','EEE','01700000006','mehedi@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300006','11705','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Farzana Akter','Nutrition and Food Science','01700000007','farzana@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300007','11706','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Tasnim','CSE','01700000008','tasnim@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300008','11707','2023-2024');
INSERT INTO author(author_name) VALUES('Robert C. Martin');
INSERT INTO author(author_name) VALUES('Herbert Schildt');
INSERT INTO author(author_name) VALUES('Elmasri & Navathe');
INSERT INTO author(author_name) VALUES('Abraham Silberschatz');
INSERT INTO author(author_name) VALUES('Thomas H. Cormen');
INSERT INTO author(author_name) VALUES('Andrew S. Tanenbaum');
INSERT INTO category(category_name) VALUES('Database');
INSERT INTO category(category_name) VALUES('Programming');
INSERT INTO category(category_name) VALUES('Software Engineering');
INSERT INTO category(category_name) VALUES('Algorithms');
INSERT INTO category(category_name) VALUES('Computer Networks');
INSERT INTO category(category_name) VALUES('Operating Systems');
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Database System Concepts',4,1,'McGraw Hill',10,10);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Java Programming',2,2,'Tata McGraw',8,8);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Clean Code',1,3,'Pearson',5,5);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Operating System Concepts',4,6,'Wiley',7,7);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Introduction to Algorithms',5,4,'MIT Press',6,6);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Computer Networks',6,5,'Pearson',9,9);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Effective Java',2,2,'Addison-Wesley',4,4);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Clean Architecture',1,3,'Pearson',5,5);
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(1,1,SYSDATE,SYSDATE+15,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(2,2,SYSDATE,SYSDATE+15,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(4,5,SYSDATE-2,SYSDATE+13,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(5,6,SYSDATE-25,SYSDATE-10,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(6,4,SYSDATE-18,SYSDATE-3,'ISSUED');
BEGIN return_book_proc(4); END;
/
BEGIN return_book_proc(5); END;
/
UPDATE fine SET payment_status='PAID',paid_amount=amount WHERE issue_id=5;
COMMIT;

INSERT INTO login_user(username,password,user_type) VALUES(:seed_admin_username,:seed_admin_password,'ADMIN');
COMMIT;
```

## database/schema/verify.sql

Source: [মূল ফাইল](../../database/schema/verify.sql)

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

## database/setup.sql

Source: [মূল ফাইল](../../database/setup.sql)

```sql
-- Fresh installation only: Setup-Database.bat requires RESET.
-- Run this entry point; schema modules depend on this order.

@@schema/reset.sql
@@schema/members.sql
@@schema/catalogue.sql
@@schema/circulation.sql
@@schema/accounts.sql
@@schema/routines.sql
-- Audit tables and triggers must exist before loading sample records.
@@circulation_upgrade.sql
@@reservations_upgrade.sql
@@student_activation_upgrade.sql
@@members_audit.sql
@@reservations_audit_upgrade.sql
@@reminders_upgrade.sql

@@schema/sample_data.sql
@@schema/verify.sql
```

## database/student_activation_upgrade.sql

Source: [মূল ফাইল](../../database/student_activation_upgrade.sql)

```sql
-- First-time student activation; preserves existing accounts and passwords.
SET DEFINE OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
DECLARE n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name='LOGIN_USER' AND column_name='MEMBER_ACTIVATED_AT';
  IF n=0 THEN EXECUTE IMMEDIATE 'ALTER TABLE login_user ADD (member_activated_at DATE)'; END IF;
END;
/
CREATE OR REPLACE PROCEDURE activate_student_proc(p_student_id NUMBER,p_phone VARCHAR2,p_password_hash VARCHAR2) AS
  v_phone VARCHAR2(11); v_membership VARCHAR2(20); v_user NUMBER;
  v_activated DATE; v_status VARCHAR2(20); v_username VARCHAR2(100);
BEGIN
  BEGIN
    SELECT phone,membership_status INTO v_phone,v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20040,'Member ID or registered phone number does not match'); END;
  IF p_phone IS NULL OR v_phone<>p_phone THEN RAISE_APPLICATION_ERROR(-20040,'Member ID or registered phone number does not match'); END IF;
  IF v_membership<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)<>'pbkdf2$' THEN RAISE_APPLICATION_ERROR(-20041,'Invalid password hash'); END IF;
  v_username:='PSTU-'||LPAD(TO_CHAR(p_student_id,'FM99999999999999999990'),GREATEST(4,LENGTH(TO_CHAR(p_student_id,'FM99999999999999999990'))),'0');
  BEGIN
    SELECT user_id,member_activated_at,account_status INTO v_user,v_activated,v_status FROM login_user WHERE student_id=p_student_id AND user_type='STUDENT' FOR UPDATE;
    IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20042,'This account is disabled. Contact the library desk'); END IF;
    IF v_activated IS NOT NULL THEN RAISE_APPLICATION_ERROR(-20043,'Account already activated. Sign in with your Member ID and password'); END IF;
    UPDATE login_user SET username=v_username,password=p_password_hash,member_activated_at=SYSDATE WHERE user_id=v_user;
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO login_user(username,password,user_type,account_status,student_id,member_activated_at)
      VALUES(v_username,p_password_hash,'STUDENT','ACTIVE',p_student_id,SYSDATE);
  END;
END;
/
CREATE OR REPLACE PROCEDURE reset_student_password_proc(p_student_id NUMBER,p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2,p_password_hash VARCHAR2) AS
  v_count NUMBER; v_lock NUMBER; v_user NUMBER; v_status VARCHAR2(20);
BEGIN
  BEGIN
    SELECT student_id INTO v_lock FROM student WHERE student_id=p_student_id FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20044,'Member details do not match'); END;
  SELECT COUNT(*) INTO v_count FROM student WHERE student_id=p_student_id
    AND UPPER(TRIM(roll_no))=UPPER(TRIM(p_roll)) AND UPPER(TRIM(registration_no))=UPPER(TRIM(p_registration))
    AND phone=p_phone AND LOWER(TRIM(email))=LOWER(TRIM(p_email));
  IF v_count<>1 THEN RAISE_APPLICATION_ERROR(-20044,'Member details do not match'); END IF;
  SELECT membership_status INTO v_status FROM student WHERE student_id=p_student_id;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  BEGIN
    SELECT user_id,account_status INTO v_user,v_status FROM login_user WHERE student_id=p_student_id AND user_type='STUDENT' FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20045,'Activate your member account before resetting its password'); END;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20042,'This account is disabled. Contact the library desk'); END IF;
  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)<>'pbkdf2$' THEN RAISE_APPLICATION_ERROR(-20041,'Invalid password hash'); END IF;
  UPDATE login_user SET password=p_password_hash,member_activated_at=NVL(member_activated_at,SYSDATE) WHERE user_id=v_user;
END;
/
COMMIT;
```
