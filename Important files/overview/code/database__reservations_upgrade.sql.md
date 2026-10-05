# database/reservations_upgrade.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/reservations_upgrade.sql)। Snapshot 2026-10-04; 112 lines; SHA-256 `1f17dde0815c1ce822a3175f018e746d9d6387b71581705b2a2403cc8b5496a1`।

## Function / object / element inventory

- **TABLE `book_reservation`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **SEQUENCE `reservation_seq`**: Numeric IDs দেয়; rollback হলেও allocated value ফেরত যায় না।
- **INDEX `uq_reserved_copy`**: Database integrity/search performance enforce করে।
- **INDEX `ix_reservation_member`**: Database integrity/search performance enforce করে।
- **PROCEDURE `expire_reservations_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `reserve_book_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TRIGGER `issue_quantity_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **PROCEDURE `issue_book_proc`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।
- **TRIGGER `book_copy_stock_trigger`**: উপরের Database/Audit chapters-এ business rules; নিচে সম্পূর্ণ definition ও line-by-line notes।

## সম্পূর্ণ original source

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

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Data-preserving student access and three-day physical-copy reservations.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>SET DEFINE OFF</code> | SQL*Plus client output/substitution configuration; database business row update নয়। |
| 3 | <code>WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK</code> | SQL/OS error-এ script failure exit এবং নির্দিষ্ট rollback behavior নির্ধারণ করে। |
| 4 | <code>DECLARE n NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 5 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 6 | <code>  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name=&#x27;LOGIN_USER&#x27; AND column_name=&#x27;STUDENT_ID&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 7 | <code>  IF n=0 THEN</code> | PL/SQL condition/alternative branch। |
| 8 | <code>    EXECUTE IMMEDIATE &#x27;ALTER TABLE login_user ADD (student_id NUMBER REFERENCES student(student_id) UNIQUE)&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 9 | <code>    EXECUTE IMMEDIATE &#x27;ALTER TABLE login_user ADD CONSTRAINT login_student_role_ck CHECK(student_id IS NULL OR user_type=&#x27;&#x27;STUDENT&#x27;&#x27;)&#x27;;</code> | Existing schema/object পরিবর্তন অথবা dependent PL/SQL recompile করে। |
| 10 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 11 | <code>  SELECT COUNT(*) INTO n FROM user_tables WHERE table_name=&#x27;BOOK_RESERVATION&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 12 | <code>  IF n=0 THEN</code> | PL/SQL condition/alternative branch। |
| 13 | <code>    EXECUTE IMMEDIATE &#x27;CREATE TABLE book_reservation (reservation_id NUMBER PRIMARY KEY, student_id NUMBER NOT NULL REFERENCES student(student_id), book_id NUMBER NOT NULL, copy_id NUMBER NOT NULL, reserved_at DATE DEFAULT SYSDATE NOT NULL, expires_at DATE DEFAULT SYSDATE+3 NOT NULL, status VARCHAR2(12) DEFAULT &#x27;&#x27;ACTIVE&#x27;&#x27; NOT NULL CHECK(status IN (&#x27;&#x27;ACTIVE&#x27;&#x27;,&#x27;&#x27;EXPIRED&#x27;&#x27;,&#x27;&#x27;CANCELLED&#x27;&#x27;,&#x27;&#x27;COLLECTED&#x27;&#x27;)), CONSTRAINT reservation_copy_fk FOREIGN KEY(book_id,copy_id) REFERENCES book_copy(book_id,copy_id))&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 14 | <code>    EXECUTE IMMEDIATE &#x27;CREATE SEQUENCE reservation_seq&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 15 | <code>    EXECUTE IMMEDIATE &#x27;CREATE UNIQUE INDEX uq_reserved_copy ON book_reservation(CASE WHEN status=&#x27;&#x27;ACTIVE&#x27;&#x27; THEN copy_id END)&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 16 | <code>    EXECUTE IMMEDIATE &#x27;CREATE INDEX ix_reservation_member ON book_reservation(student_id,status,expires_at)&#x27;;</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 17 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 18 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 19 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 20 | <code>CREATE OR REPLACE PROCEDURE expire_reservations_proc AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 21 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 22 | <code>  UPDATE book_reservation SET status=&#x27;EXPIRED&#x27; WHERE status=&#x27;ACTIVE&#x27; AND expires_at&lt;=SYSDATE;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 23 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 24 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 25 | <code>CREATE OR REPLACE PROCEDURE reserve_book_proc(p_student_id NUMBER,p_book_id NUMBER) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 26 | <code>  v_status VARCHAR2(20); v_count NUMBER; v_copy NUMBER; v_book NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 27 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 28 | <code>  SELECT membership_status INTO v_status FROM student WHERE student_id=p_student_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 29 | <code>  IF v_status&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20005,&#x27;This membership is disabled&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 30 | <code>  SELECT book_id INTO v_book FROM book WHERE book_id=p_book_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 31 | <code>  expire_reservations_proc;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 32 | <code>  SELECT COUNT(*) INTO v_count FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id WHERE i.student_id=p_student_id AND f.amount&gt;f.paid_amount;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 33 | <code>  IF v_count&gt;0 THEN RAISE_APPLICATION_ERROR(-20007,&#x27;Pay all outstanding fines before reserving a book&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 34 | <code>  SELECT (SELECT COUNT(*) FROM issue_book WHERE student_id=p_student_id AND status=&#x27;ISSUED&#x27;)+</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 35 | <code>         (SELECT COUNT(*) FROM book_reservation WHERE student_id=p_student_id AND status=&#x27;ACTIVE&#x27; AND expires_at&gt;SYSDATE)</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 36 | <code>  INTO v_count FROM dual;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 37 | <code>  IF v_count&gt;=3 THEN RAISE_APPLICATION_ERROR(-20006,&#x27;A member may have at most 3 loans and reservations together&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 38 | <code>  SELECT COUNT(*) INTO v_count FROM book_reservation WHERE student_id=p_student_id AND book_id=p_book_id AND status=&#x27;ACTIVE&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 39 | <code>  IF v_count&gt;0 THEN RAISE_APPLICATION_ERROR(-20030,&#x27;You already reserved this title&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 40 | <code>  SELECT MIN(c.copy_id) INTO v_copy FROM book_copy c WHERE c.book_id=p_book_id AND c.status=&#x27;AVAILABLE&#x27;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 41 | <code>    AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status=&#x27;ACTIVE&#x27; AND r.expires_at&gt;SYSDATE);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 42 | <code>  IF v_copy IS NULL THEN RAISE_APPLICATION_ERROR(-20001,&#x27;No available copy to reserve&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 43 | <code>  INSERT INTO book_reservation(reservation_id,student_id,book_id,copy_id) VALUES(reservation_seq.NEXTVAL,p_student_id,p_book_id,v_copy);</code> | নতুন business/audit/sample row insert করার statement। |
| 44 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 45 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 46 | <code>CREATE OR REPLACE TRIGGER issue_quantity_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 47 | <code>BEFORE INSERT ON issue_book FOR EACH ROW</code> | নতুন business/audit/sample row insert করার statement। |
| 48 | <code>DECLARE v_available NUMBER; v_status VARCHAR2(10); v_owner NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 49 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 50 | <code>  SELECT available_quantity INTO v_available FROM book WHERE book_id=:NEW.book_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 51 | <code>  IF v_available&lt;=0 THEN RAISE_APPLICATION_ERROR(-20001,&#x27;Book is not available&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 52 | <code>  IF :NEW.copy_id IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 53 | <code>    SELECT MIN(c.copy_id) INTO :NEW.copy_id FROM book_copy c WHERE c.book_id=:NEW.book_id AND c.status=&#x27;AVAILABLE&#x27;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 54 | <code>      AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status=&#x27;ACTIVE&#x27; AND r.expires_at&gt;SYSDATE);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 55 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 56 | <code>  IF :NEW.copy_id IS NULL THEN RAISE_APPLICATION_ERROR(-20001,&#x27;All available copies are reserved&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 57 | <code>  SELECT status INTO v_status FROM book_copy WHERE copy_id=:NEW.copy_id AND book_id=:NEW.book_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 58 | <code>  IF v_status&lt;&gt;&#x27;AVAILABLE&#x27; THEN RAISE_APPLICATION_ERROR(-20010,&#x27;This copy is not available&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 59 | <code>  SELECT MAX(student_id) INTO v_owner FROM book_reservation WHERE copy_id=:NEW.copy_id AND status=&#x27;ACTIVE&#x27; AND expires_at&gt;SYSDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 60 | <code>  IF v_owner IS NOT NULL AND v_owner&lt;&gt;:NEW.student_id THEN RAISE_APPLICATION_ERROR(-20031,&#x27;This copy is reserved for another member&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 61 | <code>  UPDATE book_reservation SET status=&#x27;COLLECTED&#x27; WHERE copy_id=:NEW.copy_id AND student_id=:NEW.student_id AND status=&#x27;ACTIVE&#x27; AND expires_at&gt;SYSDATE;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 62 | <code>  UPDATE book_copy SET status=&#x27;ISSUED&#x27; WHERE copy_id=:NEW.copy_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 63 | <code>  UPDATE book SET available_quantity=available_quantity-1 WHERE book_id=:NEW.book_id;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 64 | <code>  IF :NEW.issue_date IS NULL THEN :NEW.issue_date:=SYSDATE; END IF;</code> | PL/SQL condition/alternative branch। |
| 65 | <code>  IF :NEW.due_date IS NULL THEN :NEW.due_date:=:NEW.issue_date+15; END IF;</code> | PL/SQL condition/alternative branch। |
| 66 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 67 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 68 | <code>CREATE OR REPLACE PROCEDURE issue_book_proc(p_student_id NUMBER,p_book_id NUMBER,p_copy_id NUMBER DEFAULT NULL) AS</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 69 | <code>  v_membership VARCHAR2(20); v_count NUMBER; v_copy NUMBER:=p_copy_id;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 70 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 71 | <code>  SELECT membership_status INTO v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 72 | <code>  IF v_membership&lt;&gt;&#x27;ACTIVE&#x27; THEN RAISE_APPLICATION_ERROR(-20005,&#x27;This membership is disabled&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 73 | <code>  IF v_copy IS NULL THEN</code> | PL/SQL condition/alternative branch। |
| 74 | <code>    SELECT MIN(copy_id) INTO v_copy FROM book_reservation WHERE student_id=p_student_id AND book_id=p_book_id AND status=&#x27;ACTIVE&#x27; AND expires_at&gt;SYSDATE;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 75 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 76 | <code>  SELECT (SELECT COUNT(*) FROM issue_book WHERE student_id=p_student_id AND status=&#x27;ISSUED&#x27;)+</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 77 | <code>    (SELECT COUNT(*) FROM book_reservation WHERE student_id=p_student_id AND status=&#x27;ACTIVE&#x27; AND expires_at&gt;SYSDATE AND (v_copy IS NULL OR copy_id&lt;&gt;v_copy))</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 78 | <code>  INTO v_count FROM dual;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 79 | <code>  IF v_count&gt;=3 THEN RAISE_APPLICATION_ERROR(-20006,&#x27;A member may have at most 3 loans and reservations together&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 80 | <code>  SELECT COUNT(*) INTO v_count FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id WHERE i.student_id=p_student_id AND f.amount&gt;f.paid_amount;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 81 | <code>  IF v_count&gt;0 THEN RAISE_APPLICATION_ERROR(-20007,&#x27;Pay all outstanding fines before issuing another book&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 82 | <code>  INSERT INTO issue_book(student_id,book_id,copy_id,issue_date,due_date,status) VALUES(p_student_id,p_book_id,v_copy,SYSDATE,SYSDATE+15,&#x27;ISSUED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 83 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 84 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 85 | <code>CREATE OR REPLACE TRIGGER book_copy_stock_trigger</code> | Schema object define/replace করে: table, sequence, index, procedure, function অথবা trigger। |
| 86 | <code>AFTER INSERT OR UPDATE OF quantity ON book FOR EACH ROW</code> | নতুন business/audit/sample row insert করার statement। |
| 87 | <code>DECLARE v_max NUMBER; v_delta NUMBER; v_count NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 88 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 89 | <code>  v_delta:=:NEW.quantity-NVL(:OLD.quantity,0);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 90 | <code>  IF v_delta&gt;0 THEN</code> | PL/SQL condition/alternative branch। |
| 91 | <code>    SELECT NVL(MAX(copy_no),0) INTO v_max FROM book_copy WHERE book_id=:NEW.book_id;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 92 | <code>    FOR j IN 1..v_delta LOOP INSERT INTO book_copy(copy_id,book_id,copy_no) VALUES(copy_seq.NEXTVAL,:NEW.book_id,v_max+j); END LOOP;</code> | নতুন business/audit/sample row insert করার statement। |
| 93 | <code>  ELSIF v_delta&lt;0 THEN</code> | PL/SQL condition/alternative branch। |
| 94 | <code>    SELECT COUNT(*) INTO v_count FROM book_copy c WHERE c.book_id=:NEW.book_id AND c.status=&#x27;AVAILABLE&#x27;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 95 | <code>      AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status=&#x27;ACTIVE&#x27; AND r.expires_at&gt;SYSDATE);</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 96 | <code>    IF v_count &lt; -v_delta THEN RAISE_APPLICATION_ERROR(-20008,&#x27;Only unreserved available copies can be removed&#x27;); END IF;</code> | Database business validation অথবা setup verification fail হলে Oracle exception তোলে। |
| 97 | <code>    UPDATE book_copy SET status=&#x27;RETIRED&#x27; WHERE copy_id IN</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 98 | <code>      (SELECT copy_id FROM (SELECT c.copy_id FROM book_copy c WHERE c.book_id=:NEW.book_id AND c.status=&#x27;AVAILABLE&#x27;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 99 | <code>        AND NOT EXISTS (SELECT 1 FROM book_reservation r WHERE r.copy_id=c.copy_id AND r.status=&#x27;ACTIVE&#x27; AND r.expires_at&gt;SYSDATE)</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 100 | <code>        ORDER BY c.copy_no DESC) WHERE ROWNUM&lt;=-v_delta);</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 101 | <code>  END IF;</code> | PL/SQL condition/alternative branch। |
| 102 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 103 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 104 | <code>-- Oracle performs expiry even while the web server is stopped. Reads and issue</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 105 | <code>-- guards also treat the exact three-day deadline as expired between job runs.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 106 | <code>DECLARE n NUMBER; v_job NUMBER;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 107 | <code>BEGIN</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 108 | <code>  SELECT COUNT(*) INTO n FROM user_jobs WHERE what=&#x27;expire_reservations_proc;&#x27;;</code> | Database values/metadata lookup; INTO থাকলে PL/SQL variable-এ ফল রাখে। |
| 109 | <code>  IF n=0 THEN DBMS_JOB.SUBMIT(v_job,&#x27;expire_reservations_proc;&#x27;,SYSDATE,&#x27;SYSDATE+1/1440&#x27;); END IF;</code> | PL/SQL condition/alternative branch। |
| 110 | <code>  COMMIT;</code> | Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ। |
| 111 | <code>END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 112 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
