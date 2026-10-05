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
