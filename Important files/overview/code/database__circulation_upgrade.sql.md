# database/circulation_upgrade.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/circulation_upgrade.sql)। Snapshot 2026-10-04; 125 lines; SHA-256 `aa52ff7d3db0dcb2758a9c0e08711f85e4cbb6d3982caa10d6c55cf4b0375f0f`।

## Function / object / element inventory

- **TABLE `book_copy`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `copy_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **INDEX `uq_active_copy`**: Database integrity/search performance enforce করে।
- **TABLE `fine_payment`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `payment_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **TRIGGER `book_copy_stock_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TRIGGER `issue_quantity_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `issue_book_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `return_book_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `pay_fine_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

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

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Non-destructive, rerunnable upgrade. Run as CONFIGURED_SCHEMA while the app is stopped.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET DEFINE OFF</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 4 | <code>DECLARE n NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  SELECT COUNT(*) INTO n FROM user_tables WHERE table_name=&#x27;BOOK_COPY&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 7 | <code>  IF n=0 THEN</code> | PL/SQL condition/alternative branch। |
| 8 | <code>    EXECUTE IMMEDIATE &#x27;CREATE TABLE book_copy (copy_id NUMBER PRIMARY KEY, book_id NUMBER NOT NULL REFERENCES book(book_id), copy_no NUMBER NOT NULL, status VARCHAR2(10) DEFAULT &#x27;&#x27;AVAILABLE&#x27;&#x27; NOT NULL CHECK(status IN (&#x27;&#x27;AVAILABLE&#x27;&#x27;,&#x27;&#x27;ISSUED&#x27;&#x27;,&#x27;&#x27;RETIRED&#x27;&#x27;)), UNIQUE(book_id,copy_no), UNIQUE(book_id,copy_id))&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 9 | <code>    EXECUTE IMMEDIATE &#x27;CREATE SEQUENCE copy_seq&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 10 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 11 | <code>  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name=&#x27;ISSUE_BOOK&#x27; AND column_name=&#x27;COPY_ID&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 12 | <code>  IF n=0 THEN</code> | PL/SQL condition/alternative branch। |
| 13 | <code>    EXECUTE IMMEDIATE &#x27;ALTER TABLE issue_book ADD (copy_id NUMBER)&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 14 | <code>    EXECUTE IMMEDIATE &#x27;ALTER TABLE issue_book ADD CONSTRAINT issue_copy_fk FOREIGN KEY(book_id,copy_id) REFERENCES book_copy(book_id,copy_id)&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 15 | <code>    EXECUTE IMMEDIATE &#x27;CREATE UNIQUE INDEX uq_active_copy ON issue_book(CASE WHEN status=&#x27;&#x27;ISSUED&#x27;&#x27; THEN copy_id END)&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 16 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 17 | <code>  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name=&#x27;FINE&#x27; AND column_name=&#x27;PAID_AMOUNT&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 18 | <code>  IF n=0 THEN</code> | PL/SQL condition/alternative branch। |
| 19 | <code>    EXECUTE IMMEDIATE &#x27;ALTER TABLE fine ADD (paid_amount NUMBER(12,2) DEFAULT 0 NOT NULL)&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 20 | <code>    EXECUTE IMMEDIATE &#x27;UPDATE fine SET paid_amount=amount WHERE payment_status=&#x27;&#x27;PAID&#x27;&#x27;&#x27;;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 21 | <code>    EXECUTE IMMEDIATE &#x27;ALTER TABLE fine ADD CONSTRAINT fine_paid_ck CHECK(paid_amount&gt;=0 AND paid_amount&lt;=amount)&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 22 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 23 | <code>  SELECT COUNT(*) INTO n FROM user_tables WHERE table_name=&#x27;FINE_PAYMENT&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 24 | <code>  IF n=0 THEN</code> | PL/SQL condition/alternative branch। |
| 25 | <code>    EXECUTE IMMEDIATE &#x27;CREATE TABLE fine_payment (payment_id NUMBER PRIMARY KEY, fine_id NUMBER NOT NULL REFERENCES fine(fine_id), amount NUMBER(12,2) NOT NULL CHECK(amount&gt;0), paid_at DATE DEFAULT SYSDATE NOT NULL, actor VARCHAR2(100) NOT NULL, note VARCHAR2(300))&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 26 | <code>    EXECUTE IMMEDIATE &#x27;CREATE SEQUENCE payment_seq&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 27 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 28 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 29 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 30 | <code>-- Assign numbers to existing stock. Historical returned loans have no known copy.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 31 | <code>DECLARE v_copy NUMBER; v_count NUMBER; v_max NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 32 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 33 | <code>  FOR b IN (SELECT book_id,quantity FROM book ORDER BY book_id FOR UPDATE) LOOP</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 34 | <code>    SELECT COUNT(*),NVL(MAX(copy_no),0) INTO v_count,v_max FROM book_copy WHERE book_id=b.book_id AND status&lt;&gt;&#x27;RETIRED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 35 | <code>    IF v_count &lt; b.quantity THEN</code> | PL/SQL condition/alternative branch। |
| 36 | <code>      FOR j IN 1..(b.quantity-v_count) LOOP</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>        INSERT INTO book_copy(copy_id,book_id,copy_no) VALUES(copy_seq.NEXTVAL,b.book_id,v_max+j);</code> | নতুন business/audit/sample row insert করার statement। |
| 38 | <code>      END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 39 | <code>    END IF;</code> | PL/SQL condition/alternative branch। |
| 40 | <code>    FOR i IN (SELECT issue_id FROM issue_book WHERE book_id=b.book_id AND status=&#x27;ISSUED&#x27; AND copy_id IS NULL ORDER BY issue_id) LOOP</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 41 | <code>      SELECT MIN(copy_id) INTO v_copy FROM book_copy WHERE book_id=b.book_id AND status=&#x27;AVAILABLE&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 42 | <code>      IF v_copy IS NULL THEN RAISE_APPLICATION_ERROR(-20009,&#x27;Existing loans exceed stock&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 43 | <code>      UPDATE book_copy SET status=&#x27;ISSUED&#x27; WHERE copy_id=v_copy;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 44 | <code>      UPDATE issue_book SET copy_id=v_copy WHERE issue_id=i.issue_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 45 | <code>    END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 46 | <code>  END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 47 | <code>  COMMIT;</code> | Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ। |
| 48 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 49 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 50 | <code>CREATE OR REPLACE TRIGGER book_copy_stock_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 51 | <code>AFTER INSERT OR UPDATE OF quantity ON book FOR EACH ROW</code> | নতুন business/audit/sample row insert করার statement। |
| 52 | <code>DECLARE v_max NUMBER; v_delta NUMBER; v_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 53 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 54 | <code>  v_delta := :NEW.quantity - NVL(:OLD.quantity,0);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 55 | <code>  IF v_delta&gt;0 THEN</code> | PL/SQL condition/alternative branch। |
| 56 | <code>    SELECT NVL(MAX(copy_no),0) INTO v_max FROM book_copy WHERE book_id=:NEW.book_id;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 57 | <code>    FOR j IN 1..v_delta LOOP</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 58 | <code>      INSERT INTO book_copy(copy_id,book_id,copy_no) VALUES(copy_seq.NEXTVAL,:NEW.book_id,v_max+j);</code> | নতুন business/audit/sample row insert করার statement। |
| 59 | <code>    END LOOP;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 60 | <code>  ELSIF v_delta&lt;0 THEN</code> | PL/SQL condition/alternative branch। |
| 61 | <code>    SELECT COUNT(*) INTO v_count FROM book_copy WHERE book_id=:NEW.book_id AND status=&#x27;AVAILABLE&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 62 | <code>    IF v_count &lt; -v_delta THEN RAISE_APPLICATION_ERROR(-20008,&#x27;Only available copies can be removed&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 63 | <code>    UPDATE book_copy SET status=&#x27;RETIRED&#x27; WHERE copy_id IN</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 64 | <code>      (SELECT copy_id FROM (SELECT copy_id FROM book_copy WHERE book_id=:NEW.book_id AND status=&#x27;AVAILABLE&#x27; ORDER BY copy_no DESC) WHERE ROWNUM&lt;=-v_delta);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 65 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 66 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 67 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 68 | <code>CREATE OR REPLACE TRIGGER issue_quantity_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 69 | <code>BEFORE INSERT ON issue_book FOR EACH ROW</code> | নতুন business/audit/sample row insert করার statement। |
| 70 | <code>DECLARE v_available NUMBER; v_status VARCHAR2(10);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 71 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 72 | <code>  SELECT available_quantity INTO v_available FROM book WHERE book_id=:NEW.book_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 73 | <code>  IF v_available&lt;=0 THEN RAISE_APPLICATION_ERROR(-20001,&#x27;Book is not available&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 74 | <code>  IF :NEW.copy_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 75 | <code>    SELECT MIN(copy_id) INTO :NEW.copy_id FROM book_copy WHERE book_id=:NEW.book_id AND status=&#x27;AVAILABLE&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 76 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 77 | <code>  SELECT status INTO v_status FROM book_copy WHERE copy_id=:NEW.copy_id AND book_id=:NEW.book_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 78 | <code>  IF v_status&lt;&gt;&#x27;AVAILABLE&#x27; THEN RAISE_APPLICATION_ERROR(-20010,&#x27;This copy is not available&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 79 | <code>  UPDATE book_copy SET status=&#x27;ISSUED&#x27; WHERE copy_id=:NEW.copy_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 80 | <code>  UPDATE book SET available_quantity=available_quantity-1 WHERE book_id=:NEW.book_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 81 | <code>  IF :NEW.issue_date IS NULL THEN :NEW.issue_date:=SYSDATE; END IF;</code> | PL/SQL condition/alternative branch। |
| 82 | <code>  IF :NEW.due_date IS NULL THEN :NEW.due_date:=:NEW.issue_date+15; END IF;</code> | PL/SQL condition/alternative branch। |
| 83 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 84 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 85 | <code>CREATE OR REPLACE PROCEDURE issue_book_proc(p_student_id NUMBER,p_book_id NUMBER,p_copy_id NUMBER DEFAULT NULL) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 86 | <code>  v_membership VARCHAR2(20); v_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 87 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 88 | <code>  SELECT membership_status INTO v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 89 | <code>  IF v_membership&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20005,&#x27;This membership is disabled&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 90 | <code>  SELECT COUNT(*) INTO v_count FROM issue_book WHERE student_id=p_student_id AND status=&#x27;ISSUED&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 91 | <code>  IF v_count&gt;=3 THEN RAISE_APPLICATION_ERROR(-20006,&#x27;A member may borrow at most 3 copies at a time&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 92 | <code>  SELECT COUNT(*) INTO v_count FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id WHERE i.student_id=p_student_id AND f.amount&gt;f.paid_amount;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 93 | <code>  IF v_count&gt;0 THEN RAISE_APPLICATION_ERROR(-20007,&#x27;Pay all outstanding fines before issuing another book&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 94 | <code>  INSERT INTO issue_book(student_id,book_id,copy_id,issue_date,due_date,status)</code> | নতুন business/audit/sample row insert করার statement। |
| 95 | <code>  VALUES(p_student_id,p_book_id,p_copy_id,SYSDATE,SYSDATE+15,&#x27;ISSUED&#x27;);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 96 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 97 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 98 | <code>CREATE OR REPLACE PROCEDURE return_book_proc(p_issue_id NUMBER) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 99 | <code>  v_book NUMBER; v_copy NUMBER; v_status VARCHAR2(20); v_due DATE; v_fine NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 100 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 101 | <code>  SELECT book_id,copy_id,status,due_date INTO v_book,v_copy,v_status,v_due FROM issue_book WHERE issue_id=p_issue_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 102 | <code>  IF v_status=&#x27;RETURNED&#x27; THEN RAISE_APPLICATION_ERROR(-20002,&#x27;Book is already returned&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 103 | <code>  v_fine:=GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(v_due,SYSDATE)),0)*10;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 104 | <code>  INSERT INTO return_book(issue_id,return_date,fine_amount,status) VALUES(p_issue_id,SYSDATE,v_fine,&#x27;RETURNED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 105 | <code>  UPDATE issue_book SET status=&#x27;RETURNED&#x27;,return_date=SYSDATE WHERE issue_id=p_issue_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 106 | <code>  UPDATE book SET available_quantity=available_quantity+1 WHERE book_id=v_book;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 107 | <code>  UPDATE book_copy SET status=&#x27;AVAILABLE&#x27; WHERE copy_id=v_copy;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 108 | <code>  IF v_fine&gt;0 THEN INSERT INTO fine(issue_id,amount,payment_status) VALUES(p_issue_id,v_fine,&#x27;UNPAID&#x27;); END IF;</code> | নতুন business/audit/sample row insert করার statement। |
| 109 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 110 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 111 | <code>CREATE OR REPLACE PROCEDURE pay_fine_proc(p_fine_id NUMBER,p_amount NUMBER DEFAULT NULL,p_note VARCHAR2 DEFAULT NULL) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 112 | <code>  v_amount NUMBER; v_paid NUMBER; v_balance NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 113 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 114 | <code>  SELECT amount,paid_amount INTO v_amount,v_paid FROM fine WHERE fine_id=p_fine_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 115 | <code>  v_balance := v_amount-v_paid;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 116 | <code>  IF v_balance&lt;=0 THEN RAISE_APPLICATION_ERROR(-20011,&#x27;This fine is already paid&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 117 | <code>  IF p_amount IS NOT NULL AND p_amount&lt;&gt;v_balance THEN</code> | PL/SQL condition/alternative branch। |
| 118 | <code>    RAISE_APPLICATION_ERROR(-20012,&#x27;The full outstanding fine must be paid&#x27;);</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 119 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 120 | <code>  INSERT INTO fine_payment(payment_id,fine_id,amount,actor,note)</code> | নতুন business/audit/sample row insert করার statement। |
| 121 | <code>  VALUES(payment_seq.NEXTVAL,p_fine_id,v_balance,NVL(SYS_CONTEXT(&#x27;USERENV&#x27;,&#x27;CLIENT_INFO&#x27;),USER),p_note);</code> | Sequence থেকে পরবর্তী unique numeric value নেয়; sequence allocation transaction rollback হয় না। |
| 122 | <code>  UPDATE fine SET paid_amount=v_amount,payment_status=&#x27;PAID&#x27; WHERE fine_id=p_fine_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 123 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 124 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 125 | <code>COMMIT;</code> | Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ। |
