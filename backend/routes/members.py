"""Members endpoints for the library application."""

from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool
from backend.database import rows, quote, run_sql
from backend.validation import (
    form_data,
    required,
    positive_number,
    academic_identifier,
    member_details,
)

router = APIRouter()


@router.get("/api/students")
def get_students():
    sql = (
        "SELECT student_id||'|'||REPLACE(name,'|',' ')||'|'||REPLACE(department,'|',' "
        "')||'|'||phone||'|'||REPLACE(email,'|',' "
        "')||'|'||membership_status||'|'||NVL(REPLACE(roll_no,'|',' "
        "'),'~')||'|'||NVL(REPLACE(registration_no,'|',' "
        "'),'~')||'|'||NVL(academic_session,'~') FROM student ORDER BY student_id DESC"
    )
    keys = [
        "student_id",
        "name",
        "department",
        "phone",
        "email",
        "membership_status",
        "roll_no",
        "registration_no",
        "academic_session",
    ]
    return rows(sql, keys, {"student_id"})


@router.post("/api/students", status_code=201)
async def add_student(request: Request):
    p = await form_data(request)
    p = member_details(p)
    phone = p["phone"]
    phone_count = (
        await run_in_threadpool(
            run_sql, f"SELECT COUNT(*) FROM student WHERE phone = {quote(phone)};"
        )
    ).strip()
    if phone_count != "0":
        raise HTTPException(409, "Phone number is already registered")
    sql = f"""
BEGIN
  add_student_proc(
    {quote(p['name'])},
    {quote(p['department'])},
    {quote(phone)},
    {quote(p['email'])},
    DBMS_RANDOM.STRING('X',30),
    {quote(p['roll_no'])},
    {quote(p['registration_no'])},
    {quote(p['academic_session'])}
  );
  COMMIT;
END;
/"""
    await run_in_threadpool(run_sql, sql)
    return {"message": "Student added"}


@router.post("/api/students/{student_id}/edit")
async def edit_student(student_id: int, request: Request):
    student_id = positive_number(student_id, "student_id")
    data = await form_data(request)
    details = member_details(data)
    required(data, "membership_status")
    status = data["membership_status"]
    if status not in {"ACTIVE", "DISABLED"}:
        raise HTTPException(400, "Invalid membership status")
    # Lock the same member row as issue_book_proc so disabling cannot race borrowing.
    sql = f"""
DECLARE
  current_status student.membership_status%TYPE;
  active_loans NUMBER;
  unpaid_fines NUMBER;
BEGIN
  SELECT membership_status INTO current_status FROM student
  WHERE student_id = {student_id} FOR UPDATE;
  IF current_status = 'ACTIVE' AND {quote(status)} = 'DISABLED' THEN
    SELECT COUNT(*) INTO active_loans FROM issue_book
    WHERE student_id = {student_id} AND status = 'ISSUED';
    SELECT COUNT(*) INTO unpaid_fines FROM fine f
    JOIN issue_book i ON i.issue_id = f.issue_id
    WHERE i.student_id = {student_id} AND f.payment_status = 'UNPAID';
    IF active_loans > 0 THEN
      RAISE_APPLICATION_ERROR(-20003, 'Return all issued books before disabling membership');
    END IF;
    IF unpaid_fines > 0 THEN
      RAISE_APPLICATION_ERROR(-20004, 'Pay all fines before disabling membership');
    END IF;
  END IF;
  UPDATE student SET
    name = {quote(details['name'])}, department = {quote(details['department'])},
    phone = {quote(details['phone'])}, email = {quote(details['email'])},
    academic_session = {quote(details['academic_session'])},
    roll_no = {quote(details['roll_no'])}, registration_no = {quote(details['registration_no'])},
    membership_status = {quote(status)}
  WHERE student_id = {student_id};
  COMMIT;
END;
/"""
    await run_in_threadpool(run_sql, sql)
    return {"message": "Member details updated"}


@router.post("/api/students/{student_id}/identity")
async def update_student_identity(student_id: int, request: Request):
    student_id = positive_number(student_id, "student_id")
    data = await form_data(request)
    required(data, "roll_no", "registration_no")
    roll_no = academic_identifier(data["roll_no"], "ID/Roll number")
    registration_no = academic_identifier(data["registration_no"], "Registration number")
    await run_in_threadpool(
        run_sql,
        f"""
BEGIN
  UPDATE student
  SET roll_no = {quote(roll_no)}, registration_no = {quote(registration_no)}
  WHERE student_id = {student_id};
  IF SQL%ROWCOUNT = 0 THEN RAISE NO_DATA_FOUND; END IF;
  COMMIT;
END;
/""",
    )
    return {"message": "Member identifiers updated"}


@router.post("/api/students/{student_id}/toggle")
def toggle_student_membership(student_id: int):
    student_id = positive_number(student_id, "student_id")
    sql = f"""
DECLARE
  v_status student.membership_status%TYPE;
  v_active_loans NUMBER;
  v_unpaid_fines NUMBER;
BEGIN
  SELECT membership_status INTO v_status
  FROM student
  WHERE student_id = {student_id}
  FOR UPDATE;

  IF v_status = 'ACTIVE' THEN
    SELECT COUNT(*) INTO v_active_loans
    FROM issue_book
    WHERE student_id = {student_id} AND status = 'ISSUED';

    SELECT COUNT(*) INTO v_unpaid_fines
    FROM fine f
    JOIN issue_book i ON i.issue_id = f.issue_id
    WHERE i.student_id = {student_id} AND f.payment_status = 'UNPAID';

    IF v_active_loans > 0 THEN
      RAISE_APPLICATION_ERROR(-20003, 'Return all issued books before disabling membership');
    END IF;
    IF v_unpaid_fines > 0 THEN
      RAISE_APPLICATION_ERROR(-20004, 'Pay all fines before disabling membership');
    END IF;
    UPDATE student SET membership_status = 'DISABLED' WHERE student_id = {student_id};
  ELSE
    UPDATE student SET membership_status = 'ACTIVE' WHERE student_id = {student_id};
  END IF;
  COMMIT;
END;
/"""
    run_sql(sql)
    return {"message": "Membership status updated"}
