# backend/reservations.py

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../backend/reservations.py)। Snapshot 2026-10-04; 188 lines; SHA-256 `146eb8a49866412f67ee0c8d8eaf5c8e95c296070f3eac049baeafdf4a29bd6f`।

## Function / object / element inventory

### `session_for` — L14–L25

`def session_for(request):`

Test/setup helper: session for; নিচের assertions/calls সেই behavior define করে।

### `management` — L28–L32

`def management(request):`

Test/setup helper: management; নিচের assertions/calls সেই behavior define করে।

### `reservation_rows` — L35–L61

`def reservation_rows(student_id=None):`

Test/setup helper: reservation rows; নিচের assertions/calls সেই behavior define করে।

### `register_reservations` — L64–L188

`def register_reservations(app, get_books, get_issues, get_fines):`

Test/setup helper: register reservations; নিচের assertions/calls সেই behavior define করে।

### `student_page` — L66–L67

`def student_page():`

Test/setup helper: student page; নিচের assertions/calls সেই behavior define করে।

### `reservations_page` — L70–L72

`def reservations_page(request: Request):`

Test/setup helper: reservations page; নিচের assertions/calls সেই behavior define করে।

### `student_dashboard` — L75–L107

`def student_dashboard(request: Request):`

Test/setup helper: student dashboard; নিচের assertions/calls সেই behavior define করে।

### `get_reservations` — L110–L114

`def get_reservations(request: Request):`

Test/setup helper: get reservations; নিচের assertions/calls সেই behavior define করে।

### `reserve` — L117–L130

`async def reserve(request: Request):`

Test/setup helper: reserve; নিচের assertions/calls সেই behavior define করে।

### `change_reservation` — L132–L157

`async def change_reservation(reservation_id, request, collect=False):`

Test/setup helper: change reservation; নিচের assertions/calls সেই behavior define করে।

### `cancel` — L160–L161

`async def cancel(reservation_id: int, request: Request):`

Test/setup helper: cancel; নিচের assertions/calls সেই behavior define করে।

### `collect` — L164–L165

`async def collect(reservation_id: int, request: Request):`

Test/setup helper: collect; নিচের assertions/calls সেই behavior define করে।

### `student_password` — L168–L188

`async def student_password(request: Request):`

Test/setup helper: student password; নিচের assertions/calls সেই behavior define করে।

### `save` — L176–L185

`def save():`

Test/setup helper: save; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Student-scoped reads and reservation operations for the library desk.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import HTTPException, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from fastapi.responses import FileResponse</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>from backend.auth.session import current_session, invalidate_user_sessions</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.auth.passwords import hash_password, verify_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend.auth.validation import validate_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from backend.database import ROOT, rows, run_sql, quote, collect_reads, read_many</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from backend.validation import form_data, required, positive_number</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>def session_for(request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 15 | <code>    session = current_session(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `session_for` অংশে |
| 16 | <code>    if not session:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `session_for` অংশে |
| 17 | <code>        raise HTTPException(401, &quot;Authentication required&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `session_for` অংশে |
| 18 | <code>    if session[&quot;user_type&quot;] == &quot;STUDENT&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `session_for` অংশে |
| 19 | <code>        sid = positive_number(session.get(&quot;student_id&quot;), &quot;student_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `session_for` অংশে |
| 20 | <code>        members = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `session_for` অংশে |
| 21 | <code>            f&quot;SELECT membership_status FROM student WHERE student_id={sid}&quot;, [&quot;membership_status&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `session_for` অংশে |
| 22 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `session_for` অংশে |
| 23 | <code>        if not members or members[0][&quot;membership_status&quot;] != &quot;ACTIVE&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `session_for` অংশে |
| 24 | <code>            raise HTTPException(403, &quot;This membership is disabled&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `session_for` অংশে |
| 25 | <code>    return session</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `session_for` অংশে |
| 26 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>def management(request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 29 | <code>    session = session_for(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `management` অংশে |
| 30 | <code>    if session[&quot;user_type&quot;] not in {&quot;ADMIN&quot;, &quot;LIBRARIAN&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `management` অংশে |
| 31 | <code>        raise HTTPException(403, &quot;Management access required&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `management` অংশে |
| 32 | <code>    return session</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `management` অংশে |
| 33 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 34 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 35 | <code>def reservation_rows(student_id=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 36 | <code>    restriction = f&quot; WHERE r.student_id={student_id}&quot; if student_id else &quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reservation_rows` অংশে |
| 37 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reservation_rows` অংশে |
| 38 | <code>        (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 39 | <code>            &quot;SELECT r.reservation_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;r.student_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(s.name,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 40 | <code>            &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;r.book_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(b.title,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 41 | <code>            &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;c.copy_no&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;TO_CHAR(r.reserved_at,&#x27;YYYY-MM-DD &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 42 | <code>            &quot;HH24:MI:SS&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;TO_CHAR(r.expires_at,&#x27;YYYY-MM-DD HH24:MI:SS&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;CASE WHEN &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 43 | <code>            &quot;r.status=&#x27;ACTIVE&#x27; AND r.expires_at&lt;=SYSDATE THEN &#x27;EXPIRED&#x27; ELSE r.status END FROM &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reservation_rows` অংশে |
| 44 | <code>            &quot;book_reservation r JOIN student s ON s.student_id=r.student_id JOIN book b ON &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reservation_rows` অংশে |
| 45 | <code>            &quot;b.book_id=r.book_id JOIN book_copy c ON c.copy_id=r.copy_id&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reservation_rows` অংশে |
| 46 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 47 | <code>        + restriction</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 48 | <code>        + &quot; ORDER BY r.reservation_id DESC&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 49 | <code>        [</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 50 | <code>            &quot;reservation_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 51 | <code>            &quot;student_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 52 | <code>            &quot;student&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 53 | <code>            &quot;book_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 54 | <code>            &quot;title&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 55 | <code>            &quot;copy_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 56 | <code>            &quot;reserved_at&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 57 | <code>            &quot;expires_at&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 58 | <code>            &quot;status&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 59 | <code>        ],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 60 | <code>        {&quot;reservation_id&quot;, &quot;student_id&quot;, &quot;book_id&quot;, &quot;copy_no&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 61 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservation_rows` অংশে |
| 62 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 63 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 64 | <code>def register_reservations(app, get_books, get_issues, get_fines):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 65 | <code>    @app.get(&quot;/student&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 66 | <code>    def student_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 67 | <code>        return FileResponse(ROOT / &quot;frontend&quot; / &quot;student.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `student_page` অংশে |
| 68 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 69 | <code>    @app.get(&quot;/reservations&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 70 | <code>    def reservations_page(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 71 | <code>        management(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reservations_page` অংশে |
| 72 | <code>        return FileResponse(ROOT / &quot;frontend&quot; / &quot;reservations.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reservations_page` অংশে |
| 73 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 74 | <code>    @app.get(&quot;/api/student/dashboard&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 75 | <code>    def student_dashboard(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 76 | <code>        session = session_for(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 77 | <code>        if session[&quot;user_type&quot;] != &quot;STUDENT&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `student_dashboard` অংশে |
| 78 | <code>            raise HTTPException(403, &quot;Student access required&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `student_dashboard` অংশে |
| 79 | <code>        sid = positive_number(session[&quot;student_id&quot;], &quot;student_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 80 | <code>        with collect_reads() as queries:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 81 | <code>            get_books()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 82 | <code>            rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `student_dashboard` অংশে |
| 83 | <code>                f&quot;SELECT student_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(name,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(roll_no,&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(registration_no,&#x27;~&#x27;) FROM student WHERE student_id={sid}&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 84 | <code>                [&quot;student_id&quot;, &quot;name&quot;, &quot;roll_no&quot;, &quot;registration_no&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 85 | <code>                {&quot;student_id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 86 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 87 | <code>            get_issues()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 88 | <code>            get_fines()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 89 | <code>            reservation_rows(sid)</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `student_dashboard` অংশে |
| 90 | <code>        # Scope loan and fine SQL before executing; personal records never leave</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 91 | <code>        # Oracle for another member&#x27;s student session.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 92 | <code>        for index in (2, 3):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `student_dashboard` অংশে |
| 93 | <code>            sql, keys, numbers = queries[index]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 94 | <code>            select, order = sql.rsplit(&quot; ORDER BY &quot;, 1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 95 | <code>            queries[index] = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 96 | <code>                select + f&quot; WHERE i.student_id={sid} ORDER BY &quot; + order,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 97 | <code>                keys,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 98 | <code>                numbers,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 99 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 100 | <code>        books, members, issues, fines, reservations = read_many(queries)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `student_dashboard` অংশে |
| 101 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `student_dashboard` অংশে |
| 102 | <code>            &quot;books&quot;: books,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 103 | <code>            &quot;member&quot;: members[0],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 104 | <code>            &quot;issues&quot;: issues,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 105 | <code>            &quot;fines&quot;: fines,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 106 | <code>            &quot;reservations&quot;: reservations,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 107 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_dashboard` অংশে |
| 108 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 109 | <code>    @app.get(&quot;/api/reservations&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 110 | <code>    def get_reservations(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 111 | <code>        session = session_for(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_reservations` অংশে |
| 112 | <code>        return reservation_rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_reservations` অংশে |
| 113 | <code>            session[&quot;student_id&quot;] if session[&quot;user_type&quot;] == &quot;STUDENT&quot; else None</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_reservations` অংশে |
| 114 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_reservations` অংশে |
| 115 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 116 | <code>    @app.post(&quot;/api/reservations&quot;, status_code=201)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 117 | <code>    async def reserve(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 118 | <code>        session = await run_in_threadpool(session_for, request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reserve` অংশে |
| 119 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reserve` অংশে |
| 120 | <code>        required(data, &quot;bookId&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reserve` অংশে |
| 121 | <code>        book_id = positive_number(data[&quot;bookId&quot;], &quot;bookId&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reserve` অংশে |
| 122 | <code>        sid = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reserve` অংশে |
| 123 | <code>            session[&quot;student_id&quot;]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reserve` অংশে |
| 124 | <code>            if session[&quot;user_type&quot;] == &quot;STUDENT&quot;</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reserve` অংশে |
| 125 | <code>            else positive_number(data.get(&quot;studentId&quot;), &quot;studentId&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reserve` অংশে |
| 126 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reserve` অংশে |
| 127 | <code>        await run_in_threadpool(</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reserve` অংশে |
| 128 | <code>            run_sql, f&quot;BEGIN reserve_book_proc({sid},{book_id}); COMMIT; END;\n/&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reserve` অংশে |
| 129 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reserve` অংশে |
| 130 | <code>        return {&quot;message&quot;: &quot;Copy reserved. Collect it within 3 days&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reserve` অংশে |
| 131 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 132 | <code>    async def change_reservation(reservation_id, request, collect=False):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 133 | <code>        session = await run_in_threadpool(session_for, request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `change_reservation` অংশে |
| 134 | <code>        if collect and session[&quot;user_type&quot;] not in {&quot;ADMIN&quot;, &quot;LIBRARIAN&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `change_reservation` অংশে |
| 135 | <code>            raise HTTPException(403, &quot;Only the library desk can issue a reserved copy&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `change_reservation` অংশে |
| 136 | <code>        rid = positive_number(reservation_id, &quot;reservation_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 137 | <code>        restriction = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 138 | <code>            f&quot; AND student_id={session[&#x27;student_id&#x27;]}&quot; if session[&quot;user_type&quot;] == &quot;STUDENT&quot; else &quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 139 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 140 | <code>        action = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 141 | <code>            &quot;issue_book_proc(v_student,v_book,v_copy);&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 142 | <code>            if collect</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `change_reservation` অংশে |
| 143 | <code>            else f&quot;UPDATE book_reservation SET status=&#x27;CANCELLED&#x27; WHERE reservation_id={rid};&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 144 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 145 | <code>        sql = f&quot;&quot;&quot;DECLARE v_student NUMBER; v_book NUMBER; v_copy NUMBER; v_lock NUMBER; v_status VARCHAR2(12); v_expires DATE;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 146 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 147 | <code>  SELECT student_id,book_id INTO v_student,v_book FROM book_reservation WHERE reservation_id={rid}{restriction};</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 148 | <code>  SELECT student_id INTO v_lock FROM student WHERE student_id=v_student FOR UPDATE;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 149 | <code>  SELECT book_id INTO v_lock FROM book WHERE book_id=v_book FOR UPDATE;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 150 | <code>  SELECT copy_id,status,expires_at INTO v_copy,v_status,v_expires FROM book_reservation WHERE reservation_id={rid}{restriction} FOR UPDATE;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 151 | <code>  IF v_status&lt;&gt;&#x27;ACTIVE&#x27; OR v_expires&lt;=SYSDATE THEN RAISE_APPLICATION_ERROR(-20032,&#x27;This reservation is no longer active&#x27;); END IF;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_reservation` অংশে |
| 152 | <code>  {action}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 153 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 154 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 155 | <code>/&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_reservation` অংশে |
| 156 | <code>        await run_in_threadpool(run_sql, sql)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `change_reservation` অংশে |
| 157 | <code>        return {&quot;message&quot;: &quot;Reserved copy issued&quot; if collect else &quot;Reservation cancelled&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `change_reservation` অংশে |
| 158 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 159 | <code>    @app.post(&quot;/api/reservations/{reservation_id}/cancel&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 160 | <code>    async def cancel(reservation_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 161 | <code>        return await change_reservation(reservation_id, request)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `cancel` অংশে |
| 162 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 163 | <code>    @app.post(&quot;/api/reservations/{reservation_id}/collect&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 164 | <code>    async def collect(reservation_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 165 | <code>        return await change_reservation(reservation_id, request, True)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `collect` অংশে |
| 166 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 167 | <code>    @app.post(&quot;/api/student/password&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 168 | <code>    async def student_password(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 169 | <code>        session = await run_in_threadpool(session_for, request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `student_password` অংশে |
| 170 | <code>        if session[&quot;user_type&quot;] != &quot;STUDENT&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `student_password` অংশে |
| 171 | <code>            raise HTTPException(403, &quot;Student access required&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `student_password` অংশে |
| 172 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `student_password` অংশে |
| 173 | <code>        required(data, &quot;currentPassword&quot;, &quot;newPassword&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_password` অংশে |
| 174 | <code>        validate_password(data[&quot;newPassword&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `student_password` অংশে |
| 175 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 176 | <code>        def save():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 177 | <code>            account = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `save` অংশে |
| 178 | <code>                f&quot;SELECT password FROM login_user WHERE user_id={session[&#x27;user_id&#x27;]}&quot;, [&quot;password&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `save` অংশে |
| 179 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 180 | <code>            if not account or not verify_password(data[&quot;currentPassword&quot;], account[0][&quot;password&quot;]):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `save` অংশে |
| 181 | <code>                raise HTTPException(401, &quot;Current password is incorrect&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `save` অংশে |
| 182 | <code>            run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `save` অংশে |
| 183 | <code>                f&quot;UPDATE login_user SET password={quote(hash_password(data[&#x27;newPassword&#x27;]))} WHERE user_id={session[&#x27;user_id&#x27;]};\nCOMMIT;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `save` অংশে |
| 184 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 185 | <code>            invalidate_user_sessions(session[&quot;user_id&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 186 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 187 | <code>        await run_in_threadpool(save)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `student_password` অংশে |
| 188 | <code>        return {&quot;message&quot;: &quot;Password changed. Sign in again&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `student_password` অংশে |
