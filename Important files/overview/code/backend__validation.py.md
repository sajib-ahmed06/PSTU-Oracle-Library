# backend/validation.py

URL-encoded form parsing, required fields, integer, text length, academic IDs এবং member contact তথ্য যাচাই করে।

Source: [মূল file](../../backend/validation.py)। Snapshot 2026-10-04; 113 lines; SHA-256 `76bd4c7f13e513e3831cbf347d984c14a691bf34428cca8a4f1c92eee44e200b`।

## Function / object / element inventory

### `form_data` — L10–L23

`async def form_data(request):`

Request body পড়ে 16 KiB ও 30-field সীমা যাচাই করে। UTF-8, percent encoding ও duplicate keys যাচাই করে URL-encoded values-এর dictionary ফেরত দেয়।

### `required` — L26–L29

`def required(data, *keys):`

প্রয়োজনীয় fields absent, None অথবা whitespace-only হলে HTTP 400 তোলে।

### `positive_number` — L32–L39

`def positive_number(value, field):`

int conversion-এর পরে value অন্তত 1 কি না দেখে। Form strings-এর fractional input int conversion-এ reject হয়।

### `payment_amount` — L42–L54

`def payment_amount(value):`

Test/setup helper: payment amount; নিচের assertions/calls সেই behavior define করে।

### `text_field` — L57–L63

`def text_field(value, field, maximum):`

Whitespace trim করে UTF-8 byte length ও control characters যাচাই করে normalized text ফেরত দেয়।

### `academic_identifier` — L66–L72

`def academic_identifier(value, field):`

Identifier uppercase করে সর্বোচ্চ 40 bytes এবং letters/digits/dot/slash/underscore/hyphen pattern যাচাই করে; leading zero বজায় থাকে।

### `academic_session` — L75–L86

`def academic_session(value):`

Test/setup helper: academic session; নিচের assertions/calls সেই behavior define করে।

### `member_details` — L89–L113

`def member_details(data):`

নাম, department, phone, email, roll ও registration একসঙ্গে normalize/validate করে; email lowercase এবং phone ঠিক 11 ASCII digits হতে হয়।

## সম্পূর্ণ original source

```python
"""Validation shared by form endpoints."""

import re
from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qs

from fastapi import HTTPException


async def form_data(request):
    body = await request.body()
    if len(body) > 16384:
        raise HTTPException(413, "Form is too large")
    try:
        encoded = body.decode("utf-8")
        if re.search(r"%(?![0-9A-Fa-f]{2})", encoded):
            raise ValueError("Malformed percent encoding")
        parsed = parse_qs(encoded, keep_blank_values=True, max_num_fields=30, errors="strict")
        if any(len(values) != 1 for values in parsed.values()):
            raise ValueError("Duplicate form fields")
    except (UnicodeDecodeError, ValueError):
        raise HTTPException(400, "Invalid form data")
    return {key: value[0] for key, value in parsed.items()}


def required(data, *keys):
    missing = [key for key in keys if data.get(key) is None or not str(data[key]).strip()]
    if missing:
        raise HTTPException(400, "Missing fields: " + ", ".join(missing))


def positive_number(value, field):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise HTTPException(400, f"{field} must be a number")
    if number < 1:
        raise HTTPException(400, f"{field} must be greater than zero")
    return number


def payment_amount(value):
    try:
        amount = Decimal(str(value))
        if (
            not amount.is_finite()
            or amount <= 0
            or amount > Decimal("9999999999.99")
            or amount != amount.quantize(Decimal("0.01"))
        ):
            raise ValueError()
    except (InvalidOperation, ValueError):
        raise HTTPException(400, "Enter a positive payment with at most 2 decimal places")
    return format(amount, ".2f")


def text_field(value, field, maximum):
    text = str(value or "").strip()
    if not text or len(text.encode("utf-8")) > maximum:
        raise HTTPException(400, f"{field} must contain 1-{maximum} bytes")
    if any(ord(character) < 32 for character in text):
        raise HTTPException(400, f"{field} cannot contain control characters")
    return text


def academic_identifier(value, field):
    identifier = text_field(value, field, 40).upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9./_-]{0,39}", identifier):
        raise HTTPException(
            400, f"{field} must use letters, numbers, dots, slashes, underscores or hyphens"
        )
    return identifier


def academic_session(value):
    value = str(value).strip()
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}", value):
        next_year = int(value[:4]) + 1
        if next_year > 9999 or int(value[5:]) != next_year % 100:
            raise HTTPException(400, "Academic session must cover consecutive years")
        value = f"{value[:4]}-{next_year:04d}"
    if not re.fullmatch(r"[0-9]{4}-[0-9]{4}", value):
        raise HTTPException(400, "Enter an academic session such as 2023-24 or 2023-2024")
    if int(value[5:]) != int(value[:4]) + 1:
        raise HTTPException(400, "Academic session must cover consecutive years")
    return value


def member_details(data):
    required(
        data,
        "name",
        "department",
        "phone",
        "email",
        "roll_no",
        "registration_no",
        "academic_session",
    )
    details = {
        "academic_session": academic_session(data["academic_session"]),
        "name": text_field(data["name"], "name", 100),
        "department": text_field(data["department"], "department", 100),
        "email": text_field(data["email"], "email", 100).lower(),
        "phone": str(data["phone"]).strip(),
        "roll_no": academic_identifier(data["roll_no"], "ID/Roll number"),
        "registration_no": academic_identifier(data["registration_no"], "Registration number"),
    }
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", details["email"]):
        raise HTTPException(400, "Enter a valid email address")
    if not re.fullmatch(r"[0-9]{11}", details["phone"]):
        raise HTTPException(400, "Phone number must contain exactly 11 digits")
    return details
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Validation shared by form endpoints.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from decimal import Decimal, InvalidOperation</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from urllib.parse import parse_qs</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>async def form_data(request):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 11 | <code>    body = await request.body()</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `form_data` অংশে |
| 12 | <code>    if len(body) &gt; 16384:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `form_data` অংশে |
| 13 | <code>        raise HTTPException(413, &quot;Form is too large&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `form_data` অংশে |
| 14 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `form_data` অংশে |
| 15 | <code>        encoded = body.decode(&quot;utf-8&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `form_data` অংশে |
| 16 | <code>        if re.search(r&quot;%(?![0-9A-Fa-f]{2})&quot;, encoded):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `form_data` অংশে |
| 17 | <code>            raise ValueError(&quot;Malformed percent encoding&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `form_data` অংশে |
| 18 | <code>        parsed = parse_qs(encoded, keep_blank_values=True, max_num_fields=30, errors=&quot;strict&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `form_data` অংশে |
| 19 | <code>        if any(len(values) != 1 for values in parsed.values()):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `form_data` অংশে |
| 20 | <code>            raise ValueError(&quot;Duplicate form fields&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `form_data` অংশে |
| 21 | <code>    except (UnicodeDecodeError, ValueError):</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `form_data` অংশে |
| 22 | <code>        raise HTTPException(400, &quot;Invalid form data&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `form_data` অংশে |
| 23 | <code>    return {key: value[0] for key, value in parsed.items()}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `form_data` অংশে |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 26 | <code>def required(data, *keys):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 27 | <code>    missing = [key for key in keys if data.get(key) is None or not str(data[key]).strip()]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `required` অংশে |
| 28 | <code>    if missing:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `required` অংশে |
| 29 | <code>        raise HTTPException(400, &quot;Missing fields: &quot; + &quot;, &quot;.join(missing))</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `required` অংশে |
| 30 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>def positive_number(value, field):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 33 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `positive_number` অংশে |
| 34 | <code>        number = int(value)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `positive_number` অংশে |
| 35 | <code>    except (TypeError, ValueError):</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `positive_number` অংশে |
| 36 | <code>        raise HTTPException(400, f&quot;{field} must be a number&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `positive_number` অংশে |
| 37 | <code>    if number &lt; 1:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `positive_number` অংশে |
| 38 | <code>        raise HTTPException(400, f&quot;{field} must be greater than zero&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `positive_number` অংশে |
| 39 | <code>    return number</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `positive_number` অংশে |
| 40 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 41 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 42 | <code>def payment_amount(value):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 43 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `payment_amount` অংশে |
| 44 | <code>        amount = Decimal(str(value))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `payment_amount` অংশে |
| 45 | <code>        if (</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `payment_amount` অংশে |
| 46 | <code>            not amount.is_finite()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `payment_amount` অংশে |
| 47 | <code>            or amount &lt;= 0</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `payment_amount` অংশে |
| 48 | <code>            or amount &gt; Decimal(&quot;9999999999.99&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `payment_amount` অংশে |
| 49 | <code>            or amount != amount.quantize(Decimal(&quot;0.01&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `payment_amount` অংশে |
| 50 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `payment_amount` অংশে |
| 51 | <code>            raise ValueError()</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `payment_amount` অংশে |
| 52 | <code>    except (InvalidOperation, ValueError):</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `payment_amount` অংশে |
| 53 | <code>        raise HTTPException(400, &quot;Enter a positive payment with at most 2 decimal places&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `payment_amount` অংশে |
| 54 | <code>    return format(amount, &quot;.2f&quot;)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `payment_amount` অংশে |
| 55 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>def text_field(value, field, maximum):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 58 | <code>    text = str(value or &quot;&quot;).strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `text_field` অংশে |
| 59 | <code>    if not text or len(text.encode(&quot;utf-8&quot;)) &gt; maximum:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `text_field` অংশে |
| 60 | <code>        raise HTTPException(400, f&quot;{field} must contain 1-{maximum} bytes&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `text_field` অংশে |
| 61 | <code>    if any(ord(character) &lt; 32 for character in text):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `text_field` অংশে |
| 62 | <code>        raise HTTPException(400, f&quot;{field} cannot contain control characters&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `text_field` অংশে |
| 63 | <code>    return text</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `text_field` অংশে |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>def academic_identifier(value, field):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 67 | <code>    identifier = text_field(value, field, 40).upper()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `academic_identifier` অংশে |
| 68 | <code>    if not re.fullmatch(r&quot;[A-Z0-9][A-Z0-9./_-]{0,39}&quot;, identifier):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `academic_identifier` অংশে |
| 69 | <code>        raise HTTPException(</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `academic_identifier` অংশে |
| 70 | <code>            400, f&quot;{field} must use letters, numbers, dots, slashes, underscores or hyphens&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `academic_identifier` অংশে |
| 71 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `academic_identifier` অংশে |
| 72 | <code>    return identifier</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `academic_identifier` অংশে |
| 73 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 74 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 75 | <code>def academic_session(value):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 76 | <code>    value = str(value).strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `academic_session` অংশে |
| 77 | <code>    if re.fullmatch(r&quot;[0-9]{4}-[0-9]{2}&quot;, value):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `academic_session` অংশে |
| 78 | <code>        next_year = int(value[:4]) + 1</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `academic_session` অংশে |
| 79 | <code>        if next_year &gt; 9999 or int(value[5:]) != next_year % 100:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `academic_session` অংশে |
| 80 | <code>            raise HTTPException(400, &quot;Academic session must cover consecutive years&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `academic_session` অংশে |
| 81 | <code>        value = f&quot;{value[:4]}-{next_year:04d}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `academic_session` অংশে |
| 82 | <code>    if not re.fullmatch(r&quot;[0-9]{4}-[0-9]{4}&quot;, value):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `academic_session` অংশে |
| 83 | <code>        raise HTTPException(400, &quot;Enter an academic session such as 2023-24 or 2023-2024&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `academic_session` অংশে |
| 84 | <code>    if int(value[5:]) != int(value[:4]) + 1:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `academic_session` অংশে |
| 85 | <code>        raise HTTPException(400, &quot;Academic session must cover consecutive years&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `academic_session` অংশে |
| 86 | <code>    return value</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `academic_session` অংশে |
| 87 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 88 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 89 | <code>def member_details(data):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 90 | <code>    required(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 91 | <code>        data,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 92 | <code>        &quot;name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 93 | <code>        &quot;department&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 94 | <code>        &quot;phone&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 95 | <code>        &quot;email&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 96 | <code>        &quot;roll_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 97 | <code>        &quot;registration_no&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 98 | <code>        &quot;academic_session&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 99 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 100 | <code>    details = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `member_details` অংশে |
| 101 | <code>        &quot;academic_session&quot;: academic_session(data[&quot;academic_session&quot;]),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 102 | <code>        &quot;name&quot;: text_field(data[&quot;name&quot;], &quot;name&quot;, 100),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 103 | <code>        &quot;department&quot;: text_field(data[&quot;department&quot;], &quot;department&quot;, 100),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 104 | <code>        &quot;email&quot;: text_field(data[&quot;email&quot;], &quot;email&quot;, 100).lower(),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 105 | <code>        &quot;phone&quot;: str(data[&quot;phone&quot;]).strip(),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 106 | <code>        &quot;roll_no&quot;: academic_identifier(data[&quot;roll_no&quot;], &quot;ID/Roll number&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 107 | <code>        &quot;registration_no&quot;: academic_identifier(data[&quot;registration_no&quot;], &quot;Registration number&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 108 | <code>    }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `member_details` অংশে |
| 109 | <code>    if not re.fullmatch(r&quot;[^\s@]+@[^\s@]+\.[^\s@]+&quot;, details[&quot;email&quot;]):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `member_details` অংশে |
| 110 | <code>        raise HTTPException(400, &quot;Enter a valid email address&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `member_details` অংশে |
| 111 | <code>    if not re.fullmatch(r&quot;[0-9]{11}&quot;, details[&quot;phone&quot;]):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `member_details` অংশে |
| 112 | <code>        raise HTTPException(400, &quot;Phone number must contain exactly 11 digits&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `member_details` অংশে |
| 113 | <code>    return details</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `member_details` অংশে |
