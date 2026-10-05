DECLARE
  invalid_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO invalid_count FROM user_objects WHERE status = 'INVALID';
  IF invalid_count > 0 THEN
    RAISE_APPLICATION_ERROR(-20099, 'Invalid database objects; inspect USER_ERRORS');
  END IF;
END;
/
PROMPT Library Management System setup completed.
