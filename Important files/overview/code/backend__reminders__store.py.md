# backend/reminders/store.py

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../backend/reminders/store.py)। Snapshot 2026-10-04; 63 lines; SHA-256 `7dd34b6a25e745ab1dc75a0963603678dbc3cb0b28244eca40bdee2190d22171`।

## Function / object / element inventory

### `loans` — L6–L29

`def loans(issue_id=None):`

Test/setup helper: loans; নিচের assertions/calls সেই behavior define করে।

### `claim` — L32–L44

`def claim(message):`

Test/setup helper: claim; নিচের assertions/calls সেই behavior define করে।

### `finish` — L47–L55

`def finish(key, status, provider_id=None):`

Test/setup helper: finish; নিচের assertions/calls সেই behavior define করে।

### `recover_abandoned` — L58–L63

`def recover_abandoned():`

Test/setup helper: recover abandoned; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
"""Oracle-backed atomic claims prevent duplicate sends across restarts/workers."""

from backend.database import quote, rows, run_sql


def loans(issue_id=None):
    restriction = f" AND i.issue_id={int(issue_id)}" if issue_id is not None else ""
    return rows(
        "SELECT i.issue_id||'|'||i.student_id||'|'||REPLACE(s.name,'|',' ')||'|'||s.phone||'|'||s.email||'|'||"
        "REPLACE(b.title,'|',' ')||'|'||NVL(TO_CHAR(c.copy_no),'~')||'|'||"
        "TO_CHAR(i.due_date,'YYYY-MM-DD')||'|'||i.status||'|'||NVL(f.amount-f.paid_amount,0) "
        "FROM issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id "
        "LEFT JOIN book_copy c ON c.copy_id=i.copy_id LEFT JOIN fine f ON f.issue_id=i.issue_id "
        "WHERE i.due_date IS NOT NULL AND (i.status='ISSUED' OR f.amount>f.paid_amount)"
        + restriction,
        [
            "issue_id",
            "student_id",
            "name",
            "phone",
            "email",
            "title",
            "copy_no",
            "due_date",
            "status",
            "balance",
        ],
        {"issue_id", "student_id", "copy_no", "balance"},
    )


def claim(message):
    key = quote(message["key"])
    result = run_sql(
        "SET SERVEROUTPUT ON\nDECLARE claimed NUMBER:=0; BEGIN\n"
        "BEGIN INSERT INTO reminder_delivery(event_key,issue_id,channel,status,attempts) "
        f"VALUES({key},{int(message['issue_id'])},{quote(message['channel'])},'SENDING',1); "
        "claimed:=1; EXCEPTION WHEN DUP_VAL_ON_INDEX THEN "
        "UPDATE reminder_delivery SET status='SENDING',attempts=attempts+1,updated_at=SYSDATE "
        f"WHERE event_key={key} AND status='FAILED' AND attempts<3 AND next_attempt<=SYSDATE; "
        "claimed:=SQL%ROWCOUNT; END; COMMIT; "
        "IF claimed=1 THEN DBMS_OUTPUT.PUT_LINE('CLAIMED'); END IF; END;\n/"
    )
    return "CLAIMED" in result.splitlines()


def finish(key, status, provider_id=None):
    if status not in {"ACCEPTED", "FAILED", "UNKNOWN", "CANCELLED"}:
        raise ValueError("Invalid delivery status")
    provider = quote(provider_id) if provider_id else "NULL"
    run_sql(
        f"UPDATE reminder_delivery SET status={quote(status)},provider_id={provider},"
        "updated_at=SYSDATE,next_attempt=SYSDATE+30/1440 "
        f"WHERE event_key={quote(key)} AND status='SENDING';\nCOMMIT;"
    )


def recover_abandoned():
    # Sending may have succeeded before a process/connection failure. Never replay it blindly.
    run_sql(
        "UPDATE reminder_delivery SET status='UNKNOWN',updated_at=SYSDATE "
        "WHERE status='SENDING' AND updated_at<SYSDATE-15/1440;\nCOMMIT;"
    )
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Oracle-backed atomic claims prevent duplicate sends across restarts/workers.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from backend.database import quote, rows, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>def loans(issue_id=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 7 | <code>    restriction = f&quot; AND i.issue_id={int(issue_id)}&quot; if issue_id is not None else &quot;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loans` অংশে |
| 8 | <code>    return rows(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `loans` অংশে |
| 9 | <code>        &quot;SELECT i.issue_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.student_id&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;REPLACE(s.name,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;s.phone&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;s.email&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 10 | <code>        &quot;REPLACE(b.title,&#x27;&#124;&#x27;,&#x27; &#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(TO_CHAR(c.copy_no),&#x27;~&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 11 | <code>        &quot;TO_CHAR(i.due_date,&#x27;YYYY-MM-DD&#x27;)&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;i.status&#124;&#124;&#x27;&#124;&#x27;&#124;&#124;NVL(f.amount-f.paid_amount,0) &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 12 | <code>        &quot;FROM issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loans` অংশে |
| 13 | <code>        &quot;LEFT JOIN book_copy c ON c.copy_id=i.copy_id LEFT JOIN fine f ON f.issue_id=i.issue_id &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loans` অংশে |
| 14 | <code>        &quot;WHERE i.due_date IS NOT NULL AND (i.status=&#x27;ISSUED&#x27; OR f.amount&gt;f.paid_amount)&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loans` অংশে |
| 15 | <code>        + restriction,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 16 | <code>        [</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 17 | <code>            &quot;issue_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 18 | <code>            &quot;student_id&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 19 | <code>            &quot;name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 20 | <code>            &quot;phone&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 21 | <code>            &quot;email&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 22 | <code>            &quot;title&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 23 | <code>            &quot;copy_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 24 | <code>            &quot;due_date&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 25 | <code>            &quot;status&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 26 | <code>            &quot;balance&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 27 | <code>        ],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 28 | <code>        {&quot;issue_id&quot;, &quot;student_id&quot;, &quot;copy_no&quot;, &quot;balance&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 29 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loans` অংশে |
| 30 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>def claim(message):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 33 | <code>    key = quote(message[&quot;key&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 34 | <code>    result = run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `claim` অংশে |
| 35 | <code>        &quot;SET SERVEROUTPUT ON\nDECLARE claimed NUMBER:=0; BEGIN\n&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 36 | <code>        &quot;BEGIN INSERT INTO reminder_delivery(event_key,issue_id,channel,status,attempts) &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `claim` অংশে |
| 37 | <code>        f&quot;VALUES({key},{int(message[&#x27;issue_id&#x27;])},{quote(message[&#x27;channel&#x27;])},&#x27;SENDING&#x27;,1); &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `claim` অংশে |
| 38 | <code>        &quot;claimed:=1; EXCEPTION WHEN DUP_VAL_ON_INDEX THEN &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 39 | <code>        &quot;UPDATE reminder_delivery SET status=&#x27;SENDING&#x27;,attempts=attempts+1,updated_at=SYSDATE &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 40 | <code>        f&quot;WHERE event_key={key} AND status=&#x27;FAILED&#x27; AND attempts&lt;3 AND next_attempt&lt;=SYSDATE; &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 41 | <code>        &quot;claimed:=SQL%ROWCOUNT; END; COMMIT; &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 42 | <code>        &quot;IF claimed=1 THEN DBMS_OUTPUT.PUT_LINE(&#x27;CLAIMED&#x27;); END IF; END;\n/&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `claim` অংশে |
| 43 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `claim` অংশে |
| 44 | <code>    return &quot;CLAIMED&quot; in result.splitlines()</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `claim` অংশে |
| 45 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 46 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 47 | <code>def finish(key, status, provider_id=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 48 | <code>    if status not in {&quot;ACCEPTED&quot;, &quot;FAILED&quot;, &quot;UNKNOWN&quot;, &quot;CANCELLED&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `finish` অংশে |
| 49 | <code>        raise ValueError(&quot;Invalid delivery status&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `finish` অংশে |
| 50 | <code>    provider = quote(provider_id) if provider_id else &quot;NULL&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `finish` অংশে |
| 51 | <code>    run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `finish` অংশে |
| 52 | <code>        f&quot;UPDATE reminder_delivery SET status={quote(status)},provider_id={provider},&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `finish` অংশে |
| 53 | <code>        &quot;updated_at=SYSDATE,next_attempt=SYSDATE+30/1440 &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `finish` অংশে |
| 54 | <code>        f&quot;WHERE event_key={quote(key)} AND status=&#x27;SENDING&#x27;;\nCOMMIT;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `finish` অংশে |
| 55 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `finish` অংশে |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 58 | <code>def recover_abandoned():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 59 | <code>    # Sending may have succeeded before a process/connection failure. Never replay it blindly.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 60 | <code>    run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `recover_abandoned` অংশে |
| 61 | <code>        &quot;UPDATE reminder_delivery SET status=&#x27;UNKNOWN&#x27;,updated_at=SYSDATE &quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `recover_abandoned` অংশে |
| 62 | <code>        &quot;WHERE status=&#x27;SENDING&#x27; AND updated_at&lt;SYSDATE-15/1440;\nCOMMIT;&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `recover_abandoned` অংশে |
| 63 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `recover_abandoned` অংশে |
