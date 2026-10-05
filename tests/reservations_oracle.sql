-- Real Oracle checks; test records, loans and holds are always rolled back.
SET SERVEROUTPUT ON
DECLARE
  v_student NUMBER; v_other NUMBER; v_book NUMBER; v_second NUMBER;
  v_third NUMBER; v_fourth NUMBER; v_author NUMBER; v_category NUMBER;
  v_copy NUMBER; v_reservation NUMBER; v_count NUMBER; v_issue NUMBER;
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
BEGIN
  SELECT MIN(author_id) INTO v_author FROM author;
  SELECT MIN(category_id) INTO v_category FROM category;
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Reservation QA','QA','09888888881','reservation-qa1@invalid.test','unused','RES-QA1','RES-REG1','2025-2026') RETURNING student_id INTO v_student;
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Reservation other QA','QA','09888888882','reservation-qa2@invalid.test','unused','RES-QA2','RES-REG2','2025-2026') RETURNING student_id INTO v_other;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 1',v_author,v_category,1,1) RETURNING book_id INTO v_book;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 2',v_author,v_category,2,2) RETURNING book_id INTO v_second;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 3',v_author,v_category,1,1) RETURNING book_id INTO v_third;
  INSERT INTO book(title,author_id,category_id,quantity,available_quantity) VALUES('Reservation QA 4',v_author,v_category,1,1) RETURNING book_id INTO v_fourth;
  reserve_book_proc(v_student,v_book);
  SELECT reservation_id,copy_id INTO v_reservation,v_copy FROM book_reservation WHERE student_id=v_student AND book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE reservation_id=v_reservation AND ABS(expires_at-reserved_at-3)<1/86400;
  check_true(v_count=1,'Reservation must last exactly three days');
  BEGIN reserve_book_proc(v_other,v_book); RAISE_APPLICATION_ERROR(-20999,'Last copy reserved twice');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20001 THEN RAISE; END IF; END;
  BEGIN issue_book_proc(v_other,v_book,v_copy); RAISE_APPLICATION_ERROR(-20999,'Reserved copy issued to another member');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20031 THEN RAISE; END IF; END;
  BEGIN issue_book_proc(v_other,v_book); RAISE_APPLICATION_ERROR(-20999,'Auto selection stole reserved copy');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20001 THEN RAISE; END IF; END;
  BEGIN UPDATE book SET quantity=0,available_quantity=0 WHERE book_id=v_book; RAISE_APPLICATION_ERROR(-20999,'Reserved stock retired');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20008 THEN RAISE; END IF; END;
  reserve_book_proc(v_student,v_second);
  BEGIN reserve_book_proc(v_student,v_second); RAISE_APPLICATION_ERROR(-20999,'Duplicate title reservation accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20030 THEN RAISE; END IF; END;
  reserve_book_proc(v_student,v_third);
  BEGIN reserve_book_proc(v_student,v_fourth); RAISE_APPLICATION_ERROR(-20999,'Fourth hold accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20006 THEN RAISE; END IF; END;
  -- Pickup replaces one hold with one loan, even with three occupied slots.
  issue_book_proc(v_student,v_book);
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE reservation_id=v_reservation AND status='COLLECTED';
  check_true(v_count=1,'Pickup must collect the reservation');
  SELECT issue_id INTO v_issue FROM issue_book WHERE student_id=v_student AND book_id=v_book;
  SELECT COUNT(*) INTO v_count FROM issue_book WHERE issue_id=v_issue AND ABS(due_date-issue_date-15)<1/86400;
  check_true(v_count=1,'Reserved pickup must create a 15-day loan');
  return_book_proc(v_issue);
  -- Effective expiry releases stock before the background job runs.
  UPDATE book_reservation SET expires_at=SYSDATE-1/86400 WHERE student_id=v_student AND book_id=v_third;
  reserve_book_proc(v_other,v_third);
  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE student_id=v_student AND book_id=v_third AND status='EXPIRED';
  check_true(v_count=1,'Expired reservation must be cancelled automatically');
  UPDATE book_reservation SET status='CANCELLED' WHERE student_id=v_student AND book_id=v_second;
  reserve_book_proc(v_other,v_second);
  UPDATE student SET membership_status='DISABLED' WHERE student_id=v_student;
  BEGIN reserve_book_proc(v_student,v_fourth); RAISE_APPLICATION_ERROR(-20999,'Disabled member reserved a book');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20005 THEN RAISE; END IF; END;
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: last copy, owner protection, stock reduction, limits, pickup, expiry, cancellation, membership');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
