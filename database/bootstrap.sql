-- Credentials are supplied as private bind variables by backend.setup_database.
SET SERVEROUTPUT ON;
WHENEVER SQLERROR EXIT SQL.SQLCODE;
DECLARE
  user_count NUMBER;
  account_name VARCHAR2(30) := DBMS_ASSERT.SIMPLE_SQL_NAME(:bootstrap_user);
  password_clause VARCHAR2(200) := ' IDENTIFIED BY "' || REPLACE(:bootstrap_password, '"', '""') || '"';
BEGIN
  SELECT COUNT(*) INTO user_count FROM dba_users WHERE username = UPPER(account_name);
  IF user_count = 0 THEN
    EXECUTE IMMEDIATE 'CREATE USER ' || account_name || password_clause;
  ELSE
    EXECUTE IMMEDIATE 'ALTER USER ' || account_name || password_clause || ' ACCOUNT UNLOCK';
  END IF;
  EXECUTE IMMEDIATE 'GRANT CONNECT, RESOURCE, CREATE VIEW TO ' || account_name;
END;
/
PROMPT Application schema is ready.
