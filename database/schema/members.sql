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

