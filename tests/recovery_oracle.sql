SET SERVEROUTPUT ON
DECLARE v_student NUMBER; v_user NUMBER; v_staff NUMBER; v_count NUMBER;
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
  PROCEDURE mismatch(p_roll VARCHAR2,p_registration VARCHAR2,p_phone VARCHAR2,p_email VARCHAR2) IS
  BEGIN
    BEGIN reset_student_password_proc(v_student,p_roll,p_registration,p_phone,p_email,'pbkdf2$bad-attempt');
      RAISE_APPLICATION_ERROR(-20999,'Incorrect identity detail accepted');
    EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20044 THEN RAISE; END IF; END;
  END;
BEGIN
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Recovery QA','QA','09666666661','recovery-qa@invalid.test','unused','REC-QA1','REC-REG1','2025-2026') RETURNING student_id INTO v_student;
  INSERT INTO login_user(username,password,user_type) VALUES('recovery_qa_admin','staff-original','ADMIN') RETURNING user_id INTO v_staff;
  BEGIN reset_student_password_proc(v_student,'REC-QA1','REC-REG1','09666666661','recovery-qa@invalid.test','pbkdf2$new');
    RAISE_APPLICATION_ERROR(-20999,'Recovery created an account before activation');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20045 THEN RAISE; END IF; END;
  activate_student_proc(v_student,'09666666661','pbkdf2$original');
  SELECT user_id INTO v_user FROM login_user WHERE student_id=v_student;
  mismatch('wrong','REC-REG1','09666666661','recovery-qa@invalid.test');
  mismatch('REC-QA1','wrong','09666666661','recovery-qa@invalid.test');
  mismatch('REC-QA1','REC-REG1','09666666662','recovery-qa@invalid.test');
  mismatch('REC-QA1','REC-REG1','09666666661','wrong@invalid.test');
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password='pbkdf2$original';
  check_true(v_count=1,'Rejected recovery changed the password');
  reset_student_password_proc(v_student,' rec-qa1 ','rec-reg1','09666666661','RECOVERY-QA@INVALID.TEST','pbkdf2$new');
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password='pbkdf2$new' AND user_type='STUDENT';
  check_true(v_count=1,'Matching identity must reset the linked student password');
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_staff AND password='staff-original';
  check_true(v_count=1,'Recovery changed a staff password');
  UPDATE login_user SET account_status='DISABLED' WHERE user_id=v_user;
  BEGIN reset_student_password_proc(v_student,'REC-QA1','REC-REG1','09666666661','recovery-qa@invalid.test','pbkdf2$disabled');
    RAISE_APPLICATION_ERROR(-20999,'Recovery enabled a disabled account');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20042 THEN RAISE; END IF; END;
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: all identity fields, member-only recovery, account preservation, disabled guard');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
