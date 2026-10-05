# backend/routes/members.py

Create and edit library members and their membership status.

Source: [মূল file](../../backend/routes/members.py)। Snapshot 2026-10-04; 176 lines; SHA-256 `a2c06f9f84df2d07743464e129ca810d508d87d5e2f159a8e03d043dc19fb94c`।

## Function / object / element inventory

### `get_students` — L18–L37

`def get_students():`

Member directory ফেরায়; generated student_id, contact/status এবং separate roll_no/registration_no fields থাকে।

### `add_student` — L41–L68

`async def add_student(request: Request):`

Shared member validation ও existing phone check করে সাত argument-সহ add_student_proc চালায়; identity trigger ও unique indexes final integrity enforce করে।

### `edit_student` — L72–L113

`async def edit_student(student_id: int, request: Request):`

পুরো member details ও membership_status validate করে; target row lock করে disabling-এর loan/fine restrictions checks; সব editable fields এক transaction-এ update করে।

### `update_student_identity` — L117–L135

`async def update_student_identity(student_id: int, request: Request):`

Compatibility endpoint: শুধু roll ও registration update করে; missing row-তে 404 mapping-এর জন্য NO_DATA_FOUND তোলে। Current UI full edit endpoint ব্যবহার করে।

### `toggle_student_membership` — L139–L176

`def toggle_student_membership(student_id: int):`

Member lock করে ACTIVE থেকে DISABLED যাওয়ার আগে active loans/unpaid fines দেখে; DISABLED হলে ACTIVE করে।

## সম্পূর্ণ original source

```python
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Members endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import APIRouter, HTTPException, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from backend.database import rows, quote, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.validation import (</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>    form_data,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 8 | <code>    required,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 9 | <code>    positive_number,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 10 | <code>    academic_identifier,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 11 | <code>    member_details,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 12 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>@router.get(&quot;/api/students&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 18 | <code>def get_students():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 19 | <code>    sql = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_students` অংশে |
| 20 | <code>        &quot;SELECT student_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(name,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(department,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 21 | <code>        &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;phone&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(email,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 22 | <code>        &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;membership_status&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(REPLACE(roll_no,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 23 | <code>        &quot;&#x27;),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(REPLACE(registration_no,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 24 | <code>        &quot;&#x27;),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(academic_session,&#x27;~&#x27;) FROM student ORDER BY student_id DESC&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 25 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 26 | <code>    keys = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_students` অংশে |
| 27 | <code>        &quot;student_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 28 | <code>        &quot;name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 29 | <code>        &quot;department&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 30 | <code>        &quot;phone&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 31 | <code>        &quot;email&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 32 | <code>        &quot;membership_status&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 33 | <code>        &quot;roll_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 34 | <code>        &quot;registration_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 35 | <code>        &quot;academic_session&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 36 | <code>    ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_students` অংশে |
| 37 | <code>    return rows(sql, keys, {&quot;student_id&quot;})</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_students` অংশে |
| 38 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 39 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 40 | <code>@router.post(&quot;/api/students&quot;, status_code=201)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 41 | <code>async def add_student(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 42 | <code>    p = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_student` অংশে |
| 43 | <code>    p = member_details(p)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_student` অংশে |
| 44 | <code>    phone = p[&quot;phone&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_student` অংশে |
| 45 | <code>    phone_count = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_student` অংশে |
| 46 | <code>        await run_in_threadpool(</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_student` অংশে |
| 47 | <code>            run_sql, f&quot;SELECT COUNT(*) FROM student WHERE phone = {quote(phone)};&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_student` অংশে |
| 48 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 49 | <code>    ).strip()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 50 | <code>    if phone_count != &quot;0&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `add_student` অংশে |
| 51 | <code>        raise HTTPException(409, &quot;Phone number is already registered&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `add_student` অংশে |
| 52 | <code>    sql = f&quot;&quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_student` অংশে |
| 53 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 54 | <code>  add_student_proc(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 55 | <code>    {quote(p[&#x27;name&#x27;])},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 56 | <code>    {quote(p[&#x27;department&#x27;])},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 57 | <code>    {quote(phone)},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 58 | <code>    {quote(p[&#x27;email&#x27;])},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 59 | <code>    DBMS_RANDOM.STRING(&#x27;X&#x27;,30),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 60 | <code>    {quote(p[&#x27;roll_no&#x27;])},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 61 | <code>    {quote(p[&#x27;registration_no&#x27;])},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 62 | <code>    {quote(p[&#x27;academic_session&#x27;])}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 63 | <code>  );</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 64 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 65 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 66 | <code>/&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_student` অংশে |
| 67 | <code>    await run_in_threadpool(run_sql, sql)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_student` অংশে |
| 68 | <code>    return {&quot;message&quot;: &quot;Student added&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `add_student` অংশে |
| 69 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 70 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 71 | <code>@router.post(&quot;/api/students/{student_id}/edit&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 72 | <code>async def edit_student(student_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 73 | <code>    student_id = positive_number(student_id, &quot;student_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 74 | <code>    data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `edit_student` অংশে |
| 75 | <code>    details = member_details(data)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 76 | <code>    required(data, &quot;membership_status&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 77 | <code>    status = data[&quot;membership_status&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 78 | <code>    if status not in {&quot;ACTIVE&quot;, &quot;DISABLED&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `edit_student` অংশে |
| 79 | <code>        raise HTTPException(400, &quot;Invalid membership status&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `edit_student` অংশে |
| 80 | <code>    # Lock the same member row as issue_book_proc so disabling cannot race borrowing.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 81 | <code>    sql = f&quot;&quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 82 | <code>DECLARE</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 83 | <code>  current_status student.membership_status%TYPE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 84 | <code>  active_loans NUMBER;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 85 | <code>  unpaid_fines NUMBER;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 86 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 87 | <code>  SELECT membership_status INTO current_status FROM student</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 88 | <code>  WHERE student_id = {student_id} FOR UPDATE;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 89 | <code>  IF current_status = &#x27;ACTIVE&#x27; AND {quote(status)} = &#x27;DISABLED&#x27; THEN</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 90 | <code>    SELECT COUNT(*) INTO active_loans FROM issue_book</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 91 | <code>    WHERE student_id = {student_id} AND status = &#x27;ISSUED&#x27;;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 92 | <code>    SELECT COUNT(*) INTO unpaid_fines FROM fine f</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 93 | <code>    JOIN issue_book i ON i.issue_id = f.issue_id</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 94 | <code>    WHERE i.student_id = {student_id} AND f.payment_status = &#x27;UNPAID&#x27;;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 95 | <code>    IF active_loans &gt; 0 THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 96 | <code>      RAISE_APPLICATION_ERROR(-20003, &#x27;Return all issued books before disabling membership&#x27;);</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 97 | <code>    END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 98 | <code>    IF unpaid_fines &gt; 0 THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 99 | <code>      RAISE_APPLICATION_ERROR(-20004, &#x27;Pay all fines before disabling membership&#x27;);</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 100 | <code>    END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 101 | <code>  END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 102 | <code>  UPDATE student SET</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 103 | <code>    name = {quote(details[&#x27;name&#x27;])}, department = {quote(details[&#x27;department&#x27;])},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 104 | <code>    phone = {quote(details[&#x27;phone&#x27;])}, email = {quote(details[&#x27;email&#x27;])},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 105 | <code>    academic_session = {quote(details[&#x27;academic_session&#x27;])},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 106 | <code>    roll_no = {quote(details[&#x27;roll_no&#x27;])}, registration_no = {quote(details[&#x27;registration_no&#x27;])},</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 107 | <code>    membership_status = {quote(status)}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 108 | <code>  WHERE student_id = {student_id};</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `edit_student` অংশে |
| 109 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 110 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 111 | <code>/&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `edit_student` অংশে |
| 112 | <code>    await run_in_threadpool(run_sql, sql)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `edit_student` অংশে |
| 113 | <code>    return {&quot;message&quot;: &quot;Member details updated&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `edit_student` অংশে |
| 114 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 115 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 116 | <code>@router.post(&quot;/api/students/{student_id}/identity&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 117 | <code>async def update_student_identity(student_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 118 | <code>    student_id = positive_number(student_id, &quot;student_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `update_student_identity` অংশে |
| 119 | <code>    data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `update_student_identity` অংশে |
| 120 | <code>    required(data, &quot;roll_no&quot;, &quot;registration_no&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 121 | <code>    roll_no = academic_identifier(data[&quot;roll_no&quot;], &quot;ID/Roll number&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `update_student_identity` অংশে |
| 122 | <code>    registration_no = academic_identifier(data[&quot;registration_no&quot;], &quot;Registration number&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `update_student_identity` অংশে |
| 123 | <code>    await run_in_threadpool(</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `update_student_identity` অংশে |
| 124 | <code>        run_sql,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 125 | <code>        f&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 126 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 127 | <code>  UPDATE student</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 128 | <code>  SET roll_no = {quote(roll_no)}, registration_no = {quote(registration_no)}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `update_student_identity` অংশে |
| 129 | <code>  WHERE student_id = {student_id};</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `update_student_identity` অংশে |
| 130 | <code>  IF SQL%ROWCOUNT = 0 THEN RAISE NO_DATA_FOUND; END IF;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `update_student_identity` অংশে |
| 131 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 132 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 133 | <code>/&quot;&quot;&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 134 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `update_student_identity` অংশে |
| 135 | <code>    return {&quot;message&quot;: &quot;Member identifiers updated&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `update_student_identity` অংশে |
| 136 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 137 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 138 | <code>@router.post(&quot;/api/students/{student_id}/toggle&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 139 | <code>def toggle_student_membership(student_id: int):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 140 | <code>    student_id = positive_number(student_id, &quot;student_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 141 | <code>    sql = f&quot;&quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 142 | <code>DECLARE</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 143 | <code>  v_status student.membership_status%TYPE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 144 | <code>  v_active_loans NUMBER;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 145 | <code>  v_unpaid_fines NUMBER;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 146 | <code>BEGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 147 | <code>  SELECT membership_status INTO v_status</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 148 | <code>  FROM student</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 149 | <code>  WHERE student_id = {student_id}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 150 | <code>  FOR UPDATE;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 151 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 152 | <code>  IF v_status = &#x27;ACTIVE&#x27; THEN</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 153 | <code>    SELECT COUNT(*) INTO v_active_loans</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 154 | <code>    FROM issue_book</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 155 | <code>    WHERE student_id = {student_id} AND status = &#x27;ISSUED&#x27;;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 156 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 157 | <code>    SELECT COUNT(*) INTO v_unpaid_fines</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 158 | <code>    FROM fine f</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 159 | <code>    JOIN issue_book i ON i.issue_id = f.issue_id</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 160 | <code>    WHERE i.student_id = {student_id} AND f.payment_status = &#x27;UNPAID&#x27;;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 161 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 162 | <code>    IF v_active_loans &gt; 0 THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 163 | <code>      RAISE_APPLICATION_ERROR(-20003, &#x27;Return all issued books before disabling membership&#x27;);</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 164 | <code>    END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 165 | <code>    IF v_unpaid_fines &gt; 0 THEN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 166 | <code>      RAISE_APPLICATION_ERROR(-20004, &#x27;Pay all fines before disabling membership&#x27;);</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 167 | <code>    END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 168 | <code>    UPDATE student SET membership_status = &#x27;DISABLED&#x27; WHERE student_id = {student_id};</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 169 | <code>  ELSE</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 170 | <code>    UPDATE student SET membership_status = &#x27;ACTIVE&#x27; WHERE student_id = {student_id};</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_student_membership` অংশে |
| 171 | <code>  END IF;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 172 | <code>  COMMIT;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 173 | <code>END;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 174 | <code>/&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_student_membership` অংশে |
| 175 | <code>    run_sql(sql)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `toggle_student_membership` অংশে |
| 176 | <code>    return {&quot;message&quot;: &quot;Membership status updated&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `toggle_student_membership` অংশে |
