SET SERVEROUTPUT ON
DECLARE v_student NUMBER; v_count NUMBER; v_user NUMBER; v_hash VARCHAR2(255):='pbkdf2$activation-rollback-test';
  PROCEDURE check_true(ok BOOLEAN,message VARCHAR2) IS
  BEGIN IF ok IS NULL OR NOT ok THEN RAISE_APPLICATION_ERROR(-20999,message); END IF; END;
BEGIN
  INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session)
    VALUES('Activation QA','QA','09777777771','activation-qa@invalid.test','unused','ACT-QA1','ACT-REG1','2025-2026') RETURNING student_id INTO v_student;
  BEGIN activate_student_proc(v_student,'09777777772',v_hash); RAISE_APPLICATION_ERROR(-20999,'Wrong phone accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20040 THEN RAISE; END IF; END;
  BEGIN activate_student_proc(v_student,NULL,v_hash); RAISE_APPLICATION_ERROR(-20999,'Missing phone accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20040 THEN RAISE; END IF; END;
  BEGIN activate_student_proc(-1,'09777777771',v_hash); RAISE_APPLICATION_ERROR(-20999,'Unknown member accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20040 THEN RAISE; END IF; END;
  UPDATE student SET membership_status='DISABLED' WHERE student_id=v_student;
  BEGIN activate_student_proc(v_student,'09777777771',v_hash); RAISE_APPLICATION_ERROR(-20999,'Disabled member accepted');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20005 THEN RAISE; END IF; END;
  UPDATE student SET membership_status='ACTIVE' WHERE student_id=v_student;
  activate_student_proc(v_student,'09777777771',v_hash);
  SELECT user_id INTO v_user FROM login_user WHERE student_id=v_student;
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND member_activated_at IS NOT NULL AND user_type='STUDENT' AND account_status='ACTIVE' AND password=v_hash;
  check_true(v_count=1,'Activation must create an active linked student account');
  BEGIN activate_student_proc(v_student,'09777777771','pbkdf2$replacement'); RAISE_APPLICATION_ERROR(-20999,'Repeat activation changed password');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20043 THEN RAISE; END IF; END;
  SELECT COUNT(*) INTO v_count FROM login_user WHERE user_id=v_user AND password=v_hash;
  check_true(v_count=1,'Original password must survive repeated activation');
  -- A pre-existing linked account is reused, preserving its ID.
  UPDATE login_user SET member_activated_at=NULL,password='old-password' WHERE user_id=v_user;
  activate_student_proc(v_student,'09777777771',v_hash);
  SELECT COUNT(*) INTO v_count FROM login_user WHERE student_id=v_student AND user_id=v_user AND password=v_hash;
  check_true(v_count=1,'Existing linked account must be reused');
  UPDATE login_user SET member_activated_at=NULL,account_status='DISABLED' WHERE user_id=v_user;
  BEGIN activate_student_proc(v_student,'09777777771',v_hash); RAISE_APPLICATION_ERROR(-20999,'Activation enabled a disabled account');
  EXCEPTION WHEN OTHERS THEN IF SQLCODE<>-20042 THEN RAISE; END IF; END;
  ROLLBACK;
  DBMS_OUTPUT.PUT_LINE('PASS: member/phone matching, one-time activation, disabled guards, existing account preservation');
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
