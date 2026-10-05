# backend/auth/passwords.py

Salted PBKDF2 password hashes তৈরি ও verify করে; legacy plaintext management passwords-ও login-এর সময় verify করতে পারে।

Source: [মূল file](../../backend/auth/passwords.py)। Snapshot 2026-10-04; 31 lines; SHA-256 `ab0c9e791caaa38874fd7fa97d0f348406a18315c5353a45bdce86b779d27e12`।

## Function / object / element inventory

### `hash_password` — L11–L15

`def hash_password(password):`

16-byte random salt এবং 260000 PBKDF2-HMAC-SHA256 rounds দিয়ে digest তৈরি করে; salt/digest Base64-এ serialize করে।

### `verify_password` — L18–L31

`def verify_password(password, stored):`

Legacy value হলে constant-time comparison; hash হলে format/rounds/salt decode করে PBKDF2 পুনরায় চালিয়ে compare করে। Malformed storage false ফেরায়।

## সম্পূর্ণ original source

```python
"""Salted password storage with compatibility for existing demo accounts."""

import base64
import hashlib
import hmac
import secrets

ITERATIONS = 260000


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    encode = lambda value: base64.b64encode(value).decode("ascii")
    return f"pbkdf2${ITERATIONS}${encode(salt)}${encode(digest)}"


def verify_password(password, stored):
    if not stored.startswith("pbkdf2$"):
        return hmac.compare_digest(password.encode("utf-8"), stored.encode("utf-8"))
    try:
        _, iterations, salt, expected = stored.split("$")
        rounds = int(iterations)
        if not 100000 <= rounds <= 1000000:
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), base64.b64decode(salt, validate=True), rounds
        )
        return hmac.compare_digest(actual, base64.b64decode(expected, validate=True))
    except (ValueError, TypeError):
        return False
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Salted password storage with compatibility for existing demo accounts.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import base64</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import hashlib</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>import hmac</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>import secrets</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>ITERATIONS = 260000</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>def hash_password(password):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 12 | <code>    salt = secrets.token_bytes(16)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `hash_password` অংশে |
| 13 | <code>    digest = hashlib.pbkdf2_hmac(&quot;sha256&quot;, password.encode(&quot;utf-8&quot;), salt, ITERATIONS)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `hash_password` অংশে |
| 14 | <code>    encode = lambda value: base64.b64encode(value).decode(&quot;ascii&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `hash_password` অংশে |
| 15 | <code>    return f&quot;pbkdf2${ITERATIONS}${encode(salt)}${encode(digest)}&quot;</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `hash_password` অংশে |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>def verify_password(password, stored):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 19 | <code>    if not stored.startswith(&quot;pbkdf2$&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `verify_password` অংশে |
| 20 | <code>        return hmac.compare_digest(password.encode(&quot;utf-8&quot;), stored.encode(&quot;utf-8&quot;))</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `verify_password` অংশে |
| 21 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `verify_password` অংশে |
| 22 | <code>        _, iterations, salt, expected = stored.split(&quot;$&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `verify_password` অংশে |
| 23 | <code>        rounds = int(iterations)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `verify_password` অংশে |
| 24 | <code>        if not 100000 &lt;= rounds &lt;= 1000000:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `verify_password` অংশে |
| 25 | <code>            return False</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `verify_password` অংশে |
| 26 | <code>        actual = hashlib.pbkdf2_hmac(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `verify_password` অংশে |
| 27 | <code>            &quot;sha256&quot;, password.encode(&quot;utf-8&quot;), base64.b64decode(salt, validate=True), rounds</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `verify_password` অংশে |
| 28 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `verify_password` অংশে |
| 29 | <code>        return hmac.compare_digest(actual, base64.b64decode(expected, validate=True))</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `verify_password` অংশে |
| 30 | <code>    except (ValueError, TypeError):</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `verify_password` অংশে |
| 31 | <code>        return False</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `verify_password` অংশে |
