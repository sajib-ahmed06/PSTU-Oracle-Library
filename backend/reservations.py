"""Student-scoped reads and reservation operations for the library desk."""

from fastapi import HTTPException, Request
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

from backend.auth.session import current_session, invalidate_user_sessions
from backend.auth.passwords import hash_password, verify_password
from backend.auth.validation import validate_password
from backend.database import ROOT, rows, run_sql, quote, collect_reads, read_many
from backend.validation import form_data, required, positive_number


def session_for(request):
    session = current_session(request)
    if not session:
        raise HTTPException(401, "Authentication required")
    if session["user_type"] == "STUDENT":
        sid = positive_number(session.get("student_id"), "student_id")
        members = rows(
            f"SELECT membership_status FROM student WHERE student_id={sid}", ["membership_status"]
        )
        if not members or members[0]["membership_status"] != "ACTIVE":
            raise HTTPException(403, "This membership is disabled")
    return session


def management(request):
    session = session_for(request)
    if session["user_type"] not in {"ADMIN", "LIBRARIAN"}:
        raise HTTPException(403, "Management access required")
    return session


def reservation_rows(student_id=None):
    restriction = f" WHERE r.student_id={student_id}" if student_id else ""
    return rows(
        (
            "SELECT r.reservation_id||'|'||r.student_id||'|'||REPLACE(s.name,'|',' "
            "')||'|'||r.book_id||'|'||REPLACE(b.title,'|',' "
            "')||'|'||c.copy_no||'|'||TO_CHAR(r.reserved_at,'YYYY-MM-DD "
            "HH24:MI:SS')||'|'||TO_CHAR(r.expires_at,'YYYY-MM-DD HH24:MI:SS')||'|'||CASE WHEN "
            "r.status='ACTIVE' AND r.expires_at<=SYSDATE THEN 'EXPIRED' ELSE r.status END FROM "
            "book_reservation r JOIN student s ON s.student_id=r.student_id JOIN book b ON "
            "b.book_id=r.book_id JOIN book_copy c ON c.copy_id=r.copy_id"
        )
        + restriction
        + " ORDER BY r.reservation_id DESC",
        [
            "reservation_id",
            "student_id",
            "student",
            "book_id",
            "title",
            "copy_no",
            "reserved_at",
            "expires_at",
            "status",
        ],
        {"reservation_id", "student_id", "book_id", "copy_no"},
    )


def register_reservations(app, get_books, get_issues, get_fines):
    @app.get("/student")
    def student_page():
        return FileResponse(ROOT / "frontend" / "student.html")

    @app.get("/reservations")
    def reservations_page(request: Request):
        management(request)
        return FileResponse(ROOT / "frontend" / "reservations.html")

    @app.get("/api/student/dashboard")
    def student_dashboard(request: Request):
        session = session_for(request)
        if session["user_type"] != "STUDENT":
            raise HTTPException(403, "Student access required")
        sid = positive_number(session["student_id"], "student_id")
        with collect_reads() as queries:
            get_books()
            rows(
                f"SELECT student_id||'|'||REPLACE(name,'|',' ')||'|'||NVL(roll_no,'~')||'|'||NVL(registration_no,'~') FROM student WHERE student_id={sid}",
                ["student_id", "name", "roll_no", "registration_no"],
                {"student_id"},
            )
            get_issues()
            get_fines()
            reservation_rows(sid)
        # Scope loan and fine SQL before executing; personal records never leave
        # Oracle for another member's student session.
        for index in (2, 3):
            sql, keys, numbers = queries[index]
            select, order = sql.rsplit(" ORDER BY ", 1)
            queries[index] = (
                select + f" WHERE i.student_id={sid} ORDER BY " + order,
                keys,
                numbers,
            )
        books, members, issues, fines, reservations = read_many(queries)
        return {
            "books": books,
            "member": members[0],
            "issues": issues,
            "fines": fines,
            "reservations": reservations,
        }

    @app.get("/api/reservations")
    def get_reservations(request: Request):
        session = session_for(request)
        return reservation_rows(
            session["student_id"] if session["user_type"] == "STUDENT" else None
        )

    @app.post("/api/reservations", status_code=201)
    async def reserve(request: Request):
        session = await run_in_threadpool(session_for, request)
        data = await form_data(request)
        required(data, "bookId")
        book_id = positive_number(data["bookId"], "bookId")
        sid = (
            session["student_id"]
            if session["user_type"] == "STUDENT"
            else positive_number(data.get("studentId"), "studentId")
        )
        await run_in_threadpool(
            run_sql, f"BEGIN reserve_book_proc({sid},{book_id}); COMMIT; END;\n/"
        )
        return {"message": "Copy reserved. Collect it within 3 days"}

    async def change_reservation(reservation_id, request, collect=False):
        session = await run_in_threadpool(session_for, request)
        if collect and session["user_type"] not in {"ADMIN", "LIBRARIAN"}:
            raise HTTPException(403, "Only the library desk can issue a reserved copy")
        rid = positive_number(reservation_id, "reservation_id")
        restriction = (
            f" AND student_id={session['student_id']}" if session["user_type"] == "STUDENT" else ""
        )
        action = (
            "issue_book_proc(v_student,v_book,v_copy);"
            if collect
            else f"UPDATE book_reservation SET status='CANCELLED' WHERE reservation_id={rid};"
        )
        sql = f"""DECLARE v_student NUMBER; v_book NUMBER; v_copy NUMBER; v_lock NUMBER; v_status VARCHAR2(12); v_expires DATE;
BEGIN
  SELECT student_id,book_id INTO v_student,v_book FROM book_reservation WHERE reservation_id={rid}{restriction};
  SELECT student_id INTO v_lock FROM student WHERE student_id=v_student FOR UPDATE;
  SELECT book_id INTO v_lock FROM book WHERE book_id=v_book FOR UPDATE;
  SELECT copy_id,status,expires_at INTO v_copy,v_status,v_expires FROM book_reservation WHERE reservation_id={rid}{restriction} FOR UPDATE;
  IF v_status<>'ACTIVE' OR v_expires<=SYSDATE THEN RAISE_APPLICATION_ERROR(-20032,'This reservation is no longer active'); END IF;
  {action}
  COMMIT;
END;
/"""
        await run_in_threadpool(run_sql, sql)
        return {"message": "Reserved copy issued" if collect else "Reservation cancelled"}

    @app.post("/api/reservations/{reservation_id}/cancel")
    async def cancel(reservation_id: int, request: Request):
        return await change_reservation(reservation_id, request)

    @app.post("/api/reservations/{reservation_id}/collect")
    async def collect(reservation_id: int, request: Request):
        return await change_reservation(reservation_id, request, True)

    @app.post("/api/student/password")
    async def student_password(request: Request):
        session = await run_in_threadpool(session_for, request)
        if session["user_type"] != "STUDENT":
            raise HTTPException(403, "Student access required")
        data = await form_data(request)
        required(data, "currentPassword", "newPassword")
        validate_password(data["newPassword"])

        def save():
            account = rows(
                f"SELECT password FROM login_user WHERE user_id={session['user_id']}", ["password"]
            )
            if not account or not verify_password(data["currentPassword"], account[0]["password"]):
                raise HTTPException(401, "Current password is incorrect")
            run_sql(
                f"UPDATE login_user SET password={quote(hash_password(data['newPassword']))} WHERE user_id={session['user_id']};\nCOMMIT;"
            )
            invalidate_user_sessions(session["user_id"])

        await run_in_threadpool(save)
        return {"message": "Password changed. Sign in again"}
