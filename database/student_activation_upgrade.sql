-- First-time student activation; preserves existing accounts and passwords.
SET DEFINE OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
DECLARE n NUMBER;
BEGIN
  SELECT COUNT(*) INTO n FROM user_tab_columns WHERE table_name='LOGIN_USER' AND column_name='MEMBER_ACTIVATED_AT';
  IF n=0 THEN EXECUTE IMMEDIATE 'ALTER TABLE login_user ADD (member_activated_at DATE)'; END IF;
END;
/
CREATE OR REPLACE PROCEDURE activate_student_proc(p_student_id NUMBER,p_phone VARCHAR2,p_password_hash VARCHAR2) AS
  v_phone VARCHAR2(11); v_membership VARCHAR2(20); v_user NUMBER;
  v_activated DATE; v_status VARCHAR2(20); v_username VARCHAR2(100);
BEGIN
  BEGIN
    SELECT phone,membership_status INTO v_phone,v_membership FROM student WHERE student_id=p_student_id FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20040,'Member ID or registered phone number does not match'); END;
  IF p_phone IS NULL OR v_phone<>p_phone THEN RAISE_APPLICATION_ERROR(-20040,'Member ID or registered phone number does not match'); END IF;
  IF v_membership<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)<>'pbkdf2$' THEN RAISE_APPLICATION_ERROR(-20041,'Invalid password hash'); END IF;
  v_username:='PSTU-'||LPAD(TO_CHAR(p_student_id,'FM99999999999999999990'),GREATEST(4,LENGTH(TO_CHAR(p_student_id,'FM99999999999999999990'))),'0');
  BEGIN
    SELECT user_id,member_activated_at,account_status INTO v_user,v_activated,v_status FROM login_user WHERE student_id=p_student_id AND user_type='STUDENT' FOR UPDATE;
    IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20042,'This account is disabled. Contact the library desk'); END IF;
    IF v_activated IS NOT NULL THEN RAISE_APPLICATION_ERROR(-20043,'Account already activated. Sign in with your Member ID and password'); END IF;
    UPDATE login_user SET username=v_username,password=p_password_hash,member_activated_at=SYSDATE WHERE user_id=v_user;
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO login_user(username,password,user_type,account_status,student_id,member_activated_at)
      VALUES(v_username,p_password_hash,'STUDENT','ACTIVE',p_student_id,SYSDATE);
  END;
END;
/
CREATE OR REPLACE PROCEDURE reset_student_password_proc(p_student_id NUMBER,p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2,p_password_hash VARCHAR2) AS
  v_count NUMBER; v_lock NUMBER; v_user NUMBER; v_status VARCHAR2(20);
BEGIN
  BEGIN
    SELECT student_id INTO v_lock FROM student WHERE student_id=p_student_id FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20044,'Member details do not match'); END;
  SELECT COUNT(*) INTO v_count FROM student WHERE student_id=p_student_id
    AND UPPER(TRIM(roll_no))=UPPER(TRIM(p_roll)) AND UPPER(TRIM(registration_no))=UPPER(TRIM(p_registration))
    AND phone=p_phone AND LOWER(TRIM(email))=LOWER(TRIM(p_email));
  IF v_count<>1 THEN RAISE_APPLICATION_ERROR(-20044,'Member details do not match'); END IF;
  SELECT membership_status INTO v_status FROM student WHERE student_id=p_student_id;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20005,'This membership is disabled'); END IF;
  BEGIN
    SELECT user_id,account_status INTO v_user,v_status FROM login_user WHERE student_id=p_student_id AND user_type='STUDENT' FOR UPDATE;
  EXCEPTION WHEN NO_DATA_FOUND THEN RAISE_APPLICATION_ERROR(-20045,'Activate your member account before resetting its password'); END;
  IF v_status<>'ACTIVE' THEN RAISE_APPLICATION_ERROR(-20042,'This account is disabled. Contact the library desk'); END IF;
  IF p_password_hash IS NULL OR SUBSTR(p_password_hash,1,7)<>'pbkdf2$' THEN RAISE_APPLICATION_ERROR(-20041,'Invalid password hash'); END IF;
  UPDATE login_user SET password=p_password_hash,member_activated_at=NVL(member_activated_at,SYSDATE) WHERE user_id=v_user;
END;
/
COMMIT;
