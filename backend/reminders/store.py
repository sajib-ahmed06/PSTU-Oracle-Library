"""Oracle-backed atomic claims prevent duplicate sends across restarts/workers."""

from backend.database import quote, rows, run_sql


def loans(issue_id=None):
    restriction = f" AND i.issue_id={int(issue_id)}" if issue_id is not None else ""
    return rows(
        "SELECT i.issue_id||'|'||i.student_id||'|'||REPLACE(s.name,'|',' ')||'|'||s.phone||'|'||s.email||'|'||"
        "REPLACE(b.title,'|',' ')||'|'||NVL(TO_CHAR(c.copy_no),'~')||'|'||"
        "TO_CHAR(i.due_date,'YYYY-MM-DD')||'|'||i.status||'|'||NVL(f.amount-f.paid_amount,0) "
        "FROM issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id "
        "LEFT JOIN book_copy c ON c.copy_id=i.copy_id LEFT JOIN fine f ON f.issue_id=i.issue_id "
        "WHERE i.due_date IS NOT NULL AND (i.status='ISSUED' OR f.amount>f.paid_amount)"
        + restriction,
        [
            "issue_id",
            "student_id",
            "name",
            "phone",
            "email",
            "title",
            "copy_no",
            "due_date",
            "status",
            "balance",
        ],
        {"issue_id", "student_id", "copy_no", "balance"},
    )


def claim(message):
    key = quote(message["key"])
    result = run_sql(
        "SET SERVEROUTPUT ON\nDECLARE claimed NUMBER:=0; BEGIN\n"
        "BEGIN INSERT INTO reminder_delivery(event_key,issue_id,channel,status,attempts) "
        f"VALUES({key},{int(message['issue_id'])},{quote(message['channel'])},'SENDING',1); "
        "claimed:=1; EXCEPTION WHEN DUP_VAL_ON_INDEX THEN "
        "UPDATE reminder_delivery SET status='SENDING',attempts=attempts+1,updated_at=SYSDATE "
        f"WHERE event_key={key} AND status='FAILED' AND attempts<3 AND next_attempt<=SYSDATE; "
        "claimed:=SQL%ROWCOUNT; END; COMMIT; "
        "IF claimed=1 THEN DBMS_OUTPUT.PUT_LINE('CLAIMED'); END IF; END;\n/"
    )
    return "CLAIMED" in result.splitlines()


def finish(key, status, provider_id=None):
    if status not in {"ACCEPTED", "FAILED", "UNKNOWN", "CANCELLED"}:
        raise ValueError("Invalid delivery status")
    provider = quote(provider_id) if provider_id else "NULL"
    run_sql(
        f"UPDATE reminder_delivery SET status={quote(status)},provider_id={provider},"
        "updated_at=SYSDATE,next_attempt=SYSDATE+30/1440 "
        f"WHERE event_key={quote(key)} AND status='SENDING';\nCOMMIT;"
    )


def recover_abandoned():
    # Sending may have succeeded before a process/connection failure. Never replay it blindly.
    run_sql(
        "UPDATE reminder_delivery SET status='UNKNOWN',updated_at=SYSDATE "
        "WHERE status='SENDING' AND updated_at<SYSDATE-15/1440;\nCOMMIT;"
    )
