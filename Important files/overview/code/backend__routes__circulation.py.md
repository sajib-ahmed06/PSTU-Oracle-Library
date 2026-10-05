# backend/routes/circulation.py

Issue and return physical book copies.

Source: [মূল file](../../backend/routes/circulation.py)। Snapshot 2026-10-04; 69 lines; SHA-256 `20bd7fd01fc8dd2a02c8e17420d978d4eead2fe9d26e158adbbd21b45d0346a4`।

## Function / object / element inventory

### `get_issues` — L12–L40

`def get_issues():`

Loan, student ও book join করে issue/due/return dates এবং status JSON rows দেয়; newest issue আগে। The response also includes numeric overdue_days and current_fine, calculated from Oracle TRUNC(SYSDATE) using the same Tk 10/day rule as return_book_proc; returned loans return zero estimates.

### `add_issue` — L44–L62

`async def add_issue(request: Request):`

Student ও book IDs positive integer যাচাই করে issue_book_proc call এবং commit করে।

### `return_book` — L66–L69

`def return_book(issue_id: int):`

Positive issue ID নিয়ে return_book_proc call করে; returned inventory/fine changes এক transaction-এ commit।

## সম্পূর্ণ original source

```python
"""Circulation endpoints for the library application."""

from fastapi import APIRouter, Request
from starlette.concurrency import run_in_threadpool
from backend.database import rows, run_sql
from backend.validation import form_data, required, positive_number

router = APIRouter()


@router.get("/api/issues")
def get_issues():
    sql = (
        "SELECT i.issue_id||'|'||i.student_id||'|'||i.book_id||'|'||REPLACE(s.name,'|',' "
        "')||'|'||REPLACE(b.title,'|',' "
        "')||'|'||TO_CHAR(i.issue_date,'YYYY-MM-DD')||'|'||NVL(TO_CHAR(i.due_date,'YYYY-MM-DD'),'~')||'|'||NVL(TO_CHAR(i.return_date,'YYYY-MM-DD'),'~')||'|'||i.status||'|'||NVL(TO_CHAR(c.copy_no),'~')||'|'||CASE"
        " WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)"
        " ELSE 0 END||'|'||CASE WHEN i.status='ISSUED' THEN "
        "GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10 ELSE 0 END FROM "
        "issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON "
        "b.book_id=i.book_id LEFT JOIN book_copy c ON c.copy_id=i.copy_id ORDER BY i.issue_date"
        " DESC, i.issue_id DESC"
    )
    keys = [
        "issue_id",
        "student_id",
        "book_id",
        "student",
        "title",
        "issue_date",
        "due_date",
        "return_date",
        "status",
        "copy_no",
        "overdue_days",
        "current_fine",
    ]
    return rows(
        sql, keys, {"issue_id", "student_id", "book_id", "copy_no", "overdue_days", "current_fine"}
    )


@router.post("/api/issues", status_code=201)
async def add_issue(request: Request):
    p = await form_data(request)
    required(p, "studentId", "bookId")
    student_id = positive_number(p["studentId"], "studentId")
    book_id = positive_number(p["bookId"], "bookId")
    selections = [(book_id, p.get("copyId"))]
    for suffix in ("2", "3"):
        if p.get("bookId" + suffix):
            selections.append(
                (positive_number(p["bookId" + suffix], "bookId" + suffix), p.get("copyId" + suffix))
            )
    calls = []
    for selected_book, selected_copy in selections:
        copy_id = positive_number(selected_copy, "copyId") if selected_copy else "NULL"
        calls.append(f"  issue_book_proc({student_id}, {selected_book}, {copy_id});")
    # All selections succeed together, or SQL*Plus rolls the entire batch back.
    sql = "BEGIN\n" + "\n".join(calls) + "\n  COMMIT;\nEND;\n/"
    await run_in_threadpool(run_sql, sql)
    return {"message": f"{len(selections)} book copies issued"}


@router.post("/api/issues/{issue_id}/return")
def return_book(issue_id: int):
    issue_id = positive_number(issue_id, "issue_id")
    run_sql(f"BEGIN\n return_book_proc({issue_id});\n COMMIT;\nEND;\n/")
    return {"message": "Book returned"}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Circulation endpoints for the library application.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import APIRouter, Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from starlette.concurrency import run_in_threadpool</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from backend.database import rows, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from backend.validation import form_data, required, positive_number</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>router = APIRouter()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>@router.get(&quot;/api/issues&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 12 | <code>def get_issues():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 13 | <code>    sql = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_issues` অংশে |
| 14 | <code>        &quot;SELECT i.issue_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.student_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.book_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(s.name,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 15 | <code>        &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(b.title,&#x27;&#124;&#x27;,&#x27; &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 16 | <code>        &quot;&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;TO_CHAR(i.issue_date,&#x27;YYYY-MM-DD&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(TO_CHAR(i.due_date,&#x27;YYYY-MM-DD&#x27;),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(TO_CHAR(i.return_date,&#x27;YYYY-MM-DD&#x27;),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.status&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(TO_CHAR(c.copy_no),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;CASE&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 17 | <code>        &quot; WHEN i.status=&#x27;ISSUED&#x27; THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_issues` অংশে |
| 18 | <code>        &quot; ELSE 0 END&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;CASE WHEN i.status=&#x27;ISSUED&#x27; THEN &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_issues` অংশে |
| 19 | <code>        &quot;GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10 ELSE 0 END FROM &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 20 | <code>        &quot;issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_issues` অংশে |
| 21 | <code>        &quot;b.book_id=i.book_id LEFT JOIN book_copy c ON c.copy_id=i.copy_id ORDER BY i.issue_date&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_issues` অংশে |
| 22 | <code>        &quot; DESC, i.issue_id DESC&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 23 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 24 | <code>    keys = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `get_issues` অংশে |
| 25 | <code>        &quot;issue_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 26 | <code>        &quot;student_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 27 | <code>        &quot;book_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 28 | <code>        &quot;student&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 29 | <code>        &quot;title&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 30 | <code>        &quot;issue_date&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 31 | <code>        &quot;due_date&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 32 | <code>        &quot;return_date&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 33 | <code>        &quot;status&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 34 | <code>        &quot;copy_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 35 | <code>        &quot;overdue_days&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 36 | <code>        &quot;current_fine&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 37 | <code>    ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 38 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `get_issues` অংশে |
| 39 | <code>        sql, keys, {&quot;issue_id&quot;, &quot;student_id&quot;, &quot;book_id&quot;, &quot;copy_no&quot;, &quot;overdue_days&quot;, &quot;current_fine&quot;}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 40 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `get_issues` অংশে |
| 41 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 42 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 43 | <code>@router.post(&quot;/api/issues&quot;, status_code=201)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 44 | <code>async def add_issue(request: Request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 45 | <code>    p = await form_data(request)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_issue` অংশে |
| 46 | <code>    required(p, &quot;studentId&quot;, &quot;bookId&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_issue` অংশে |
| 47 | <code>    student_id = positive_number(p[&quot;studentId&quot;], &quot;studentId&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_issue` অংশে |
| 48 | <code>    book_id = positive_number(p[&quot;bookId&quot;], &quot;bookId&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_issue` অংশে |
| 49 | <code>    selections = [(book_id, p.get(&quot;copyId&quot;))]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_issue` অংশে |
| 50 | <code>    for suffix in (&quot;2&quot;, &quot;3&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `add_issue` অংশে |
| 51 | <code>        if p.get(&quot;bookId&quot; + suffix):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `add_issue` অংশে |
| 52 | <code>            selections.append(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_issue` অংশে |
| 53 | <code>                (positive_number(p[&quot;bookId&quot; + suffix], &quot;bookId&quot; + suffix), p.get(&quot;copyId&quot; + suffix))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_issue` অংশে |
| 54 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_issue` অংশে |
| 55 | <code>    calls = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_issue` অংশে |
| 56 | <code>    for selected_book, selected_copy in selections:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `add_issue` অংশে |
| 57 | <code>        copy_id = positive_number(selected_copy, &quot;copyId&quot;) if selected_copy else &quot;NULL&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_issue` অংশে |
| 58 | <code>        calls.append(f&quot;  issue_book_proc({student_id}, {selected_book}, {copy_id});&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `add_issue` অংশে |
| 59 | <code>    # All selections succeed together, or SQL*Plus rolls the entire batch back.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 60 | <code>    sql = &quot;BEGIN\n&quot; + &quot;\n&quot;.join(calls) + &quot;\n  COMMIT;\nEND;\n/&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `add_issue` অংশে |
| 61 | <code>    await run_in_threadpool(run_sql, sql)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `add_issue` অংশে |
| 62 | <code>    return {&quot;message&quot;: f&quot;{len(selections)} book copies issued&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `add_issue` অংশে |
| 63 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>@router.post(&quot;/api/issues/{issue_id}/return&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 66 | <code>def return_book(issue_id: int):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 67 | <code>    issue_id = positive_number(issue_id, &quot;issue_id&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `return_book` অংশে |
| 68 | <code>    run_sql(f&quot;BEGIN\n return_book_proc({issue_id});\n COMMIT;\nEND;\n/&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `return_book` অংশে |
| 69 | <code>    return {&quot;message&quot;: &quot;Book returned&quot;}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `return_book` অংশে |
