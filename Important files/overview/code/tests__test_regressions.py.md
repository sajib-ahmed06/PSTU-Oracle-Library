# tests/test_regressions.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_regressions.py)। Snapshot 2026-10-04; 144 lines; SHA-256 `169725850395cde7b6a9c93d4f453feea61dbd57acac2a95343a5ff14d5dd74b`।

## Function / object / element inventory

### `tearDown` — L17–L18

`def tearDown(self):`

Test/setup helper: tearDown; নিচের assertions/calls সেই behavior define করে।

### `test_password_hash_and_legacy_compatibility` — L20–L26

`def test_password_hash_and_legacy_compatibility(self):`

Test/setup helper: test password hash and legacy compatibility; নিচের assertions/calls সেই behavior define করে।

### `test_sqlplus_control_input_rejected` — L28–L32

`def test_sqlplus_control_input_rejected(self):`

Test/setup helper: test sqlplus control input rejected; নিচের assertions/calls সেই behavior define করে।

### `test_form_blank_and_invalid_utf8` — L34–L42

`def test_form_blank_and_invalid_utf8(self):`

Test/setup helper: test form blank and invalid utf8; নিচের assertions/calls সেই behavior define করে।

### `body` — L35–L36

`async def body():`

Test/setup helper: body; নিচের assertions/calls সেই behavior define করে।

### `test_login_upgrades_legacy_password` — L44–L91

`def test_login_upgrades_legacy_password(self):`

Test/setup helper: test login upgrades legacy password; নিচের assertions/calls সেই behavior define করে।

### `users` — L48–L57

`def users(*args):`

Test/setup helper: users; নিচের assertions/calls সেই behavior define করে।

### `receive` — L68–L73

`async def receive():`

Test/setup helper: receive; নিচের assertions/calls সেই behavior define করে।

### `test_invalid_utf8_form_rejected` — L93–L99

`def test_invalid_utf8_form_rejected(self):`

Test/setup helper: test invalid utf8 form rejected; নিচের assertions/calls সেই behavior define করে।

### `body` — L94–L95

`async def body():`

Test/setup helper: body; নিচের assertions/calls সেই behavior define করে।

### `test_sessions_expire_and_invalidate` — L101–L109

`def test_sessions_expire_and_invalidate(self):`

Test/setup helper: test sessions expire and invalidate; নিচের assertions/calls সেই behavior define করে।

### `test_row_parser_fails_on_corrupt_records` — L111–L118

`def test_row_parser_fails_on_corrupt_records(self):`

Test/setup helper: test row parser fails on corrupt records; নিচের assertions/calls সেই behavior define করে।

### `test_missing_fine_is_checked_in_transaction` — L120–L130

`def test_missing_fine_is_checked_in_transaction(self):`

Test/setup helper: test missing fine is checked in transaction; নিচের assertions/calls সেই behavior define করে।

### `receive` — L121–L122

`async def receive():`

Test/setup helper: receive; নিচের assertions/calls সেই behavior define করে।

### `test_sqlplus_errors_are_mapped_and_rollback_enabled` — L132–L140

`def test_sqlplus_errors_are_mapped_and_rollback_enabled(self):`

Test/setup helper: test sqlplus errors are mapped and rollback enabled; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
from backend.routes import fines
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from backend.auth.routes import register_auth_routes
from backend import database, main
from backend.auth.passwords import hash_password, verify_password
from backend.auth.session import SESSIONS, create_session, current_session, invalidate_user_sessions
from backend.validation import form_data, required


class RegressionTests(unittest.TestCase):
    def tearDown(self):
        SESSIONS.clear()

    def test_password_hash_and_legacy_compatibility(self):
        stored = hash_password("test-password")
        self.assertLessEqual(len(stored), 100)
        self.assertTrue(verify_password("test-password", stored))
        self.assertFalse(verify_password("wrong", stored))
        self.assertTrue(verify_password("legacy", "legacy"))
        self.assertFalse(verify_password("test", "pbkdf2$broken"))

    def test_sqlplus_control_input_rejected(self):
        self.assertEqual(database.quote("O'Reilly & Co"), "'O''Reilly & Co'")
        self.assertEqual(database.quote(0), "'0'")
        with self.assertRaises(HTTPException):
            database.quote("value\n/\nHOST command")

    def test_form_blank_and_invalid_utf8(self):
        async def body():
            return b"publisher=&title=Clean+Code"

        request = SimpleNamespace(body=body)
        data = asyncio.run(form_data(request))
        self.assertEqual(data["publisher"], "")
        with self.assertRaises(HTTPException):
            required({"title": "   "}, "title")

    def test_login_upgrades_legacy_password(self):
        app = FastAPI()
        writes = []

        def users(*args):
            return [
                {
                    "user_id": 1,
                    "username": "admin",
                    "user_type": "ADMIN",
                    "account_status": "ACTIVE",
                    "password": "fixture-password",
                }
            ]

        with patch.object(app, "include_router") as include:
            register_auth_routes(
                app, None, users, writes.append, database.quote, form_data, required
            )
        router = include.call_args.args[0]
        endpoint = next(
            route.endpoint for route in router.routes if route.path == "/api/auth/login"
        )

        async def receive():
            return {
                "type": "http.request",
                "body": b"username=admin&password=fixture-password",
                "more_body": False,
            }

        request = Request(
            {
                "type": "http",
                "method": "POST",
                "path": "/api/auth/login",
                "scheme": "http",
                "headers": [],
                "server": ("localhost", 8091),
                "query_string": b"",
            },
            receive,
        )
        response = asyncio.run(endpoint(request))
        self.assertEqual(response.status_code, 200)
        self.assertIn("HttpOnly", response.headers["set-cookie"])
        self.assertIn("pbkdf2$", writes[0])
        self.assertNotIn("password='fixture-password'", writes[0])

    def test_invalid_utf8_form_rejected(self):
        async def body():
            return b"name=\xff"

        with self.assertRaises(HTTPException) as error:
            asyncio.run(form_data(SimpleNamespace(body=body)))
        self.assertEqual(error.exception.status_code, 400)

    def test_sessions_expire_and_invalidate(self):
        token = create_session({"user_id": 1, "username": "admin", "user_type": "ADMIN"})
        request = SimpleNamespace(cookies={"library_session": token})
        self.assertIsNotNone(current_session(request))
        invalidate_user_sessions(1)
        self.assertIsNone(current_session(request))
        token = create_session({"user_id": 1, "username": "admin", "user_type": "ADMIN"})
        SESSIONS[token]["expires"] = 0
        self.assertIsNone(current_session(SimpleNamespace(cookies={"library_session": token})))

    def test_row_parser_fails_on_corrupt_records(self):
        with patch.object(database, "run_sql", return_value="1|Clean Code|5"):
            self.assertEqual(
                database.rows("SELECT", ["id", "title", "stock"], {"id", "stock"})[0]["stock"], 5
            )
        with patch.object(database, "run_sql", return_value="1|unexpected|delimiter"):
            with self.assertRaises(HTTPException):
                database.rows("SELECT", ["id", "title"])

    def test_missing_fine_is_checked_in_transaction(self):
        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        request = Request({"type": "http", "method": "POST", "headers": []}, receive)
        with patch.object(fines, "run_sql") as run:
            asyncio.run(main.pay_fine(123, request))
            self.assertIn("pay_fine_proc(123, NULL", run.call_args.args[0])
            self.assertIn("COMMIT", run.call_args.args[0])
        with self.assertRaises(HTTPException):
            asyncio.run(main.pay_fine(-1, request))

    def test_sqlplus_errors_are_mapped_and_rollback_enabled(self):
        result = SimpleNamespace(stdout="ORA-20001: Book is not available", stderr="", returncode=1)
        with patch.object(database.subprocess, "run", return_value=result) as run:
            with self.assertRaises(HTTPException) as error:
                database.run_sql("SELECT 1 FROM dual;")
            self.assertEqual(error.exception.status_code, 409)
            self.assertIn("ROLLBACK", run.call_args.kwargs["input"])
            self.assertIn("SET DEFINE OFF", run.call_args.kwargs["input"])
            self.assertEqual(run.call_args.args[0][-1], "/nolog")


if __name__ == "__main__":
    unittest.main()
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>from backend.routes import fines</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import asyncio</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from types import SimpleNamespace</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>from fastapi import FastAPI, HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from starlette.requests import Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend.auth.routes import register_auth_routes</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from backend import database, main</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from backend.auth.passwords import hash_password, verify_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from backend.auth.session import SESSIONS, create_session, current_session, invalidate_user_sessions</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>from backend.validation import form_data, required</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 14 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>class RegressionTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 17 | <code>    def tearDown(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 18 | <code>        SESSIONS.clear()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `tearDown` অংশে |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>    def test_password_hash_and_legacy_compatibility(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 21 | <code>        stored = hash_password(&quot;test-password&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_password_hash_and_legacy_compatibility` অংশে |
| 22 | <code>        self.assertLessEqual(len(stored), 100)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 23 | <code>        self.assertTrue(verify_password(&quot;test-password&quot;, stored))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 24 | <code>        self.assertFalse(verify_password(&quot;wrong&quot;, stored))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 25 | <code>        self.assertTrue(verify_password(&quot;legacy&quot;, &quot;legacy&quot;))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 26 | <code>        self.assertFalse(verify_password(&quot;test&quot;, &quot;pbkdf2$broken&quot;))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>    def test_sqlplus_control_input_rejected(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 29 | <code>        self.assertEqual(database.quote(&quot;O&#x27;Reilly &amp; Co&quot;), &quot;&#x27;O&#x27;&#x27;Reilly &amp; Co&#x27;&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 30 | <code>        self.assertEqual(database.quote(0), &quot;&#x27;0&#x27;&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 31 | <code>        with self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 32 | <code>            database.quote(&quot;value\n/\nHOST command&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sqlplus_control_input_rejected` অংশে |
| 33 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 34 | <code>    def test_form_blank_and_invalid_utf8(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 35 | <code>        async def body():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 36 | <code>            return b&quot;publisher=&amp;title=Clean+Code&quot;</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `body` অংশে |
| 37 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 38 | <code>        request = SimpleNamespace(body=body)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_form_blank_and_invalid_utf8` অংশে |
| 39 | <code>        data = asyncio.run(form_data(request))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_form_blank_and_invalid_utf8` অংশে |
| 40 | <code>        self.assertEqual(data[&quot;publisher&quot;], &quot;&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 41 | <code>        with self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 42 | <code>            required({&quot;title&quot;: &quot;   &quot;}, &quot;title&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_form_blank_and_invalid_utf8` অংশে |
| 43 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 44 | <code>    def test_login_upgrades_legacy_password(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 45 | <code>        app = FastAPI()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 46 | <code>        writes = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 47 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 48 | <code>        def users(*args):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 49 | <code>            return [</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `users` অংশে |
| 50 | <code>                {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 51 | <code>                    &quot;user_id&quot;: 1,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 52 | <code>                    &quot;username&quot;: &quot;admin&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 53 | <code>                    &quot;user_type&quot;: &quot;ADMIN&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 54 | <code>                    &quot;account_status&quot;: &quot;ACTIVE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 55 | <code>                    &quot;password&quot;: &quot;fixture-password&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 56 | <code>                }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 57 | <code>            ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `users` অংশে |
| 58 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 59 | <code>        with patch.object(app, &quot;include_router&quot;) as include:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 60 | <code>            register_auth_routes(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 61 | <code>                app, None, users, writes.append, database.quote, form_data, required</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 62 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 63 | <code>        router = include.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 64 | <code>        endpoint = next(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 65 | <code>            route.endpoint for route in router.routes if route.path == &quot;/api/auth/login&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 66 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 67 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 68 | <code>        async def receive():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 69 | <code>            return {</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `receive` অংশে |
| 70 | <code>                &quot;type&quot;: &quot;http.request&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `receive` অংশে |
| 71 | <code>                &quot;body&quot;: b&quot;username=admin&amp;password=fixture-password&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `receive` অংশে |
| 72 | <code>                &quot;more_body&quot;: False,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `receive` অংশে |
| 73 | <code>            }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `receive` অংশে |
| 74 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 75 | <code>        request = Request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 76 | <code>            {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 77 | <code>                &quot;type&quot;: &quot;http&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 78 | <code>                &quot;method&quot;: &quot;POST&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 79 | <code>                &quot;path&quot;: &quot;/api/auth/login&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 80 | <code>                &quot;scheme&quot;: &quot;http&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 81 | <code>                &quot;headers&quot;: [],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 82 | <code>                &quot;server&quot;: (&quot;localhost&quot;, 8091),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 83 | <code>                &quot;query_string&quot;: b&quot;&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 84 | <code>            },</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 85 | <code>            receive,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 86 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_upgrades_legacy_password` অংশে |
| 87 | <code>        response = asyncio.run(endpoint(request))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_upgrades_legacy_password` অংশে |
| 88 | <code>        self.assertEqual(response.status_code, 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 89 | <code>        self.assertIn(&quot;HttpOnly&quot;, response.headers[&quot;set-cookie&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 90 | <code>        self.assertIn(&quot;pbkdf2$&quot;, writes[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 91 | <code>        self.assertNotIn(&quot;password=&#x27;fixture-password&#x27;&quot;, writes[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 92 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 93 | <code>    def test_invalid_utf8_form_rejected(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 94 | <code>        async def body():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 95 | <code>            return b&quot;name=\xff&quot;</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `body` অংশে |
| 96 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 97 | <code>        with self.assertRaises(HTTPException) as error:</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 98 | <code>            asyncio.run(form_data(SimpleNamespace(body=body)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_utf8_form_rejected` অংশে |
| 99 | <code>        self.assertEqual(error.exception.status_code, 400)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 100 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 101 | <code>    def test_sessions_expire_and_invalidate(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 102 | <code>        token = create_session({&quot;user_id&quot;: 1, &quot;username&quot;: &quot;admin&quot;, &quot;user_type&quot;: &quot;ADMIN&quot;})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sessions_expire_and_invalidate` অংশে |
| 103 | <code>        request = SimpleNamespace(cookies={&quot;library_session&quot;: token})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sessions_expire_and_invalidate` অংশে |
| 104 | <code>        self.assertIsNotNone(current_session(request))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 105 | <code>        invalidate_user_sessions(1)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sessions_expire_and_invalidate` অংশে |
| 106 | <code>        self.assertIsNone(current_session(request))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 107 | <code>        token = create_session({&quot;user_id&quot;: 1, &quot;username&quot;: &quot;admin&quot;, &quot;user_type&quot;: &quot;ADMIN&quot;})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sessions_expire_and_invalidate` অংশে |
| 108 | <code>        SESSIONS[token][&quot;expires&quot;] = 0</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sessions_expire_and_invalidate` অংশে |
| 109 | <code>        self.assertIsNone(current_session(SimpleNamespace(cookies={&quot;library_session&quot;: token})))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 110 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 111 | <code>    def test_row_parser_fails_on_corrupt_records(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 112 | <code>        with patch.object(database, &quot;run_sql&quot;, return_value=&quot;1&#124;Clean Code&#124;5&quot;):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_row_parser_fails_on_corrupt_records` অংশে |
| 113 | <code>            self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 114 | <code>                database.rows(&quot;SELECT&quot;, [&quot;id&quot;, &quot;title&quot;, &quot;stock&quot;], {&quot;id&quot;, &quot;stock&quot;})[0][&quot;stock&quot;], 5</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `test_row_parser_fails_on_corrupt_records` অংশে |
| 115 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_row_parser_fails_on_corrupt_records` অংশে |
| 116 | <code>        with patch.object(database, &quot;run_sql&quot;, return_value=&quot;1&#124;unexpected&#124;delimiter&quot;):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_row_parser_fails_on_corrupt_records` অংশে |
| 117 | <code>            with self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 118 | <code>                database.rows(&quot;SELECT&quot;, [&quot;id&quot;, &quot;title&quot;])</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `test_row_parser_fails_on_corrupt_records` অংশে |
| 119 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 120 | <code>    def test_missing_fine_is_checked_in_transaction(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 121 | <code>        async def receive():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 122 | <code>            return {&quot;type&quot;: &quot;http.request&quot;, &quot;body&quot;: b&quot;&quot;, &quot;more_body&quot;: False}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `receive` অংশে |
| 123 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 124 | <code>        request = Request({&quot;type&quot;: &quot;http&quot;, &quot;method&quot;: &quot;POST&quot;, &quot;headers&quot;: []}, receive)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_missing_fine_is_checked_in_transaction` অংশে |
| 125 | <code>        with patch.object(fines, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_missing_fine_is_checked_in_transaction` অংশে |
| 126 | <code>            asyncio.run(main.pay_fine(123, request))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_missing_fine_is_checked_in_transaction` অংশে |
| 127 | <code>            self.assertIn(&quot;pay_fine_proc(123, NULL&quot;, run.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 128 | <code>            self.assertIn(&quot;COMMIT&quot;, run.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 129 | <code>        with self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 130 | <code>            asyncio.run(main.pay_fine(-1, request))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_missing_fine_is_checked_in_transaction` অংশে |
| 131 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 132 | <code>    def test_sqlplus_errors_are_mapped_and_rollback_enabled(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 133 | <code>        result = SimpleNamespace(stdout=&quot;ORA-20001: Book is not available&quot;, stderr=&quot;&quot;, returncode=1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sqlplus_errors_are_mapped_and_rollback_enabled` অংশে |
| 134 | <code>        with patch.object(database.subprocess, &quot;run&quot;, return_value=result) as run:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sqlplus_errors_are_mapped_and_rollback_enabled` অংশে |
| 135 | <code>            with self.assertRaises(HTTPException) as error:</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 136 | <code>                database.run_sql(&quot;SELECT 1 FROM dual;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_sqlplus_errors_are_mapped_and_rollback_enabled` অংশে |
| 137 | <code>            self.assertEqual(error.exception.status_code, 409)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 138 | <code>            self.assertIn(&quot;ROLLBACK&quot;, run.call_args.kwargs[&quot;input&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 139 | <code>            self.assertIn(&quot;SET DEFINE OFF&quot;, run.call_args.kwargs[&quot;input&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 140 | <code>            self.assertEqual(run.call_args.args[0][-1], &quot;/nolog&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 141 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 142 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 143 | <code>if __name__ == &quot;__main__&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। |
| 144 | <code>    unittest.main()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
