# backend/auth/member_access.py

Member-only self activation and verified password recovery.

Source: [মূল file](../../backend/auth/member_access.py)। Snapshot 2026-10-04; 106 lines; SHA-256 `2a4d8985fce4c19117a33321a775107d803cf84a7a0402a2bb0424a3fb9ab0ce`।

## Function / object / element inventory

### `register_member_access_routes` — L15–L106

`def register_member_access_routes(router, frontend, rows, form_data, required, quote):`

Test/setup helper: register member access routes; নিচের assertions/calls সেই behavior define করে।

### `recovery_page` — L17–L18

`def recovery_page():`

Test/setup helper: recovery page; নিচের assertions/calls সেই behavior define করে।

### `reset_password` — L21–L70

`async def reset_password(request: Request):`

Test/setup helper: reset password; নিচের assertions/calls সেই behavior define করে।

### `save` — L46–L64

`def save():`

Test/setup helper: save; নিচের assertions/calls সেই behavior define করে।

### `activation_page` — L73–L74

`def activation_page():`

Test/setup helper: activation page; নিচের assertions/calls সেই behavior define করে।

### `activate` — L77–L106

`async def activate(request: Request):`

Test/setup helper: activate; নিচের assertions/calls সেই behavior define করে।

### `save` — L88–L100

`def save():`

Test/setup helper: save; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
"""Public, member-only account activation and password recovery."""

import re
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool
from backend.audit import audit_actor
from backend.database import run_sql
from backend.validation import text_field, academic_identifier
from .passwords import hash_password
from .session import invalidate_user_sessions
from .validation import member_number, validate_password


def register_member_access_routes(router, frontend, rows, form_data, required, quote):
    @router.get("/forgot-password")
    def recovery_page():
        return FileResponse(frontend / "forgot-password.html")

    @router.post("/api/auth/reset-password")
    async def reset_password(request: Request):
        data = await form_data(request)
        required(
            data,
            "memberId",
            "rollNo",
            "registrationNo",
            "phone",
            "email",
            "password",
            "confirmPassword",
        )
        sid = member_number(data["memberId"])
        roll = academic_identifier(data["rollNo"], "ID/Roll number")
        registration = academic_identifier(data["registrationNo"], "Registration No.")
        phone = data["phone"].strip()
        if not re.fullmatch(r"[0-9]{11}", phone):
            raise HTTPException(400, "Enter the registered 11-digit phone number")
        email = text_field(data["email"], "email", 100).strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise HTTPException(400, "Enter your registered email address")
        validate_password(data["password"])
        if data["password"] != data["confirmPassword"]:
            raise HTTPException(400, "Passwords do not match")

        def save():
            token = audit_actor.set(f"PSTU-{sid:04d}")
            try:
                run_sql(
                    (
                        f"BEGIN "
                        f"reset_student_password_proc({sid},{quote(roll)},{quote(registration)},{quote(phone)},{quote(email)},{quote(hash_password(data['password']))});"
                        f" COMMIT; END;\n/"
                    )
                )
            finally:
                audit_actor.reset(token)
            accounts = rows(
                f"SELECT user_id FROM login_user WHERE student_id={sid} AND user_type='STUDENT'",
                ["user_id"],
                {"user_id"},
            )
            for account in accounts:
                invalidate_user_sessions(account["user_id"])

        await run_in_threadpool(save)
        return {
            "message": "Password changed. Sign in with your Member ID and new password",
            "member_id": f"PSTU-{sid:04d}",
        }

    @router.get("/activate-account")
    def activation_page():
        return FileResponse(frontend / "activate-account.html")

    @router.post("/api/auth/activate")
    async def activate(request: Request):
        data = await form_data(request)
        required(data, "memberId", "phone", "password", "confirmPassword")
        sid = member_number(data["memberId"])
        phone = data["phone"].strip()
        if not re.fullmatch(r"[0-9]{11}", phone):
            raise HTTPException(400, "Enter the registered 11-digit phone number")
        validate_password(data["password"])
        if data["password"] != data["confirmPassword"]:
            raise HTTPException(400, "Passwords do not match")

        def save():
            token = audit_actor.set(f"PSTU-{sid:04d}")
            try:
                run_sql(
                    f"BEGIN activate_student_proc({sid},{quote(phone)},{quote(hash_password(data['password']))}); COMMIT; END;\n/"
                )
            finally:
                audit_actor.reset(token)
            accounts = rows(
                f"SELECT user_id FROM login_user WHERE student_id={sid}", ["user_id"], {"user_id"}
            )
            for account in accounts:
                invalidate_user_sessions(account["user_id"])

        await run_in_threadpool(save)
        return {
            "message": "Account activated. Sign in with your Member ID and password",
            "member_id": f"PSTU-{sid:04d}",
        }
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Public, member-only account activation and password recovery.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from fastapi import HTTPException, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from fastapi.responses import FileResponse</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from backend.audit import audit_actor</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.database import run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend.validation import text_field, academic_identifier</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from .passwords import hash_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from .session import invalidate_user_sessions</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from .validation import member_number, validate_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 15 | <code>def register_member_access_routes(router, frontend, rows, form_data, required, quote):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 16 | <code>    @router.get(&quot;/forgot-password&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 17 | <code>    def recovery_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 18 | <code>        return FileResponse(frontend / &quot;forgot-password.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `recovery_page` অংশে |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>    @router.post(&quot;/api/auth/reset-password&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 21 | <code>    async def reset_password(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 22 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reset_password` অংশে |
| 23 | <code>        required(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 24 | <code>            data,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 25 | <code>            &quot;memberId&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 26 | <code>            &quot;rollNo&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 27 | <code>            &quot;registrationNo&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 28 | <code>            &quot;phone&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 29 | <code>            &quot;email&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 30 | <code>            &quot;password&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 31 | <code>            &quot;confirmPassword&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 32 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 33 | <code>        sid = member_number(data[&quot;memberId&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reset_password` অংশে |
| 34 | <code>        roll = academic_identifier(data[&quot;rollNo&quot;], &quot;ID/Roll number&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reset_password` অংশে |
| 35 | <code>        registration = academic_identifier(data[&quot;registrationNo&quot;], &quot;Registration No.&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reset_password` অংশে |
| 36 | <code>        phone = data[&quot;phone&quot;].strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reset_password` অংশে |
| 37 | <code>        if not re.fullmatch(r&quot;[0-9]{11}&quot;, phone):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reset_password` অংশে |
| 38 | <code>            raise HTTPException(400, &quot;Enter the registered 11-digit phone number&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `reset_password` অংশে |
| 39 | <code>        email = text_field(data[&quot;email&quot;], &quot;email&quot;, 100).strip().lower()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reset_password` অংশে |
| 40 | <code>        if not re.fullmatch(r&quot;[^\s@]+@[^\s@]+\.[^\s@]+&quot;, email):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reset_password` অংশে |
| 41 | <code>            raise HTTPException(400, &quot;Enter your registered email address&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `reset_password` অংশে |
| 42 | <code>        validate_password(data[&quot;password&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 43 | <code>        if data[&quot;password&quot;] != data[&quot;confirmPassword&quot;]:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reset_password` অংশে |
| 44 | <code>            raise HTTPException(400, &quot;Passwords do not match&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `reset_password` অংশে |
| 45 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 46 | <code>        def save():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 47 | <code>            token = audit_actor.set(f&quot;PSTU-{sid:04d}&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `save` অংশে |
| 48 | <code>            try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `save` অংশে |
| 49 | <code>                run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `save` অংশে |
| 50 | <code>                    (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 51 | <code>                        f&quot;BEGIN &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 52 | <code>                        f&quot;reset_student_password_proc({sid},{quote(roll)},{quote(registration)},{quote(phone)},{quote(email)},{quote(hash_password(data[&#x27;password&#x27;]))});&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 53 | <code>                        f&quot; COMMIT; END;\n/&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 54 | <code>                    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 55 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 56 | <code>            finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `save` অংশে |
| 57 | <code>                audit_actor.reset(token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 58 | <code>            accounts = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `save` অংশে |
| 59 | <code>                f&quot;SELECT user_id FROM login_user WHERE student_id={sid} AND user_type=&#x27;STUDENT&#x27;&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `save` অংশে |
| 60 | <code>                [&quot;user_id&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 61 | <code>                {&quot;user_id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 62 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 63 | <code>            for account in accounts:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `save` অংশে |
| 64 | <code>                invalidate_user_sessions(account[&quot;user_id&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>        await run_in_threadpool(save)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `reset_password` অংশে |
| 67 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reset_password` অংশে |
| 68 | <code>            &quot;message&quot;: &quot;Password changed. Sign in with your Member ID and new password&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 69 | <code>            &quot;member_id&quot;: f&quot;PSTU-{sid:04d}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 70 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reset_password` অংশে |
| 71 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 72 | <code>    @router.get(&quot;/activate-account&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 73 | <code>    def activation_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 74 | <code>        return FileResponse(frontend / &quot;activate-account.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `activation_page` অংশে |
| 75 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 76 | <code>    @router.post(&quot;/api/auth/activate&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 77 | <code>    async def activate(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 78 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `activate` অংশে |
| 79 | <code>        required(data, &quot;memberId&quot;, &quot;phone&quot;, &quot;password&quot;, &quot;confirmPassword&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `activate` অংশে |
| 80 | <code>        sid = member_number(data[&quot;memberId&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `activate` অংশে |
| 81 | <code>        phone = data[&quot;phone&quot;].strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `activate` অংশে |
| 82 | <code>        if not re.fullmatch(r&quot;[0-9]{11}&quot;, phone):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `activate` অংশে |
| 83 | <code>            raise HTTPException(400, &quot;Enter the registered 11-digit phone number&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `activate` অংশে |
| 84 | <code>        validate_password(data[&quot;password&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `activate` অংশে |
| 85 | <code>        if data[&quot;password&quot;] != data[&quot;confirmPassword&quot;]:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `activate` অংশে |
| 86 | <code>            raise HTTPException(400, &quot;Passwords do not match&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `activate` অংশে |
| 87 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 88 | <code>        def save():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 89 | <code>            token = audit_actor.set(f&quot;PSTU-{sid:04d}&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `save` অংশে |
| 90 | <code>            try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `save` অংশে |
| 91 | <code>                run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `save` অংশে |
| 92 | <code>                    f&quot;BEGIN activate_student_proc({sid},{quote(phone)},{quote(hash_password(data[&#x27;password&#x27;]))}); COMMIT; END;\n/&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 93 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 94 | <code>            finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `save` অংশে |
| 95 | <code>                audit_actor.reset(token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 96 | <code>            accounts = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `save` অংশে |
| 97 | <code>                f&quot;SELECT user_id FROM login_user WHERE student_id={sid}&quot;, [&quot;user_id&quot;], {&quot;user_id&quot;}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `save` অংশে |
| 98 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 99 | <code>            for account in accounts:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `save` অংশে |
| 100 | <code>                invalidate_user_sessions(account[&quot;user_id&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `save` অংশে |
| 101 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 102 | <code>        await run_in_threadpool(save)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `activate` অংশে |
| 103 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `activate` অংশে |
| 104 | <code>            &quot;message&quot;: &quot;Account activated. Sign in with your Member ID and password&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `activate` অংশে |
| 105 | <code>            &quot;member_id&quot;: f&quot;PSTU-{sid:04d}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `activate` অংশে |
| 106 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `activate` অংশে |
