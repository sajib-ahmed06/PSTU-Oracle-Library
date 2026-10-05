# backend/reminders/messages.py

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../backend/reminders/messages.py)। Snapshot 2026-10-04; 51 lines; SHA-256 `2a9afff1aad7bded85d580a42808d83e66b44f3b2a8264d1626ab99d4bd859cb`।

## Function / object / element inventory

### `reminder_for` — L9–L51

`def reminder_for(loan, today=None):`

Test/setup helper: reminder for; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
"""Reminder rules and message content, independent of providers and scheduling."""

from datetime import date, datetime, timedelta, timezone

DAILY_FINE = 10
DHAKA = timezone(timedelta(hours=6), "Asia/Dhaka")


def reminder_for(loan, today=None):
    today = today or datetime.now(DHAKA).date()
    due = date.fromisoformat(loan["due_date"])
    overdue = (today - due).days
    active = loan["status"] == "ISSUED"
    member = f"PSTU-{int(loan['student_id']):04d}"
    book = f"{loan['title']} (Copy #{loan['copy_no']})" if loan.get("copy_no") else loan["title"]
    prefix = f"PSTU Library: {loan['name']} ({member}), book: {book}. "
    if active and -3 <= overdue <= 0:
        return {
            "key": f"due:{loan['issue_id']}:{due.isoformat()}",
            "issue_id": loan["issue_id"],
            "channel": "SMS",
            "recipient": loan["phone"],
            "subject": "Library return reminder",
            "body": prefix + f"Return by {due.isoformat()} ({-overdue} day(s) left). "
            f"Late fine: Tk {DAILY_FINE}/day from {(due + timedelta(days=1)).isoformat()}. "
            "Please return the book to the library by the due date to avoid a fine.",
        }
    amount = float(loan.get("balance") or 0) if not active else overdue * DAILY_FINE
    if overdue >= 1 and amount > 0:
        # First overdue day, then every ten days: 1, 11, 21, ...
        milestone = 1 + ((overdue - 1) // 10) * 10
        note = (
            f"The book is {overdue} day(s) overdue. Current estimated fine: Tk {amount:g}. "
            f"The fine increases by Tk {DAILY_FINE} each overdue day until return. "
            "Please return the book as soon as possible and pay the final fine in full at the library."
            if active
            else f"Your book has been returned. Outstanding recorded fine: Tk {amount:g}. "
            "The fine no longer increases after return. Please pay the outstanding fine in full at the library."
        )
        return {
            "key": f"fine:{loan['issue_id']}:{due.isoformat()}:{milestone}",
            "issue_id": loan["issue_id"],
            "channel": "EMAIL",
            "recipient": loan["email"],
            "subject": f"Library fine reminder: {book} — Tk {amount:g}",
            "body": prefix
            + f"Return was due on {due.isoformat()}. "
            + note
            + f"\nAs of {today.isoformat()} (Asia/Dhaka).",
        }
    return None
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Reminder rules and message content, independent of providers and scheduling.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from datetime import date, datetime, timedelta, timezone</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>DAILY_FINE = 10</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 6 | <code>DHAKA = timezone(timedelta(hours=6), &quot;Asia/Dhaka&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>def reminder_for(loan, today=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 10 | <code>    today = today or datetime.now(DHAKA).date()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 11 | <code>    due = date.fromisoformat(loan[&quot;due_date&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 12 | <code>    overdue = (today - due).days</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 13 | <code>    active = loan[&quot;status&quot;] == &quot;ISSUED&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 14 | <code>    member = f&quot;PSTU-{int(loan[&#x27;student_id&#x27;]):04d}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 15 | <code>    book = f&quot;{loan[&#x27;title&#x27;]} (Copy #{loan[&#x27;copy_no&#x27;]})&quot; if loan.get(&quot;copy_no&quot;) else loan[&quot;title&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 16 | <code>    prefix = f&quot;PSTU Library: {loan[&#x27;name&#x27;]} ({member}), book: {book}. &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 17 | <code>    if active and -3 &lt;= overdue &lt;= 0:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reminder_for` অংশে |
| 18 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reminder_for` অংশে |
| 19 | <code>            &quot;key&quot;: f&quot;due:{loan[&#x27;issue_id&#x27;]}:{due.isoformat()}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 20 | <code>            &quot;issue_id&quot;: loan[&quot;issue_id&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 21 | <code>            &quot;channel&quot;: &quot;SMS&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 22 | <code>            &quot;recipient&quot;: loan[&quot;phone&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 23 | <code>            &quot;subject&quot;: &quot;Library return reminder&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 24 | <code>            &quot;body&quot;: prefix + f&quot;Return by {due.isoformat()} ({-overdue} day(s) left). &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 25 | <code>            f&quot;Late fine: Tk {DAILY_FINE}/day from {(due + timedelta(days=1)).isoformat()}. &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 26 | <code>            &quot;Please return the book to the library by the due date to avoid a fine.&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 27 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 28 | <code>    amount = float(loan.get(&quot;balance&quot;) or 0) if not active else overdue * DAILY_FINE</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 29 | <code>    if overdue &gt;= 1 and amount &gt; 0:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reminder_for` অংশে |
| 30 | <code>        # First overdue day, then every ten days: 1, 11, 21, ...</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 31 | <code>        milestone = 1 + ((overdue - 1) // 10) * 10</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 32 | <code>        note = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `reminder_for` অংশে |
| 33 | <code>            f&quot;The book is {overdue} day(s) overdue. Current estimated fine: Tk {amount:g}. &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 34 | <code>            f&quot;The fine increases by Tk {DAILY_FINE} each overdue day until return. &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 35 | <code>            &quot;Please return the book as soon as possible and pay the final fine in full at the library.&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 36 | <code>            if active</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `reminder_for` অংশে |
| 37 | <code>            else f&quot;Your book has been returned. Outstanding recorded fine: Tk {amount:g}. &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 38 | <code>            &quot;The fine no longer increases after return. Please pay the outstanding fine in full at the library.&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 39 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 40 | <code>        return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reminder_for` অংশে |
| 41 | <code>            &quot;key&quot;: f&quot;fine:{loan[&#x27;issue_id&#x27;]}:{due.isoformat()}:{milestone}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 42 | <code>            &quot;issue_id&quot;: loan[&quot;issue_id&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 43 | <code>            &quot;channel&quot;: &quot;EMAIL&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 44 | <code>            &quot;recipient&quot;: loan[&quot;email&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 45 | <code>            &quot;subject&quot;: f&quot;Library fine reminder: {book} — Tk {amount:g}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 46 | <code>            &quot;body&quot;: prefix</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 47 | <code>            + f&quot;Return was due on {due.isoformat()}. &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 48 | <code>            + note</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 49 | <code>            + f&quot;\nAs of {today.isoformat()} (Asia/Dhaka).&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 50 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `reminder_for` অংশে |
| 51 | <code>    return None</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `reminder_for` অংশে |
