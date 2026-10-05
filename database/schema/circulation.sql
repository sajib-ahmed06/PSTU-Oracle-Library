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

