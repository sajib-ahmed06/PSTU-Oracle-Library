# backend/routes/audit.py

Administrator audit search, filters and pagination.

Source: [মূল file](../../backend/routes/audit.py)। Snapshot 2026-10-04; 69 lines; SHA-256 `12cd74e9858f078c124b3fc0a2eba31944dfb0fff5729332d136646d85760ffe`।

## Function / object / element inventory

### `get_audit` — L14–L69

`def get_audit(request: Request, q: str = "", entity: str = "", action: str = "", page: int = 1):`

Admin-only search/entity/action filters ও 25-row Oracle ROWNUM pagination; RAWTOHEX snapshots decode করে JSON before/after ফেরায়। Stored UTC timestamps UI-তে Dhaka সময় হয়।

## সম্পূর্ণ original source

```python
"""Audit endpoints for the library application."""

import json

from fastapi import APIRouter, HTTPException, Request
from backend.auth import require_admin
from backend.database import rows, quote
from backend.validation import positive_number

router = APIRouter()


@router.get("/api/audit")
def get_audit(request: Request, q: str = "", entity: str = "", action: str = "", page: int = 1):
    require_admin(request)
    page = positive_number(page, "page")
    if len(q) > 100:
        raise HTTPException(400, "Search must contain at most 100 characters")
    entities = {
        "STUDENT",
        "BOOK",
        "AUTHOR",
        "CATEGORY",
        "ISSUE_BOOK",
        "RETURN_BOOK",
        "FINE",
        "LOGIN_USER",
        "ADMIN",
        "BOOK_RESERVATION",
    }
    actions = {"INSERT", "UPDATE", "DELETE", "SNAPSHOT"}
    conditions = ["1=1"]
    if entity:
        if entity not in entities:
            raise HTTPException(400, "Unknown audit entity")
        conditions.append(f"entity = {quote(entity)}")
    if action:
        if action not in actions:
            raise HTTPException(400, "Unknown audit action")
        conditions.append(f"action = {quote(action)}")
    if q.strip():
        # Literal search: identifiers containing % or _ are not wildcards.
        search = quote(q.strip().lower())
        conditions.append(
            f"INSTR(LOWER(actor || entity || TO_CHAR(record_id) || before_data || after_data), {search}) > 0"
        )
    where = " AND ".join(conditions)
    total = rows(f"SELECT COUNT(*) FROM audit_log WHERE {where}", ["total"], {"total"})[0]["total"]
    size = 25
    first, last = (page - 1) * size, page * size
    sql = f"""SELECT audit_id||'|'||TO_CHAR(occurred_at,'YYYY-MM-DD"T"HH24:MI:SS.FF3"Z"')||'|'||
      RAWTOHEX(actor)||'|'||action||'|'||entity||'|'||record_id||'|'||
      NVL(RAWTOHEX(before_data),'~')||'|'||NVL(RAWTOHEX(after_data),'~')
    FROM (
      SELECT ordered_logs.*, ROWNUM AS row_number FROM (
        SELECT * FROM audit_log WHERE {where} ORDER BY audit_id DESC
      ) ordered_logs WHERE ROWNUM <= {last}
    ) WHERE row_number > {first}"""
    items = rows(
        sql,
        ["audit_id", "occurred_at", "actor", "action", "entity", "record_id", "before", "after"],
        {"audit_id", "record_id"},
    )
    for item in items:
        # The installed Oracle 10g client uses WE8MSWIN1252.
        item["actor"] = bytes.fromhex(item["actor"]).decode("cp1252")
        for key in ("before", "after"):
            item[key] = json.loads(bytes.fromhex(item[key]).decode("cp1252")) if item[key] else None
    return {"items": items, "total": total, "page": page, "page_size": size}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Audit endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import json</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from fastapi import APIRouter, HTTPException, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.auth import require_admin</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from backend.database import rows, quote</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.validation import positive_number</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 11 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>@router.get(&quot;/api/audit&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 14 | <code>def get_audit(request: Request, q: str = &quot;&quot;, entity: str = &quot;&quot;, action: str = &quot;&quot;, page: int = 1):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 15 | <code>    require_admin(request)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 16 | <code>    page = positive_number(page, &quot;page&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 17 | <code>    if len(q) &gt; 100:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `get_audit` অংশে |
| 18 | <code>        raise HTTPException(400, &quot;Search must contain at most 100 characters&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `get_audit` অংশে |
| 19 | <code>    entities = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 20 | <code>        &quot;STUDENT&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 21 | <code>        &quot;BOOK&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 22 | <code>        &quot;AUTHOR&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 23 | <code>        &quot;CATEGORY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 24 | <code>        &quot;ISSUE_BOOK&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 25 | <code>        &quot;RETURN_BOOK&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 26 | <code>        &quot;FINE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 27 | <code>        &quot;LOGIN_USER&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 28 | <code>        &quot;ADMIN&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 29 | <code>        &quot;BOOK_RESERVATION&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 30 | <code>    }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 31 | <code>    actions = {&quot;INSERT&quot;, &quot;UPDATE&quot;, &quot;DELETE&quot;, &quot;SNAPSHOT&quot;}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 32 | <code>    conditions = [&quot;1=1&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 33 | <code>    if entity:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `get_audit` অংশে |
| 34 | <code>        if entity not in entities:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `get_audit` অংশে |
| 35 | <code>            raise HTTPException(400, &quot;Unknown audit entity&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `get_audit` অংশে |
| 36 | <code>        conditions.append(f&quot;entity = {quote(entity)}&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 37 | <code>    if action:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `get_audit` অংশে |
| 38 | <code>        if action not in actions:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `get_audit` অংশে |
| 39 | <code>            raise HTTPException(400, &quot;Unknown audit action&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `get_audit` অংশে |
| 40 | <code>        conditions.append(f&quot;action = {quote(action)}&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 41 | <code>    if q.strip():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `get_audit` অংশে |
| 42 | <code>        # Literal search: identifiers containing % or _ are not wildcards.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 43 | <code>        search = quote(q.strip().lower())</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 44 | <code>        conditions.append(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 45 | <code>            f&quot;INSTR(LOWER(actor &#124;&#124; entity &#124;&#124; TO_CHAR(record_id) &#124;&#124; before_data &#124;&#124; after_data), {search}) &gt; 0&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 46 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 47 | <code>    where = &quot; AND &quot;.join(conditions)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 48 | <code>    total = rows(f&quot;SELECT COUNT(*) FROM audit_log WHERE {where}&quot;, [&quot;total&quot;], {&quot;total&quot;})[0][&quot;total&quot;]</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `get_audit` অংশে |
| 49 | <code>    size = 25</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 50 | <code>    first, last = (page - 1) * size, page * size</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 51 | <code>    sql = f&quot;&quot;&quot;SELECT audit_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;TO_CHAR(occurred_at,&#x27;YYYY-MM-DD&quot;T&quot;HH24:MI:SS.FF3&quot;Z&quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 52 | <code>      RAWTOHEX(actor)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;action&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;entity&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;record_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 53 | <code>      NVL(RAWTOHEX(before_data),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(RAWTOHEX(after_data),&#x27;~&#x27;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 54 | <code>    FROM (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 55 | <code>      SELECT ordered_logs.*, ROWNUM AS row_number FROM (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 56 | <code>        SELECT * FROM audit_log WHERE {where} ORDER BY audit_id DESC</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 57 | <code>      ) ordered_logs WHERE ROWNUM &lt;= {last}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 58 | <code>    ) WHERE row_number &gt; {first}&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 59 | <code>    items = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `get_audit` অংশে |
| 60 | <code>        sql,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 61 | <code>        [&quot;audit_id&quot;, &quot;occurred_at&quot;, &quot;actor&quot;, &quot;action&quot;, &quot;entity&quot;, &quot;record_id&quot;, &quot;before&quot;, &quot;after&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 62 | <code>        {&quot;audit_id&quot;, &quot;record_id&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 63 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_audit` অংশে |
| 64 | <code>    for item in items:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `get_audit` অংশে |
| 65 | <code>        # The installed Oracle 10g client uses WE8MSWIN1252.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 66 | <code>        item[&quot;actor&quot;] = bytes.fromhex(item[&quot;actor&quot;]).decode(&quot;cp1252&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 67 | <code>        for key in (&quot;before&quot;, &quot;after&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `get_audit` অংশে |
| 68 | <code>            item[key] = json.loads(bytes.fromhex(item[key]).decode(&quot;cp1252&quot;)) if item[key] else None</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_audit` অংশে |
| 69 | <code>    return {&quot;items&quot;: items, &quot;total&quot;: total, &quot;page&quot;: page, &quot;page_size&quot;: size}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_audit` অংশে |
