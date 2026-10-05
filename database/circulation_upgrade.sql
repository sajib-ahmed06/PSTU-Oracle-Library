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
