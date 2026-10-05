-- Integration checks against Oracle. All test rows and changes are rolled back.
SET SERVEROUTPUT ON
DECLARE
  v_student NUMBER; v_book NUMBER; v_issue NUMBER; v_fine NUMBER;
  v_count NUMBER; v_total NUMBER; v_available NUMBER; v_copy NUMBER;
  v_paid NUMBER; v_status VARCHAR2(20);
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
BEGIN
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
  VALUES('Circulation rollback test','QA','09999999999','circulation-rollback-test@invalid.test','unused','QA-ROLL-TEST','QA-REG-TEST','2025-2026') RETURNING student_id INTO v_student;
  SELECT MIN(book_id) INTO v_book FROM book WHERE available_quantity>=4;
  check_true(v_book IS NOT NULL,'A book with at least four available copies is required');
  SELECT quantity,available_quantity INTO v_total,v_available FROM book WHERE book_id=v_book;
  -- Stock additions/removal must also add/retire physical copies.
  UPDATE book SET quantity=quantity+2,available_quantity=available_quantity+2 WHERE book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=v_book AND status<>'RETIRED';
  check_true(v_count=v_total+2,'Stock add mismatch');
  UPDATE book SET quantity=quantity-2,available_quantity=available_quantity-2 WHERE book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=v_book AND status<>'RETIRED';
  check_true(v_count=v_total,'Stock reduction mismatch');
  issue_book_proc(v_student,v_book);
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND ABS(due_date-issue_date-15)<1/86400;
  check_true(v_count=1,'New loan must be due 15 days after issue');
  issue_book_proc(v_student,v_book);
  issue_book_proc(v_student,v_book);
  SELECT COUNT(DISTINCT copy_id) INTO v_count FROM issue_book WHERE student_id=v_student AND status='ISSUED';
  check_true(v_count=3,'Three distinct physical copies required');
  BEGIN
    issue_book_proc(v_student,v_book);
    RAISE_APPLICATION_ERROR(-20999,'Fourth loan unexpectedly accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20006 THEN RAISE; END IF; END;
  SELECT MIN(issue_id) INTO v_issue FROM issue_book WHERE student_id=v_student;
  SELECT copy_id INTO v_copy FROM issue_book WHERE issue_id=v_issue;
  UPDATE issue_book SET due_date=TRUNC(SYSDATE)-10 WHERE issue_id=v_issue;
  return_book_proc(v_issue);
  SELECT status INTO v_status FROM book_copy WHERE copy_id=v_copy;
  check_true(v_status='AVAILABLE','Returned physical copy must become available');
  SELECT available_quantity INTO v_count FROM book WHERE book_id=v_book;
  check_true(v_count=v_available-2,'Only returned copy must restore stock');
  BEGIN
    return_book_proc(v_issue);
    RAISE_APPLICATION_ERROR(-20999,'Double return accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20002 THEN RAISE; END IF; END;
  SELECT fine_id,amount INTO v_fine,v_paid FROM fine WHERE issue_id=v_issue;
  check_true(v_paid=100,'Final overdue fine incorrect');
  BEGIN
    pay_fine_proc(v_fine,35.25,'Partial payment attempt');
    RAISE_APPLICATION_ERROR(-20999,'Partial payment accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20012 THEN RAISE; END IF; END;
  SELECT paid_amount,payment_status INTO v_paid,v_status FROM fine WHERE fine_id=v_fine;
  check_true(v_paid=0 AND v_status='UNPAID','Rejected payment changed balance');
  SELECT COUNT(*) INTO v_count FROM fine_payment WHERE fine_id=v_fine;
  check_true(v_count=0,'Rejected payment created a receipt');
  BEGIN
    pay_fine_proc(v_fine,100.01);
    RAISE_APPLICATION_ERROR(-20999,'Overpayment accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20012 THEN RAISE; END IF; END;
  BEGIN
    issue_book_proc(v_student,v_book,v_copy);
    RAISE_APPLICATION_ERROR(-20999,'Unpaid fine did not block loan');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20007 THEN RAISE; END IF; END;
  pay_fine_proc(v_fine);
  SELECT paid_amount,payment_status INTO v_paid,v_status FROM fine WHERE fine_id=v_fine;
  check_true(v_paid=100 AND v_status='PAID','Final settlement incorrect');
  SELECT COUNT(*) INTO v_count FROM fine_payment WHERE fine_id=v_fine;
  check_true(v_count=1,'One full payment receipt required');
  SELECT copy_id INTO v_count FROM issue_book WHERE issue_id=(SELECT MIN(issue_id) FROM issue_book WHERE student_id=v_student AND status='ISSUED');
  BEGIN
    issue_book_proc(v_student,v_book,v_count);
    RAISE_APPLICATION_ERROR(-20999,'Already borrowed copy accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20010 THEN RAISE; END IF; END;
  issue_book_proc(v_student,v_book,v_copy);
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND copy_id=v_copy;
  check_true(v_count=2,'Returned copy should be reusable');
  BEGIN
    pay_fine_proc(v_fine);
    RAISE_APPLICATION_ERROR(-20999,'Duplicate payment accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20011 THEN RAISE; END IF; END;
  -- A failed selection must roll back earlier issues from the same request.
  SELECT MAX(issue_id) INTO v_issue FROM issue_book WHERE student_id=v_student;
  return_book_proc(v_issue);
  SAVEPOINT batch_test;
  BEGIN
    issue_book_proc(v_student,v_book,v_copy);
    issue_book_proc(v_student,v_book);
    RAISE_APPLICATION_ERROR(-20999,'Failed batch unexpectedly accepted');
  EXCEPTION WHEN OTHERS THEN
    IF SQLCODE<>-20006 THEN RAISE; END IF;
    ROLLBACK TO batch_test;
  END;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=v_student AND status='ISSUED';
  check_true(v_count=2,'Failed batch must preserve initial loans');
  SELECT status INTO v_status FROM book_copy WHERE copy_id=v_copy;
  check_true(v_status='AVAILABLE','Failed batch must restore copy availability');
  -- Direct inserts with a historical issue date also derive the deadline from that date.
  INSERT INTO issue_book(student_id,book_id,issue_date,status) VALUES(v_student,v_book,SYSDATE-2,'ISSUED') RETURNING issue_id INTO v_issue;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE issue_id=v_issue AND ABS(due_date-issue_date-15)<1/86400;
  check_true(v_count=1,'Default due date must be based on issue date, not today');
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: copies, loan limit, stock, returns, full payments, receipts');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
