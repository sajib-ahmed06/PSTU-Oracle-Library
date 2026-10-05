# backend/auth/validation.py

Validate member IDs, staff usernames and account passwords.

Source: [মূল file](../../backend/auth/validation.py)। Snapshot 2026-10-04; 24 lines; SHA-256 `9487ba5388cbd8c813df988d98cdf0b8cd3c48e9209b90d93034a77e560a869b`।

## Function / object / element inventory

### `member_number` — L9–L13

`def member_number(value):`

Test/setup helper: member number; নিচের assertions/calls সেই behavior define করে।

### `validate_password` — L16–L18

`def validate_password(password):`

Test/setup helper: validate password; নিচের assertions/calls সেই behavior define করে।

### `validate_credentials` — L21–L24

`def validate_credentials(username, password):`

Username letter দিয়ে শুরু, 3–30 characters এবং letters/digits/underscore; password 4–128 characters হতে হয়।

## সম্পূর্ণ original source

```python
"""Member ID, staff username, and password validation."""

import re
from fastapi import HTTPException

USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,29}")


def member_number(value):
    match = re.fullmatch(r"(?:PSTU-)?([0-9]{1,20})", value.strip(), re.I)
    if not match or int(match[1]) < 1:
        raise HTTPException(400, "Enter a valid Member ID, for example PSTU-0001")
    return int(match[1])


def validate_password(password):
    if not 4 <= len(password) <= 128:
        raise HTTPException(400, "Password must contain 4-128 characters")


def validate_credentials(username, password):
    if not USERNAME_PATTERN.fullmatch(username):
        raise HTTPException(400, "Username must be 3-30 letters, numbers or underscores")
    validate_password(password)
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Member ID, staff username, and password validation.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>USERNAME_PATTERN = re.compile(r&quot;[A-Za-z][A-Za-z0-9_]{2,29}&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>def member_number(value):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 10 | <code>    match = re.fullmatch(r&quot;(?:PSTU-)?([0-9]{1,20})&quot;, value.strip(), re.I)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `member_number` অংশে |
| 11 | <code>    if not match or int(match[1]) &lt; 1:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `member_number` অংশে |
| 12 | <code>        raise HTTPException(400, &quot;Enter a valid Member ID, for example PSTU-0001&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `member_number` অংশে |
| 13 | <code>    return int(match[1])</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `member_number` অংশে |
| 14 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>def validate_password(password):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 17 | <code>    if not 4 &lt;= len(password) &lt;= 128:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `validate_password` অংশে |
| 18 | <code>        raise HTTPException(400, &quot;Password must contain 4-128 characters&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `validate_password` অংশে |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 21 | <code>def validate_credentials(username, password):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 22 | <code>    if not USERNAME_PATTERN.fullmatch(username):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `validate_credentials` অংশে |
| 23 | <code>        raise HTTPException(400, &quot;Username must be 3-30 letters, numbers or underscores&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `validate_credentials` অংশে |
| 24 | <code>    validate_password(password)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `validate_credentials` অংশে |
