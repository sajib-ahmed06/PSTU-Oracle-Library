# backend/routes/pages.py

Serve management pages and report Oracle connectivity.

Source: [মূল file](../../backend/routes/pages.py)। Snapshot 2026-10-04; 55 lines; SHA-256 `f8ba649b29193b209314092c34076a85d60a6ef5846bdd7d486dc2b1b771c955`।

## Function / object / element inventory

### `home` — L15–L16

`def home():`

Dashboard index.html response দেয়; authentication middleware আগেই access check করে।

### `books_page` — L20–L21

`def books_page():`

Books page HTML পরিবেশন করে।

### `students_page` — L25–L26

`def students_page():`

Members directory HTML পরিবেশন করে।

### `circulation_page` — L30–L31

`def circulation_page():`

Issue/Return page HTML পরিবেশন করে।

### `fines_page` — L35–L36

`def fines_page():`

Fine register HTML পরিবেশন করে।

### `accounts_page` — L40–L43

`def accounts_page(request: Request):`

ADMIN role ছাড়া dashboard redirect দেয়; admin হলে accounts.html দেয়।

### `health` — L47–L49

`def health():`

dual-এ SELECT 1 চালিয়ে actual Oracle connectivity যাচাই করে CONNECTED metadata দেয়। এটি public endpoint।

### `audit_page` — L53–L55

`def audit_page(request: Request):`

Admin permission ছাড়া access reject করে; admin-কে audit.html response দেয়।

## সম্পূর্ণ original source

```python
"""Pages endpoints for the library application."""

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse
from backend.auth import current_session, require_admin
from backend.database import ROOT, run_sql

FRONTEND = ROOT / "frontend"


router = APIRouter()


@router.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")


@router.get("/books")
def books_page():
    return FileResponse(FRONTEND / "books.html")


@router.get("/students")
def students_page():
    return FileResponse(FRONTEND / "students.html")


@router.get("/circulation")
def circulation_page():
    return FileResponse(FRONTEND / "circulation.html")


@router.get("/fines")
def fines_page():
    return FileResponse(FRONTEND / "fines.html")


@router.get("/accounts")
def accounts_page(request: Request):
    if current_session(request)["user_type"] != "ADMIN":
        return RedirectResponse("/", status_code=303)
    return FileResponse(FRONTEND / "accounts.html")


@router.get("/api/health")
def health():
    run_sql("SELECT 1 FROM dual;")
    return {"status": "CONNECTED", "database": "Oracle XE 10g"}


@router.get("/audit")
def audit_page(request: Request):
    require_admin(request)
    return FileResponse(FRONTEND / "audit.html")
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Pages endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import APIRouter, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from fastapi.responses import FileResponse, RedirectResponse</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from backend.auth import current_session, require_admin</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.database import ROOT, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>FRONTEND = ROOT / &quot;frontend&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>@router.get(&quot;/&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 15 | <code>def home():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 16 | <code>    return FileResponse(FRONTEND / &quot;index.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `home` অংশে |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 19 | <code>@router.get(&quot;/books&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 20 | <code>def books_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 21 | <code>    return FileResponse(FRONTEND / &quot;books.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `books_page` অংশে |
| 22 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>@router.get(&quot;/students&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 25 | <code>def students_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 26 | <code>    return FileResponse(FRONTEND / &quot;students.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `students_page` অংশে |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>@router.get(&quot;/circulation&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 30 | <code>def circulation_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 31 | <code>    return FileResponse(FRONTEND / &quot;circulation.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `circulation_page` অংশে |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 34 | <code>@router.get(&quot;/fines&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 35 | <code>def fines_page():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 36 | <code>    return FileResponse(FRONTEND / &quot;fines.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `fines_page` অংশে |
| 37 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 38 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 39 | <code>@router.get(&quot;/accounts&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 40 | <code>def accounts_page(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 41 | <code>    if current_session(request)[&quot;user_type&quot;] != &quot;ADMIN&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `accounts_page` অংশে |
| 42 | <code>        return RedirectResponse(&quot;/&quot;, status_code=303)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `accounts_page` অংশে |
| 43 | <code>    return FileResponse(FRONTEND / &quot;accounts.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `accounts_page` অংশে |
| 44 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 45 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 46 | <code>@router.get(&quot;/api/health&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 47 | <code>def health():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 48 | <code>    run_sql(&quot;SELECT 1 FROM dual;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `health` অংশে |
| 49 | <code>    return {&quot;status&quot;: &quot;CONNECTED&quot;, &quot;database&quot;: &quot;Oracle XE 10g&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `health` অংশে |
| 50 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 51 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 52 | <code>@router.get(&quot;/audit&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 53 | <code>def audit_page(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 54 | <code>    require_admin(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `audit_page` অংশে |
| 55 | <code>    return FileResponse(FRONTEND / &quot;audit.html&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `audit_page` অংশে |
