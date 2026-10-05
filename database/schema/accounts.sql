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

