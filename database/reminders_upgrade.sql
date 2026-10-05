-- Delivery tracking only; existing loans, fines and member records are preserved.
DECLARE
  table_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO table_count FROM user_tables WHERE table_name='REMINDER_DELIVERY';
  IF table_count=0 THEN
    EXECUTE IMMEDIATE 'CREATE TABLE reminder_delivery (
      event_key VARCHAR2(120) PRIMARY KEY,
      issue_id NUMBER NOT NULL,
      channel VARCHAR2(10) NOT NULL,
      status VARCHAR2(12) DEFAULT ''PENDING'' NOT NULL,
      attempts NUMBER DEFAULT 0 NOT NULL,
      updated_at DATE DEFAULT SYSDATE NOT NULL,
      next_attempt DATE DEFAULT SYSDATE NOT NULL,
      provider_id VARCHAR2(100),
      CONSTRAINT reminder_channel_ck CHECK(channel IN (''SMS'',''EMAIL'')),
      CONSTRAINT reminder_status_ck CHECK(status IN (''PENDING'',''SENDING'',''ACCEPTED'',''FAILED'',''UNKNOWN'',''CANCELLED''))
    )';
  END IF;
END;
/
