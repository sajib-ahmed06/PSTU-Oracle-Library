# backend/routes/fines.py

Read fines, accept full-balance payments and list receipts.

Source: [মূল file](../../backend/routes/fines.py)। Snapshot 2026-10-04; 80 lines; SHA-256 `9fd94fad072138b19ff5ec28aaa89fe2752ec967e75a79148ff5c51488ab3bb1`।

## Function / object / element inventory

### `get_collection_summary` — L14–L26

`def get_collection_summary():`

Test/setup helper: get collection summary; নিচের assertions/calls সেই behavior define করে।

### `get_fines` — L30–L51

`def get_fines():`

Fine, issue, student ও book join করে amount ও payment status দেখায়।

### `pay_fine` — L55–L66

`async def pay_fine(fine_id: int, request: Request):`

Target fine PAID update করে; affected row না থাকলে NO_DATA_FOUND; audit trigger-সহ commit করে। Already-paid row আবার update করলেও নতুন audit event হতে পারে।

### `get_fine_payments` — L70–L80

`def get_fine_payments(fine_id: int):`

Test/setup helper: get fine payments; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
"""Fines endpoints for the library application."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool
from backend.database import rows, quote, run_sql
from backend.validation import form_data, positive_number, text_field

router = APIRouter()


@router.get("/api/fines/collection-summary")
def get_collection_summary():
    today = datetime.now(timezone(timedelta(hours=6), "Asia/Dhaka")).date()
    day = f"TO_DATE('{today.isoformat()}','YYYY-MM-DD')"
    month = f"TO_DATE('{today.replace(day=1).isoformat()}','YYYY-MM-DD')"
    result = rows(
        "SELECT (SELECT NVL(SUM(paid_amount),0) FROM fine)||'|'||"
        f"(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at>={day} AND paid_at<{day}+1)||'|'||"
        f"(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at>={month} AND paid_at<ADD_MONTHS({month},1)) "
        "FROM dual",
        ["total", "today", "month"],
        {"total", "today", "month"},
    )[0]
    return {**result, "date": today.isoformat(), "month_start": today.replace(day=1).isoformat()}


@router.get("/api/fines")
def get_fines():
    sql = (
        "SELECT f.fine_id||'|'||i.issue_id||'|'||i.student_id||'|'||REPLACE(s.name,'|',' "
        "')||'|'||REPLACE(b.title,'|',' "
        "')||'|'||f.amount||'|'||f.payment_status||'|'||f.paid_amount||'|'||(f.amount-f.paid_amount)"
        " FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id JOIN student s ON "
        "s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id ORDER BY f.fine_id DESC"
    )
    keys = [
        "fine_id",
        "issue_id",
        "student_id",
        "student",
        "title",
        "amount",
        "payment_status",
        "paid_amount",
        "balance",
    ]
    return rows(
        sql, keys, {"fine_id", "issue_id", "student_id", "amount", "paid_amount", "balance"}
    )


@router.post("/api/fines/{fine_id}/pay")
async def pay_fine(fine_id: int, request: Request):
    fine_id = positive_number(fine_id, "fine_id")
    p = await form_data(request)
    if "amount" in p:
        raise HTTPException(
            400, "Custom payment amounts are not allowed; pay the full outstanding fine"
        )
    note = text_field(p["note"], "note", 300) if p.get("note", "").strip() else ""
    await run_in_threadpool(
        run_sql, f"BEGIN\n pay_fine_proc({fine_id}, NULL, {quote(note)});\n COMMIT;\nEND;\n/"
    )
    return {"message": "Fine paid in full"}


@router.get("/api/fines/{fine_id}/payments")
def get_fine_payments(fine_id: int):
    fine_id = positive_number(fine_id, "fine_id")
    return rows(
        (
            f"SELECT payment_id||'|'||amount||'|'||TO_CHAR(paid_at,'YYYY-MM-DD "
            f"HH24:MI:SS')||'|'||REPLACE(actor,'|',' ')||'|'||NVL(REPLACE(note,'|',' '),'~') FROM "
            f"fine_payment WHERE fine_id={fine_id} ORDER BY paid_at DESC,payment_id DESC"
        ),
        ["payment_id", "amount", "paid_at", "actor", "note"],
        {"payment_id", "amount"},
    )
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Fines endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from datetime import datetime, timedelta, timezone</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from fastapi import APIRouter, HTTPException, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from backend.database import rows, quote, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.validation import form_data, positive_number, text_field</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 11 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>@router.get(&quot;/api/fines/collection-summary&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 14 | <code>def get_collection_summary():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 15 | <code>    today = datetime.now(timezone(timedelta(hours=6), &quot;Asia/Dhaka&quot;)).date()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_collection_summary` অংশে |
| 16 | <code>    day = f&quot;TO_DATE(&#x27;{today.isoformat()}&#x27;,&#x27;YYYY-MM-DD&#x27;)&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_collection_summary` অংশে |
| 17 | <code>    month = f&quot;TO_DATE(&#x27;{today.replace(day=1).isoformat()}&#x27;,&#x27;YYYY-MM-DD&#x27;)&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_collection_summary` অংশে |
| 18 | <code>    result = rows(</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `get_collection_summary` অংশে |
| 19 | <code>        &quot;SELECT (SELECT NVL(SUM(paid_amount),0) FROM fine)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_collection_summary` অংশে |
| 20 | <code>        f&quot;(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at&gt;={day} AND paid_at&lt;{day}+1)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_collection_summary` অংশে |
| 21 | <code>        f&quot;(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at&gt;={month} AND paid_at&lt;ADD_MONTHS({month},1)) &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_collection_summary` অংশে |
| 22 | <code>        &quot;FROM dual&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_collection_summary` অংশে |
| 23 | <code>        [&quot;total&quot;, &quot;today&quot;, &quot;month&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_collection_summary` অংশে |
| 24 | <code>        {&quot;total&quot;, &quot;today&quot;, &quot;month&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_collection_summary` অংশে |
| 25 | <code>    )[0]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_collection_summary` অংশে |
| 26 | <code>    return {**result, &quot;date&quot;: today.isoformat(), &quot;month_start&quot;: today.replace(day=1).isoformat()}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_collection_summary` অংশে |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>@router.get(&quot;/api/fines&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 30 | <code>def get_fines():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 31 | <code>    sql = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_fines` অংশে |
| 32 | <code>        &quot;SELECT f.fine_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.issue_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.student_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(s.name,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 33 | <code>        &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(b.title,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 34 | <code>        &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;f.amount&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;f.payment_status&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;f.paid_amount&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;(f.amount-f.paid_amount)&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 35 | <code>        &quot; FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id JOIN student s ON &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_fines` অংশে |
| 36 | <code>        &quot;s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id ORDER BY f.fine_id DESC&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_fines` অংশে |
| 37 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 38 | <code>    keys = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_fines` অংশে |
| 39 | <code>        &quot;fine_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 40 | <code>        &quot;issue_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 41 | <code>        &quot;student_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 42 | <code>        &quot;student&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 43 | <code>        &quot;title&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 44 | <code>        &quot;amount&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 45 | <code>        &quot;payment_status&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 46 | <code>        &quot;paid_amount&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 47 | <code>        &quot;balance&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 48 | <code>    ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 49 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_fines` অংশে |
| 50 | <code>        sql, keys, {&quot;fine_id&quot;, &quot;issue_id&quot;, &quot;student_id&quot;, &quot;amount&quot;, &quot;paid_amount&quot;, &quot;balance&quot;}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 51 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fines` অংশে |
| 52 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 53 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 54 | <code>@router.post(&quot;/api/fines/{fine_id}/pay&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 55 | <code>async def pay_fine(fine_id: int, request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 56 | <code>    fine_id = positive_number(fine_id, &quot;fine_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `pay_fine` অংশে |
| 57 | <code>    p = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `pay_fine` অংশে |
| 58 | <code>    if &quot;amount&quot; in p:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `pay_fine` অংশে |
| 59 | <code>        raise HTTPException(</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `pay_fine` অংশে |
| 60 | <code>            400, &quot;Custom payment amounts are not allowed; pay the full outstanding fine&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `pay_fine` অংশে |
| 61 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `pay_fine` অংশে |
| 62 | <code>    note = text_field(p[&quot;note&quot;], &quot;note&quot;, 300) if p.get(&quot;note&quot;, &quot;&quot;).strip() else &quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `pay_fine` অংশে |
| 63 | <code>    await run_in_threadpool(</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `pay_fine` অংশে |
| 64 | <code>        run_sql, f&quot;BEGIN\n pay_fine_proc({fine_id}, NULL, {quote(note)});\n COMMIT;\nEND;\n/&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `pay_fine` অংশে |
| 65 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `pay_fine` অংশে |
| 66 | <code>    return {&quot;message&quot;: &quot;Fine paid in full&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `pay_fine` অংশে |
| 67 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 68 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 69 | <code>@router.get(&quot;/api/fines/{fine_id}/payments&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 70 | <code>def get_fine_payments(fine_id: int):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 71 | <code>    fine_id = positive_number(fine_id, &quot;fine_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_fine_payments` অংশে |
| 72 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_fine_payments` অংশে |
| 73 | <code>        (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
| 74 | <code>            f&quot;SELECT payment_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;amount&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;TO_CHAR(paid_at,&#x27;YYYY-MM-DD &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
| 75 | <code>            f&quot;HH24:MI:SS&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(actor,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(REPLACE(note,&#x27;&#124;&#x27;,&#x27; &#x27;),&#x27;~&#x27;) FROM &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
| 76 | <code>            f&quot;fine_payment WHERE fine_id={fine_id} ORDER BY paid_at DESC,payment_id DESC&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_fine_payments` অংশে |
| 77 | <code>        ),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
| 78 | <code>        [&quot;payment_id&quot;, &quot;amount&quot;, &quot;paid_at&quot;, &quot;actor&quot;, &quot;note&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
| 79 | <code>        {&quot;payment_id&quot;, &quot;amount&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
| 80 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_fine_payments` অংশে |
