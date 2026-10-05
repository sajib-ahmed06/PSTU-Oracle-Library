# backend/main.py

Create the app, register authentication and feature routers, and serve static files.

Source: [মূল file](../../backend/main.py)। Snapshot 2026-10-04; 73 lines; SHA-256 `3d62b2ca94bba8860f5aeff35d078131fbd4a13e8c2dd22089d1dd0075b3cd07`।

## Function / object / element inventory

## সম্পূর্ণ original source

```python
"""Application entry point: authentication, feature routers, and static assets."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.auth import install_authentication, register_auth_routes
from backend.database import ROOT, rows, execute_dml, quote
from backend.validation import form_data, required
from backend.reservations import register_reservations
from backend.reminders.worker import lifespan

from backend.routes.pages import (
    router as pages_router,
    home,
    books_page,
    students_page,
    circulation_page,
    fines_page,
    accounts_page,
    health,
    audit_page,
)

from backend.routes.books import (
    router as books_router,
    get_books,
    add_book,
    get_book_copies,
    reduce_book_stock,
)

from backend.routes.members import (
    router as members_router,
    get_students,
    add_student,
    edit_student,
    update_student_identity,
    toggle_student_membership,
)

from backend.routes.circulation import (
    router as circulation_router,
    get_issues,
    add_issue,
    return_book,
)

from backend.routes.fines import router as fines_router, get_fines, pay_fine, get_fine_payments

from backend.routes.snapshot import router as snapshot_router, get_meta, get_snapshot

from backend.routes.audit import router as audit_router, get_audit

FRONTEND = ROOT / "frontend"

app = FastAPI(
    title="PSTU Library API", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan
)
install_authentication(app)
register_auth_routes(app, FRONTEND, rows, execute_dml, quote, form_data, required)

for router in (
    pages_router,
    books_router,
    members_router,
    circulation_router,
    fines_router,
    snapshot_router,
    audit_router,
):
    app.include_router(router)

register_reservations(app, get_books, get_issues, get_fines)
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Application entry point: authentication, feature routers, and static assets.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import FastAPI</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from fastapi.staticfiles import StaticFiles</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from backend.auth import install_authentication, register_auth_routes</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.database import ROOT, rows, execute_dml, quote</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from backend.validation import form_data, required</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.reservations import register_reservations</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend.reminders.worker import lifespan</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>from backend.routes.pages import (</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>    router as pages_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 13 | <code>    home,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 14 | <code>    books_page,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 15 | <code>    students_page,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 16 | <code>    circulation_page,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 17 | <code>    fines_page,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 18 | <code>    accounts_page,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 19 | <code>    health,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 20 | <code>    audit_page,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 21 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 22 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 23 | <code>from backend.routes.books import (</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 24 | <code>    router as books_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 25 | <code>    get_books,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 26 | <code>    add_book,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 27 | <code>    get_book_copies,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 28 | <code>    reduce_book_stock,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 29 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 30 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 31 | <code>from backend.routes.members import (</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 32 | <code>    router as members_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 33 | <code>    get_students,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 34 | <code>    add_student,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 35 | <code>    edit_student,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 36 | <code>    update_student_identity,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 37 | <code>    toggle_student_membership,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 38 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 39 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 40 | <code>from backend.routes.circulation import (</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 41 | <code>    router as circulation_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 42 | <code>    get_issues,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 43 | <code>    add_issue,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 44 | <code>    return_book,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 45 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 46 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 47 | <code>from backend.routes.fines import router as fines_router, get_fines, pay_fine, get_fine_payments</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 48 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 49 | <code>from backend.routes.snapshot import router as snapshot_router, get_meta, get_snapshot</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 50 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 51 | <code>from backend.routes.audit import router as audit_router, get_audit</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 52 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 53 | <code>FRONTEND = ROOT / &quot;frontend&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 54 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 55 | <code>app = FastAPI(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 56 | <code>    title=&quot;PSTU Library API&quot;, docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 57 | <code>)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 58 | <code>install_authentication(app)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 59 | <code>register_auth_routes(app, FRONTEND, rows, execute_dml, quote, form_data, required)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 60 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 61 | <code>for router in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। |
| 62 | <code>    pages_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 63 | <code>    books_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 64 | <code>    members_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 65 | <code>    circulation_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 66 | <code>    fines_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 67 | <code>    snapshot_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 68 | <code>    audit_router,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 69 | <code>):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 70 | <code>    app.include_router(router)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 71 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 72 | <code>register_reservations(app, get_books, get_issues, get_fines)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 73 | <code>app.mount(&quot;/static&quot;, StaticFiles(directory=FRONTEND), name=&quot;static&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
