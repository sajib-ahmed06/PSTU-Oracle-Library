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

