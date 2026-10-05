# backend/auth/session.py

In-memory session token সৃষ্টি/expiry/invalidation, admin permission, request origin check এবং protected resource access নিয়ন্ত্রণ করে।

Source: [মূল file](../../backend/auth/session.py)। Snapshot 2026-10-04; 115 lines; SHA-256 `28428a73e181ed547080d07aacdfba6c0782404e51deec6870af614c21d07a67`।

## Function / object / element inventory

### `current_session` — L14–L22

`def current_session(request):`

Cookie token দিয়ে SESSIONS dictionary lookup করে; expired session সরিয়ে None ফেরায়। Valid session হলে তার dictionary ফেরায়।

### `require_admin` — L25–L29

`def require_admin(request):`

Session না থাকলে অথবা role ADMIN না হলে HTTP 403; valid admin session ফেরত দেয়।

### `create_session` — L32–L45

`def create_session(user):`

Expired tokens cleanup করে cryptographically random token তৈরি করে; user_id, username, role ও আট ঘণ্টার expiry dictionary-তে রাখে।

### `remove_session` — L48–L50

`def remove_session(token):`

নির্দিষ্ট token dictionary থেকে সরিয়ে logout/invalidation করে।

### `invalidate_user_sessions` — L53–L56

`def invalidate_user_sessions(user_id):`

এক user_id-এর সব session token খুঁজে সরায়; disabled/deleted account অথবা credential change-এ ব্যবহৃত।

### `install_authentication` — L59–L115

`def install_authentication(app):`

HTTP middleware register করে যাতে route execution-এর আগেই authentication/origin checks হয়।

### `require_authentication` — L61–L115

`async def require_authentication(request, call_next):`

Public paths নির্ধারণ করে; write request-এর supplied Origin-এর scheme/host যাচাই করে; request actor context বসায়; private API-তে 401, page-এ login redirect দেয়; nonstatic response-এ no-store।

## সম্পূর্ণ original source

```python
import secrets
import time
from urllib.parse import urlsplit

from fastapi import HTTPException
from backend.audit import audit_actor
from fastapi.responses import JSONResponse, RedirectResponse

SESSION_COOKIE = "library_session"
SESSION_SECONDS = 8 * 60 * 60
SESSIONS = {}


def current_session(request):
    token = request.cookies.get(SESSION_COOKIE)
    session = SESSIONS.get(token)
    if not session:
        return None
    if session["expires"] <= time.time():
        SESSIONS.pop(token, None)
        return None
    return session


def require_admin(request):
    session = current_session(request)
    if not session or session["user_type"] != "ADMIN":
        raise HTTPException(403, "Administrator access required")
    return session


def create_session(user):
    now = time.time()
    for expired_token, session in list(SESSIONS.items()):
        if session["expires"] <= now:
            SESSIONS.pop(expired_token, None)
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {
        "user_id": user["user_id"],
        "username": user["username"],
        "user_type": user["user_type"],
        "student_id": user.get("student_id"),
        "expires": time.time() + SESSION_SECONDS,
    }
    return token


def remove_session(token):
    if token:
        SESSIONS.pop(token, None)


def invalidate_user_sessions(user_id):
    expired_tokens = [token for token, session in SESSIONS.items() if session["user_id"] == user_id]
    for token in expired_tokens:
        SESSIONS.pop(token, None)


def install_authentication(app):
    @app.middleware("http")
    async def require_authentication(request, call_next):
        path = request.url.path
        public = (
            path == "/login"
            or path == "/activate-account"
            or path == "/forgot-password"
            or path == "/api/health"
            or path
            in {
                "/api/auth/login",
                "/api/auth/activate",
                "/api/auth/reset-password",
                "/api/auth/session",
                "/api/auth/logout",
            }
            or path.startswith("/static/")
        )
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            if origin and (urlsplit(origin).scheme, urlsplit(origin).netloc) != (
                request.url.scheme,
                request.url.netloc,
            ):
                return JSONResponse(
                    {"detail": "Cross-origin changes are not allowed"}, status_code=403
                )
        if public or current_session(request):
            session = current_session(request)
            if session and session["user_type"] == "STUDENT" and not public:
                allowed = path in {
                    "/student",
                    "/api/student/dashboard",
                    "/api/student/password",
                    "/api/reservations",
                }
                allowed = allowed or (
                    path.startswith("/api/reservations/") and path.endswith("/cancel")
                )
                if not allowed:
                    if path.startswith("/api/"):
                        return JSONResponse(
                            {"detail": "Management access required"}, status_code=403
                        )
                    return RedirectResponse("/student", status_code=303)
            token = audit_actor.set(session["username"] if session else "")
            try:
                response = await call_next(request)
            finally:
                audit_actor.reset(token)
            if not path.startswith("/static/"):
                response.headers["Cache-Control"] = "no-store"
            return response
        if path.startswith("/api/"):
            return JSONResponse({"detail": "Authentication required"}, status_code=401)
        return RedirectResponse("/login", status_code=303)
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import secrets</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import time</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>from urllib.parse import urlsplit</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.audit import audit_actor</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from fastapi.responses import JSONResponse, RedirectResponse</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>SESSION_COOKIE = &quot;library_session&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 10 | <code>SESSION_SECONDS = 8 * 60 * 60</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 11 | <code>SESSIONS = {}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>def current_session(request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 15 | <code>    token = request.cookies.get(SESSION_COOKIE)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `current_session` অংশে |
| 16 | <code>    session = SESSIONS.get(token)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `current_session` অংশে |
| 17 | <code>    if not session:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `current_session` অংশে |
| 18 | <code>        return None</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `current_session` অংশে |
| 19 | <code>    if session[&quot;expires&quot;] &lt;= time.time():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `current_session` অংশে |
| 20 | <code>        SESSIONS.pop(token, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `current_session` অংশে |
| 21 | <code>        return None</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `current_session` অংশে |
| 22 | <code>    return session</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `current_session` অংশে |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>def require_admin(request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 26 | <code>    session = current_session(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_admin` অংশে |
| 27 | <code>    if not session or session[&quot;user_type&quot;] != &quot;ADMIN&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_admin` অংশে |
| 28 | <code>        raise HTTPException(403, &quot;Administrator access required&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `require_admin` অংশে |
| 29 | <code>    return session</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_admin` অংশে |
| 30 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>def create_session(user):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 33 | <code>    now = time.time()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `create_session` অংশে |
| 34 | <code>    for expired_token, session in list(SESSIONS.items()):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `create_session` অংশে |
| 35 | <code>        if session[&quot;expires&quot;] &lt;= now:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `create_session` অংশে |
| 36 | <code>            SESSIONS.pop(expired_token, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 37 | <code>    token = secrets.token_urlsafe(32)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `create_session` অংশে |
| 38 | <code>    SESSIONS[token] = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `create_session` অংশে |
| 39 | <code>        &quot;user_id&quot;: user[&quot;user_id&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 40 | <code>        &quot;username&quot;: user[&quot;username&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 41 | <code>        &quot;user_type&quot;: user[&quot;user_type&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 42 | <code>        &quot;student_id&quot;: user.get(&quot;student_id&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 43 | <code>        &quot;expires&quot;: time.time() + SESSION_SECONDS,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 44 | <code>    }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `create_session` অংশে |
| 45 | <code>    return token</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `create_session` অংশে |
| 46 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 47 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 48 | <code>def remove_session(token):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 49 | <code>    if token:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `remove_session` অংশে |
| 50 | <code>        SESSIONS.pop(token, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `remove_session` অংশে |
| 51 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 52 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 53 | <code>def invalidate_user_sessions(user_id):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 54 | <code>    expired_tokens = [token for token, session in SESSIONS.items() if session[&quot;user_id&quot;] == user_id]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `invalidate_user_sessions` অংশে |
| 55 | <code>    for token in expired_tokens:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `invalidate_user_sessions` অংশে |
| 56 | <code>        SESSIONS.pop(token, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `invalidate_user_sessions` অংশে |
| 57 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 58 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 59 | <code>def install_authentication(app):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 60 | <code>    @app.middleware(&quot;http&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 61 | <code>    async def require_authentication(request, call_next):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 62 | <code>        path = request.url.path</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 63 | <code>        public = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 64 | <code>            path == &quot;/login&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 65 | <code>            or path == &quot;/activate-account&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 66 | <code>            or path == &quot;/forgot-password&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 67 | <code>            or path == &quot;/api/health&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 68 | <code>            or path</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 69 | <code>            in {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 70 | <code>                &quot;/api/auth/login&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 71 | <code>                &quot;/api/auth/activate&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 72 | <code>                &quot;/api/auth/reset-password&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 73 | <code>                &quot;/api/auth/session&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 74 | <code>                &quot;/api/auth/logout&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 75 | <code>            }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 76 | <code>            or path.startswith(&quot;/static/&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 77 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 78 | <code>        if request.method not in {&quot;GET&quot;, &quot;HEAD&quot;, &quot;OPTIONS&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 79 | <code>            origin = request.headers.get(&quot;origin&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 80 | <code>            if origin and (urlsplit(origin).scheme, urlsplit(origin).netloc) != (</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 81 | <code>                request.url.scheme,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 82 | <code>                request.url.netloc,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 83 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 84 | <code>                return JSONResponse(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_authentication` অংশে |
| 85 | <code>                    {&quot;detail&quot;: &quot;Cross-origin changes are not allowed&quot;}, status_code=403</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 86 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 87 | <code>        if public or current_session(request):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 88 | <code>            session = current_session(request)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 89 | <code>            if session and session[&quot;user_type&quot;] == &quot;STUDENT&quot; and not public:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 90 | <code>                allowed = path in {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 91 | <code>                    &quot;/student&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 92 | <code>                    &quot;/api/student/dashboard&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 93 | <code>                    &quot;/api/student/password&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 94 | <code>                    &quot;/api/reservations&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 95 | <code>                }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 96 | <code>                allowed = allowed or (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 97 | <code>                    path.startswith(&quot;/api/reservations/&quot;) and path.endswith(&quot;/cancel&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 98 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 99 | <code>                if not allowed:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 100 | <code>                    if path.startswith(&quot;/api/&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 101 | <code>                        return JSONResponse(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_authentication` অংশে |
| 102 | <code>                            {&quot;detail&quot;: &quot;Management access required&quot;}, status_code=403</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 103 | <code>                        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 104 | <code>                    return RedirectResponse(&quot;/student&quot;, status_code=303)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_authentication` অংশে |
| 105 | <code>            token = audit_actor.set(session[&quot;username&quot;] if session else &quot;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 106 | <code>            try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `require_authentication` অংশে |
| 107 | <code>                response = await call_next(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `require_authentication` অংশে |
| 108 | <code>            finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `require_authentication` অংশে |
| 109 | <code>                audit_actor.reset(token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `require_authentication` অংশে |
| 110 | <code>            if not path.startswith(&quot;/static/&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 111 | <code>                response.headers[&quot;Cache-Control&quot;] = &quot;no-store&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `require_authentication` অংশে |
| 112 | <code>            return response</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_authentication` অংশে |
| 113 | <code>        if path.startswith(&quot;/api/&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `require_authentication` অংশে |
| 114 | <code>            return JSONResponse({&quot;detail&quot;: &quot;Authentication required&quot;}, status_code=401)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_authentication` অংশে |
| 115 | <code>        return RedirectResponse(&quot;/login&quot;, status_code=303)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `require_authentication` অংশে |
