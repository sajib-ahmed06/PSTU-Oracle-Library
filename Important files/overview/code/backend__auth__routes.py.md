# backend/auth/routes.py

Login, logout, current session, librarian account management এবং administrator credentials change endpoints নিবন্ধন করে।

Source: [মূল file](../../backend/auth/routes.py)। Snapshot 2026-10-04; 222 lines; SHA-256 `bd3597e13d153ea86ffbb3831117fc6601483112343200efa51bda3283791b4e`।

## Function / object / element inventory

### `register_auth_routes` — L25–L200

`def register_auth_routes(app, frontend, rows, execute_dml, quote, form_data, required):`

Injected rows/execute_dml/quote/form helpers ব্যবহার করে APIRouter-এ auth/account routes define ও app-এ include করে।

### `login_page` — L30–L33

`def login_page(request: Request):`

Session থাকলে dashboard redirect; না থাকলে login.html FileResponse দেয়।

### `login` — L36–L101

`async def login(request: Request):`

Form parse ও length check করে authenticate helper worker thread-এ চালায়; পুরোনো cookie session সরিয়ে নতুন HttpOnly SameSite=strict cookie দেয়। HTTPS হলে Secure flag।

### `authenticate` — L43–L86

`def authenticate():`

Username দিয়ে Oracle user খোঁজে, password/role/status যাচাই করে এবং প্রয়োজন হলে legacy plaintext password hash-এ upgrade করে; সেই upgrade-এর audit actor user-এর username হয়।

### `auth_session` — L104–L111

`def auth_session(request: Request):`

Current session থেকে username ও user_type JSON দেয়; session না থাকলে 401।

### `logout` — L114–L118

`def logout(request: Request):`

Cookie token invalidates করে browser cookie delete response দেয়।

### `get_accounts` — L121–L129

`def get_accounts(request: Request):`

Admin permission যাচাই করে admin/librarian account metadata ফেরায়; passwords select করে না।

### `create_librarian` — L132–L145

`async def create_librarian(request: Request):`

Admin-only username/password validation, duplicate check ও hashed password insertion করে; role LIBRARIAN এবং status ACTIVE।

### `toggle_librarian` — L148–L157

`def toggle_librarian(user_id: int, request: Request):`

Admin-only target librarian status পরিবর্তন করে; disabled হলে তার active sessions সরিয়ে দেয়।

### `delete_librarian` — L160–L165

`def delete_librarian(user_id: int, request: Request):`

Admin-only librarian যাচাই করে delete করে এবং তার sessions invalidates করে। Admin account এই helper দিয়ে delete হয় না।

### `change_admin_credentials` — L168–L198

`async def change_admin_credentials(request: Request):`

Current password verify করে নতুন username/password validate ও update করে; অন্য sessions বাতিল করে current token-এর session ধরে রাখে।

### `username_exists` — L203–L210

`def username_exists(rows, quote, username, excluded_user_id=None):`

Case-insensitive username count query চালায়; current user-এর ID বাদ দেওয়া যায় যাতে নিজের username রাখা সম্ভব হয়।

### `librarian` — L213–L222

`def librarian(rows, user_id):`

Target user LIBRARIAN কি না query করে; absent হলে 404।

## সম্পূর্ণ original source

```python
"""Sign-in, staff account management, and authenticated credential changes."""

import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool
from backend.validation import text_field
from backend.audit import audit_actor
from .member_access import register_member_access_routes
from .passwords import hash_password, verify_password
from .validation import member_number, validate_password, validate_credentials

from .session import (
    SESSION_COOKIE,
    SESSION_SECONDS,
    create_session,
    current_session,
    invalidate_user_sessions,
    remove_session,
    require_admin,
)


def register_auth_routes(app, frontend, rows, execute_dml, quote, form_data, required):
    router = APIRouter()
    register_member_access_routes(router, frontend, rows, form_data, required, quote)

    @router.get("/login")
    def login_page(request: Request):
        if current_session(request):
            return RedirectResponse("/", status_code=303)
        return FileResponse(frontend / "login.html")

    @router.post("/api/auth/login")
    async def login(request: Request):
        data = await form_data(request)
        required(data, "username", "password")
        username = text_field(data["username"], "username", 100)
        if len(data["password"]) > 128:
            raise HTTPException(400, "Password must contain at most 128 characters")

        def authenticate():
            member_login = re.fullmatch(r"(?:PSTU-)?[0-9]{1,20}", username, re.I)
            condition = (
                f"student_id={member_number(username)} AND user_type='STUDENT'"
                if member_login
                else f"LOWER(username)=LOWER({quote(username)})"
            )
            users = rows(
                "SELECT user_id||'|'||username||'|'||user_type||'|'||account_status||'|'||password||'|'||NVL(TO_CHAR(student_id),'~') "
                "FROM login_user "
                f"WHERE {condition}",
                ["user_id", "username", "user_type", "account_status", "password", "student_id"],
                {"user_id", "student_id"},
            )
            if not users or not verify_password(data["password"], users[0]["password"]):
                raise HTTPException(401, "Incorrect username or password")

            user = users[0]
            if user["user_type"] not in {"ADMIN", "LIBRARIAN", "STUDENT"}:
                raise HTTPException(403, "This account cannot access the management dashboard")
            if user["account_status"] != "ACTIVE":
                raise HTTPException(403, "This account has been disabled")
            if user["user_type"] == "STUDENT":
                if not user.get("student_id"):
                    raise HTTPException(
                        403,
                        "Activate your account using your Member ID and registered phone number",
                    )
                members = rows(
                    f"SELECT membership_status FROM student WHERE student_id={user['student_id']}",
                    ["membership_status"],
                )
                if not members or members[0]["membership_status"] != "ACTIVE":
                    raise HTTPException(403, "This membership is disabled")

            if not user["password"].startswith("pbkdf2$"):
                actor_token = audit_actor.set(user["username"])
                try:
                    execute_dml(
                        f"UPDATE login_user SET password={quote(hash_password(data['password']))} WHERE user_id={user['user_id']}"
                    )
                finally:
                    audit_actor.reset(actor_token)
            return user

        # SQL*Plus and password hashing must not block other HTTP requests.
        user = await run_in_threadpool(authenticate)
        remove_session(request.cookies.get(SESSION_COOKIE))
        token = create_session(user)
        response = JSONResponse({"username": user["username"], "user_type": user["user_type"]})
        response.set_cookie(
            SESSION_COOKIE,
            token,
            max_age=SESSION_SECONDS,
            httponly=True,
            samesite="strict",
            secure=request.url.scheme == "https",
        )
        return response

    @router.get("/api/auth/session")
    def auth_session(request: Request):
        session = current_session(request)
        if not session:
            raise HTTPException(401, "Authentication required")
        return {
            "username": session["username"],
            "user_type": session["user_type"],
        }

    @router.post("/api/auth/logout")
    def logout(request: Request):
        remove_session(request.cookies.get(SESSION_COOKIE))
        response = JSONResponse({"message": "Logged out"})
        response.delete_cookie(SESSION_COOKIE)
        return response

    @router.get("/api/accounts")
    def get_accounts(request: Request):
        require_admin(request)
        return rows(
            "SELECT user_id||'|'||username||'|'||user_type||'|'||account_status "
            "FROM login_user WHERE user_type IN ('ADMIN','LIBRARIAN') "
            "ORDER BY DECODE(user_type,'ADMIN',1,2), username",
            ["user_id", "username", "user_type", "account_status"],
            {"user_id"},
        )

    @router.post("/api/accounts/librarians", status_code=201)
    async def create_librarian(request: Request):
        require_admin(request)
        data = await form_data(request)
        required(data, "username", "password")
        username = data["username"].strip()
        password = data["password"]
        validate_credentials(username, password)
        if username_exists(rows, quote, username):
            raise HTTPException(409, "Username already exists")
        execute_dml(
            "INSERT INTO login_user(username,password,user_type,account_status) "
            f"VALUES({quote(username)},{quote(hash_password(password))},'LIBRARIAN','ACTIVE')"
        )
        return {"message": "Librarian account created"}

    @router.post("/api/accounts/{user_id}/toggle")
    def toggle_librarian(user_id: int, request: Request):
        require_admin(request)
        account = librarian(rows, user_id)
        next_status = "DISABLED" if account["account_status"] == "ACTIVE" else "ACTIVE"
        execute_dml(
            "UPDATE login_user " f"SET account_status={quote(next_status)} WHERE user_id={user_id}"
        )
        if next_status == "DISABLED":
            invalidate_user_sessions(user_id)
        return {"message": f"Librarian account {next_status.lower()}"}

    @router.delete("/api/accounts/{user_id}")
    def delete_librarian(user_id: int, request: Request):
        require_admin(request)
        librarian(rows, user_id)
        execute_dml(f"DELETE FROM login_user WHERE user_id={user_id}")
        invalidate_user_sessions(user_id)
        return {"message": "Librarian account deleted"}

    @router.post("/api/auth/change-credentials")
    async def change_admin_credentials(request: Request):
        session = require_admin(request)
        data = await form_data(request)
        required(data, "currentPassword", "newUsername", "newPassword")
        username = data["newUsername"].strip()
        validate_credentials(username, data["newPassword"])

        accounts = rows(
            f"SELECT password FROM login_user WHERE user_id={session['user_id']}",
            ["password"],
        )
        if not accounts or not verify_password(data["currentPassword"], accounts[0]["password"]):
            raise HTTPException(401, "Current password is incorrect")
        if username_exists(rows, quote, username, session["user_id"]):
            raise HTTPException(409, "Username already exists")

        execute_dml(
            f"UPDATE login_user SET username={quote(username)}, "
            f"password={quote(hash_password(data['newPassword']))} "
            f"WHERE user_id={session['user_id']}"
        )
        token = request.cookies.get(SESSION_COOKIE)
        invalidate_user_sessions(session["user_id"])
        session["username"] = username
        from .session import SESSIONS

        SESSIONS[token] = session
        return {
            "message": "Administrator credentials updated",
            "username": username,
        }

    app.include_router(router)


def username_exists(rows, quote, username, excluded_user_id=None):
    exclusion = f" AND user_id<>{excluded_user_id}" if excluded_user_id else ""
    return rows(
        "SELECT COUNT(*) FROM login_user "
        f"WHERE LOWER(username)=LOWER({quote(username)}){exclusion}",
        ["count"],
        {"count"},
    )[0]["count"]


def librarian(rows, user_id):
    accounts = rows(
        "SELECT user_id||'|'||account_status FROM login_user "
        f"WHERE user_id={user_id} AND user_type='LIBRARIAN'",
        ["user_id", "account_status"],
        {"user_id"},
    )
    if not accounts:
        raise HTTPException(404, "Librarian account not found")
    return accounts[0]
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Sign-in, staff account management, and authenticated credential changes.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from fastapi import APIRouter, HTTPException, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from fastapi.responses import FileResponse, JSONResponse, RedirectResponse</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.validation import text_field</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend.audit import audit_actor</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from .member_access import register_member_access_routes</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from .passwords import hash_password, verify_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from .validation import member_number, validate_password, validate_credentials</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>from .session import (</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 15 | <code>    SESSION_COOKIE,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 16 | <code>    SESSION_SECONDS,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 17 | <code>    create_session,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 18 | <code>    current_session,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 19 | <code>    invalidate_user_sessions,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 20 | <code>    remove_session,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 21 | <code>    require_admin,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 22 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>def register_auth_routes(app, frontend, rows, execute_dml, quote, form_data, required):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 26 | <code>    router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `register_auth_routes` অংশে |
| 27 | <code>    register_member_access_routes(router, frontend, rows, form_data, required, quote)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `register_auth_routes` অংশে |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>    @router.get(&quot;/login&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 30 | <code>    def login_page(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 31 | <code>        if current_session(request):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `login_page` অংশে |
| 32 | <code>            return RedirectResponse(&quot;/&quot;, status_code=303)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `login_page` অংশে |
| 33 | <code>        return FileResponse(frontend / &quot;login.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `login_page` অংশে |
| 34 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 35 | <code>    @router.post(&quot;/api/auth/login&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 36 | <code>    async def login(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 37 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `login` অংশে |
| 38 | <code>        required(data, &quot;username&quot;, &quot;password&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `login` অংশে |
| 39 | <code>        username = text_field(data[&quot;username&quot;], &quot;username&quot;, 100)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 40 | <code>        if len(data[&quot;password&quot;]) &gt; 128:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `login` অংশে |
| 41 | <code>            raise HTTPException(400, &quot;Password must contain at most 128 characters&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `login` অংশে |
| 42 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 43 | <code>        def authenticate():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 44 | <code>            member_login = re.fullmatch(r&quot;(?:PSTU-)?[0-9]{1,20}&quot;, username, re.I)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 45 | <code>            condition = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 46 | <code>                f&quot;student_id={member_number(username)} AND user_type=&#x27;STUDENT&#x27;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 47 | <code>                if member_login</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 48 | <code>                else f&quot;LOWER(username)=LOWER({quote(username)})&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 49 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 50 | <code>            users = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `authenticate` অংশে |
| 51 | <code>                &quot;SELECT user_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;username&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;user_type&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;account_status&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;password&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(TO_CHAR(student_id),&#x27;~&#x27;) &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 52 | <code>                &quot;FROM login_user &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 53 | <code>                f&quot;WHERE {condition}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 54 | <code>                [&quot;user_id&quot;, &quot;username&quot;, &quot;user_type&quot;, &quot;account_status&quot;, &quot;password&quot;, &quot;student_id&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 55 | <code>                {&quot;user_id&quot;, &quot;student_id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 56 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 57 | <code>            if not users or not verify_password(data[&quot;password&quot;], users[0][&quot;password&quot;]):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 58 | <code>                raise HTTPException(401, &quot;Incorrect username or password&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `authenticate` অংশে |
| 59 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 60 | <code>            user = users[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 61 | <code>            if user[&quot;user_type&quot;] not in {&quot;ADMIN&quot;, &quot;LIBRARIAN&quot;, &quot;STUDENT&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 62 | <code>                raise HTTPException(403, &quot;This account cannot access the management dashboard&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `authenticate` অংশে |
| 63 | <code>            if user[&quot;account_status&quot;] != &quot;ACTIVE&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 64 | <code>                raise HTTPException(403, &quot;This account has been disabled&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `authenticate` অংশে |
| 65 | <code>            if user[&quot;user_type&quot;] == &quot;STUDENT&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 66 | <code>                if not user.get(&quot;student_id&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 67 | <code>                    raise HTTPException(</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `authenticate` অংশে |
| 68 | <code>                        403,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 69 | <code>                        &quot;Activate your account using your Member ID and registered phone number&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 70 | <code>                    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 71 | <code>                members = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `authenticate` অংশে |
| 72 | <code>                    f&quot;SELECT membership_status FROM student WHERE student_id={user[&#x27;student_id&#x27;]}&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 73 | <code>                    [&quot;membership_status&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 74 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 75 | <code>                if not members or members[0][&quot;membership_status&quot;] != &quot;ACTIVE&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 76 | <code>                    raise HTTPException(403, &quot;This membership is disabled&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `authenticate` অংশে |
| 77 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 78 | <code>            if not user[&quot;password&quot;].startswith(&quot;pbkdf2$&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `authenticate` অংশে |
| 79 | <code>                actor_token = audit_actor.set(user[&quot;username&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 80 | <code>                try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `authenticate` অংশে |
| 81 | <code>                    execute_dml(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `authenticate` অংশে |
| 82 | <code>                        f&quot;UPDATE login_user SET password={quote(hash_password(data[&#x27;password&#x27;]))} WHERE user_id={user[&#x27;user_id&#x27;]}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `authenticate` অংশে |
| 83 | <code>                    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 84 | <code>                finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `authenticate` অংশে |
| 85 | <code>                    audit_actor.reset(actor_token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `authenticate` অংশে |
| 86 | <code>            return user</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `authenticate` অংশে |
| 87 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 88 | <code>        # SQL*Plus and password hashing must not block other HTTP requests.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 89 | <code>        user = await run_in_threadpool(authenticate)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `login` অংশে |
| 90 | <code>        remove_session(request.cookies.get(SESSION_COOKIE))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `login` অংশে |
| 91 | <code>        token = create_session(user)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 92 | <code>        response = JSONResponse({&quot;username&quot;: user[&quot;username&quot;], &quot;user_type&quot;: user[&quot;user_type&quot;]})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 93 | <code>        response.set_cookie(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `login` অংশে |
| 94 | <code>            SESSION_COOKIE,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `login` অংশে |
| 95 | <code>            token,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `login` অংশে |
| 96 | <code>            max_age=SESSION_SECONDS,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 97 | <code>            httponly=True,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 98 | <code>            samesite=&quot;strict&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 99 | <code>            secure=request.url.scheme == &quot;https&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `login` অংশে |
| 100 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `login` অংশে |
| 101 | <code>        return response</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `login` অংশে |
| 102 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 103 | <code>    @router.get(&quot;/api/auth/session&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 104 | <code>    def auth_session(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 105 | <code>        session = current_session(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `auth_session` অংশে |
| 106 | <code>        if not session:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `auth_session` অংশে |
| 107 | <code>            raise HTTPException(401, &quot;Authentication required&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `auth_session` অংশে |
| 108 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `auth_session` অংশে |
| 109 | <code>            &quot;username&quot;: session[&quot;username&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `auth_session` অংশে |
| 110 | <code>            &quot;user_type&quot;: session[&quot;user_type&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `auth_session` অংশে |
| 111 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `auth_session` অংশে |
| 112 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 113 | <code>    @router.post(&quot;/api/auth/logout&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 114 | <code>    def logout(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 115 | <code>        remove_session(request.cookies.get(SESSION_COOKIE))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `logout` অংশে |
| 116 | <code>        response = JSONResponse({&quot;message&quot;: &quot;Logged out&quot;})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `logout` অংশে |
| 117 | <code>        response.delete_cookie(SESSION_COOKIE)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `logout` অংশে |
| 118 | <code>        return response</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `logout` অংশে |
| 119 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 120 | <code>    @router.get(&quot;/api/accounts&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 121 | <code>    def get_accounts(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 122 | <code>        require_admin(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 123 | <code>        return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_accounts` অংশে |
| 124 | <code>            &quot;SELECT user_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;username&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;user_type&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;account_status &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 125 | <code>            &quot;FROM login_user WHERE user_type IN (&#x27;ADMIN&#x27;,&#x27;LIBRARIAN&#x27;) &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 126 | <code>            &quot;ORDER BY DECODE(user_type,&#x27;ADMIN&#x27;,1,2), username&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 127 | <code>            [&quot;user_id&quot;, &quot;username&quot;, &quot;user_type&quot;, &quot;account_status&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 128 | <code>            {&quot;user_id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 129 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_accounts` অংশে |
| 130 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 131 | <code>    @router.post(&quot;/api/accounts/librarians&quot;, status_code=201)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 132 | <code>    async def create_librarian(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 133 | <code>        require_admin(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_librarian` অংশে |
| 134 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `create_librarian` অংশে |
| 135 | <code>        required(data, &quot;username&quot;, &quot;password&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_librarian` অংশে |
| 136 | <code>        username = data[&quot;username&quot;].strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `create_librarian` অংশে |
| 137 | <code>        password = data[&quot;password&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `create_librarian` অংশে |
| 138 | <code>        validate_credentials(username, password)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_librarian` অংশে |
| 139 | <code>        if username_exists(rows, quote, username):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `create_librarian` অংশে |
| 140 | <code>            raise HTTPException(409, &quot;Username already exists&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `create_librarian` অংশে |
| 141 | <code>        execute_dml(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `create_librarian` অংশে |
| 142 | <code>            &quot;INSERT INTO login_user(username,password,user_type,account_status) &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_librarian` অংশে |
| 143 | <code>            f&quot;VALUES({quote(username)},{quote(hash_password(password))},&#x27;LIBRARIAN&#x27;,&#x27;ACTIVE&#x27;)&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_librarian` অংশে |
| 144 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_librarian` অংশে |
| 145 | <code>        return {&quot;message&quot;: &quot;Librarian account created&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `create_librarian` অংশে |
| 146 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 147 | <code>    @router.post(&quot;/api/accounts/{user_id}/toggle&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 148 | <code>    def toggle_librarian(user_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 149 | <code>        require_admin(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_librarian` অংশে |
| 150 | <code>        account = librarian(rows, user_id)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_librarian` অংশে |
| 151 | <code>        next_status = &quot;DISABLED&quot; if account[&quot;account_status&quot;] == &quot;ACTIVE&quot; else &quot;ACTIVE&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_librarian` অংশে |
| 152 | <code>        execute_dml(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `toggle_librarian` অংশে |
| 153 | <code>            &quot;UPDATE login_user &quot; f&quot;SET account_status={quote(next_status)} WHERE user_id={user_id}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `toggle_librarian` অংশে |
| 154 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_librarian` অংশে |
| 155 | <code>        if next_status == &quot;DISABLED&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `toggle_librarian` অংশে |
| 156 | <code>            invalidate_user_sessions(user_id)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `toggle_librarian` অংশে |
| 157 | <code>        return {&quot;message&quot;: f&quot;Librarian account {next_status.lower()}&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `toggle_librarian` অংশে |
| 158 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 159 | <code>    @router.delete(&quot;/api/accounts/{user_id}&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 160 | <code>    def delete_librarian(user_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 161 | <code>        require_admin(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `delete_librarian` অংশে |
| 162 | <code>        librarian(rows, user_id)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `delete_librarian` অংশে |
| 163 | <code>        execute_dml(f&quot;DELETE FROM login_user WHERE user_id={user_id}&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `delete_librarian` অংশে |
| 164 | <code>        invalidate_user_sessions(user_id)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `delete_librarian` অংশে |
| 165 | <code>        return {&quot;message&quot;: &quot;Librarian account deleted&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `delete_librarian` অংশে |
| 166 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 167 | <code>    @router.post(&quot;/api/auth/change-credentials&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 168 | <code>    async def change_admin_credentials(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 169 | <code>        session = require_admin(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 170 | <code>        data = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `change_admin_credentials` অংশে |
| 171 | <code>        required(data, &quot;currentPassword&quot;, &quot;newUsername&quot;, &quot;newPassword&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 172 | <code>        username = data[&quot;newUsername&quot;].strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 173 | <code>        validate_credentials(username, data[&quot;newPassword&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 174 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 175 | <code>        accounts = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `change_admin_credentials` অংশে |
| 176 | <code>            f&quot;SELECT password FROM login_user WHERE user_id={session[&#x27;user_id&#x27;]}&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 177 | <code>            [&quot;password&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 178 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 179 | <code>        if not accounts or not verify_password(data[&quot;currentPassword&quot;], accounts[0][&quot;password&quot;]):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `change_admin_credentials` অংশে |
| 180 | <code>            raise HTTPException(401, &quot;Current password is incorrect&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `change_admin_credentials` অংশে |
| 181 | <code>        if username_exists(rows, quote, username, session[&quot;user_id&quot;]):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `change_admin_credentials` অংশে |
| 182 | <code>            raise HTTPException(409, &quot;Username already exists&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `change_admin_credentials` অংশে |
| 183 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 184 | <code>        execute_dml(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `change_admin_credentials` অংশে |
| 185 | <code>            f&quot;UPDATE login_user SET username={quote(username)}, &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 186 | <code>            f&quot;password={quote(hash_password(data[&#x27;newPassword&#x27;]))} &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 187 | <code>            f&quot;WHERE user_id={session[&#x27;user_id&#x27;]}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 188 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 189 | <code>        token = request.cookies.get(SESSION_COOKIE)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 190 | <code>        invalidate_user_sessions(session[&quot;user_id&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 191 | <code>        session[&quot;username&quot;] = username</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 192 | <code>        from .session import SESSIONS</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 193 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 194 | <code>        SESSIONS[token] = session</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `change_admin_credentials` অংশে |
| 195 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `change_admin_credentials` অংশে |
| 196 | <code>            &quot;message&quot;: &quot;Administrator credentials updated&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 197 | <code>            &quot;username&quot;: username,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 198 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `change_admin_credentials` অংশে |
| 199 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 200 | <code>    app.include_router(router)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `register_auth_routes` অংশে |
| 201 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 202 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 203 | <code>def username_exists(rows, quote, username, excluded_user_id=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 204 | <code>    exclusion = f&quot; AND user_id&lt;&gt;{excluded_user_id}&quot; if excluded_user_id else &quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `username_exists` অংশে |
| 205 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `username_exists` অংশে |
| 206 | <code>        &quot;SELECT COUNT(*) FROM login_user &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `username_exists` অংশে |
| 207 | <code>        f&quot;WHERE LOWER(username)=LOWER({quote(username)}){exclusion}&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `username_exists` অংশে |
| 208 | <code>        [&quot;count&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `username_exists` অংশে |
| 209 | <code>        {&quot;count&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `username_exists` অংশে |
| 210 | <code>    )[0][&quot;count&quot;]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `username_exists` অংশে |
| 211 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 212 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 213 | <code>def librarian(rows, user_id):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 214 | <code>    accounts = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `librarian` অংশে |
| 215 | <code>        &quot;SELECT user_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;account_status FROM login_user &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `librarian` অংশে |
| 216 | <code>        f&quot;WHERE user_id={user_id} AND user_type=&#x27;LIBRARIAN&#x27;&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `librarian` অংশে |
| 217 | <code>        [&quot;user_id&quot;, &quot;account_status&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `librarian` অংশে |
| 218 | <code>        {&quot;user_id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `librarian` অংশে |
| 219 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `librarian` অংশে |
| 220 | <code>    if not accounts:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `librarian` অংশে |
| 221 | <code>        raise HTTPException(404, &quot;Librarian account not found&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `librarian` অংশে |
| 222 | <code>    return accounts[0]</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `librarian` অংশে |
