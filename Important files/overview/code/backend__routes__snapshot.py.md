# backend/routes/snapshot.py

Collect the complete management dataset in one Oracle connection.

Source: [মূল file](../../backend/routes/snapshot.py)। Snapshot 2026-10-04; 47 lines; SHA-256 `ce1aa07e91b369f0fdf0e86a179754a05b229e7c454991e82e9c7866f371e0cd`।

## Function / object / element inventory

### `get_meta` — L15–L26

`def get_meta():`

Author/category IDs ও names দেয়; book form datalist-এর options হিসেবে ব্যবহৃত।

### `get_snapshot` — L30–L47

`def get_snapshot():`

Collect the existing books/member/loan/fine/metadata SELECT definitions and execute all seven in one Oracle connection; return one complete management dataset.

## সম্পূর্ণ original source

```python
"""Snapshot endpoints for the library application."""

from fastapi import APIRouter
from backend.database import rows, collect_reads, read_many
from backend.reservations import reservation_rows
from .books import get_books
from .members import get_students
from .circulation import get_issues
from .fines import get_fines

router = APIRouter()


@router.get("/api/meta")
def get_meta():
    authors = rows(
        "SELECT author_id||'|'||REPLACE(author_name,'|',' ') FROM author ORDER BY author_name",
        ["id", "name"],
        {"id"},
    )
    categories = rows(
        "SELECT category_id||'|'||REPLACE(category_name,'|',' ') FROM category ORDER BY category_name",
        ["id", "name"],
        {"id"},
    )
    return {"authors": authors, "categories": categories}


@router.get("/api/snapshot")
def get_snapshot():
    # Reuse the same query definitions as individual endpoints, with one login.
    with collect_reads() as queries:
        get_books()
        get_students()
        get_issues()
        get_fines()
        get_meta()
        reservation_rows()
    books, students, issues, fines, authors, categories, reservations = read_many(queries)
    return {
        "books": books,
        "students": students,
        "issues": issues,
        "fines": fines,
        "meta": {"authors": authors, "categories": categories},
        "reservations": reservations,
    }
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Snapshot endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import APIRouter</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from backend.database import rows, collect_reads, read_many</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from backend.reservations import reservation_rows</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from .books import get_books</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from .members import get_students</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from .circulation import get_issues</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from .fines import get_fines</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>@router.get(&quot;/api/meta&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 15 | <code>def get_meta():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 16 | <code>    authors = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `get_meta` অংশে |
| 17 | <code>        &quot;SELECT author_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(author_name,&#x27;&#124;&#x27;,&#x27; &#x27;) FROM author ORDER BY author_name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 18 | <code>        [&quot;id&quot;, &quot;name&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 19 | <code>        {&quot;id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 20 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 21 | <code>    categories = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `get_meta` অংশে |
| 22 | <code>        &quot;SELECT category_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(category_name,&#x27;&#124;&#x27;,&#x27; &#x27;) FROM category ORDER BY category_name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 23 | <code>        [&quot;id&quot;, &quot;name&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 24 | <code>        {&quot;id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 25 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_meta` অংশে |
| 26 | <code>    return {&quot;authors&quot;: authors, &quot;categories&quot;: categories}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_meta` অংশে |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>@router.get(&quot;/api/snapshot&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 30 | <code>def get_snapshot():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 31 | <code>    # Reuse the same query definitions as individual endpoints, with one login.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 32 | <code>    with collect_reads() as queries:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 33 | <code>        get_books()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 34 | <code>        get_students()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 35 | <code>        get_issues()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 36 | <code>        get_fines()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 37 | <code>        get_meta()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 38 | <code>        reservation_rows()</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `get_snapshot` অংশে |
| 39 | <code>    books, students, issues, fines, authors, categories, reservations = read_many(queries)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_snapshot` অংশে |
| 40 | <code>    return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_snapshot` অংশে |
| 41 | <code>        &quot;books&quot;: books,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 42 | <code>        &quot;students&quot;: students,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 43 | <code>        &quot;issues&quot;: issues,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 44 | <code>        &quot;fines&quot;: fines,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 45 | <code>        &quot;meta&quot;: {&quot;authors&quot;: authors, &quot;categories&quot;: categories},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 46 | <code>        &quot;reservations&quot;: reservations,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
| 47 | <code>    }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_snapshot` অংশে |
