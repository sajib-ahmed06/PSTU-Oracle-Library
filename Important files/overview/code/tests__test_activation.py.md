# tests/test_activation.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_activation.py)। Snapshot 2026-10-04; 192 lines; SHA-256 `a782902b4e4be629f3cf122c0745ca1a6e430e997e055430b880897c188856e0`।

## Function / object / element inventory

### `request` — L17–L31

`def request(fields):`

Test/setup helper: request; নিচের assertions/calls সেই behavior define করে।

### `receive` — L18–L19

`async def receive():`

Test/setup helper: receive; নিচের assertions/calls সেই behavior define করে।

### `setUp` — L35–L55

`def setUp(self):`

Test/setup helper: setUp; নিচের assertions/calls সেই behavior define করে।

### `test_member_id_parsing_preserves_library_identity` — L57–L62

`def test_member_id_parsing_preserves_library_identity(self):`

Test/setup helper: test member id parsing preserves library identity; নিচের assertions/calls সেই behavior define করে।

### `test_activation_uses_hash_and_atomic_database_procedure` — L64–L77

`def test_activation_uses_hash_and_atomic_database_procedure(self):`

Test/setup helper: test activation uses hash and atomic database procedure; নিচের assertions/calls সেই behavior define করে।

### `test_invalid_fields_never_reach_database` — L79–L94

`def test_invalid_fields_never_reach_database(self):`

Test/setup helper: test invalid fields never reach database; নিচের assertions/calls সেই behavior define করে।

### `test_member_id_login_queries_linked_student_and_redirect_role` — L96–L123

`def test_member_id_login_queries_linked_student_and_redirect_role(self):`

Test/setup helper: test member id login queries linked student and redirect role; নিচের assertions/calls সেই behavior define করে।

### `test_recovery_requires_every_registered_detail_and_hashes_password` — L125–L149

`def test_recovery_requires_every_registered_detail_and_hashes_password(self):`

Test/setup helper: test recovery requires every registered detail and hashes password; নিচের assertions/calls সেই behavior define করে।

### `test_recovery_rejects_staff_username_and_invalid_email` — L151–L169

`def test_recovery_rejects_staff_username_and_invalid_email(self):`

Test/setup helper: test recovery rejects staff username and invalid email; নিচের assertions/calls সেই behavior define করে।

### `test_recovery_invalidates_only_the_members_sessions` — L171–L192

`def test_recovery_invalidates_only_the_members_sessions(self):`

Test/setup helper: test recovery invalidates only the members sessions; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import asyncio
import unittest
from unittest.mock import patch
from urllib.parse import urlencode
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock

from fastapi import HTTPException
from starlette.requests import Request
from backend.auth.routes import member_number, register_auth_routes
from backend.auth.passwords import verify_password
from backend.database import quote
from backend.validation import form_data, required


def request(fields):
    async def receive():
        return {"type": "http.request", "body": urlencode(fields).encode(), "more_body": False}

    return Request(
        {
            "type": "http",
            "method": "POST",
            "scheme": "http",
            "path": "/api/auth/login",
            "server": ("localhost", 8091),
            "headers": [],
        },
        receive,
    )


class ActivationTests(unittest.TestCase):
    def setUp(self):
        routes = []
        self.rows = Mock(return_value=[])
        register_auth_routes(
            SimpleNamespace(include_router=lambda router: routes.extend(router.routes)),
            Path("frontend"),
            self.rows,
            Mock(),
            quote,
            form_data,
            required,
        )
        self.activate = next(r.endpoint for r in routes if r.path == "/api/auth/activate")
        self.login = next(r.endpoint for r in routes if r.path == "/api/auth/login")
        self.reset = next(r.endpoint for r in routes if r.path == "/api/auth/reset-password")
        self.fields = {
            "memberId": "pstu-0007",
            "phone": "01700000007",
            "password": "Secret1234",
            "confirmPassword": "Secret1234",
        }

    def test_member_id_parsing_preserves_library_identity(self):
        for value in ("PSTU-0007", "pstu-7", "0007", " 7 "):
            self.assertEqual(member_number(value), 7)
        for value in ("PSTU-0000", "-7", "roll-7", "7 OR 1=1", "7.0", ""):
            with self.subTest(value=value), self.assertRaises(HTTPException):
                member_number(value)

    def test_activation_uses_hash_and_atomic_database_procedure(self):
        from backend.auth.passwords import hash_password

        password_hash = hash_password(self.fields["password"])
        with (
            patch("backend.auth.member_access.run_sql") as run,
            patch("backend.auth.member_access.hash_password", return_value=password_hash),
        ):
            result = asyncio.run(self.activate(request(self.fields)))
        sql = run.call_args.args[0]
        self.assertIn("activate_student_proc(7,'01700000007','pbkdf2$", sql)
        self.assertNotIn("Secret1234", sql)
        self.assertTrue(verify_password(self.fields["password"], password_hash))
        self.assertEqual(result["member_id"], "PSTU-0007")

    def test_invalid_fields_never_reach_database(self):
        for field, value in (
            ("phone", "1700000007"),
            ("phone", "0170000000x"),
            ("memberId", "PSTU-0"),
            ("password", "123"),
            ("confirmPassword", "Different"),
        ):
            data = {**self.fields, field: value}
            with (
                self.subTest(field=field, value=value),
                patch("backend.auth.member_access.run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(self.activate(request(data)))
            run.assert_not_called()

    def test_member_id_login_queries_linked_student_and_redirect_role(self):
        from backend.auth.passwords import hash_password
        from backend.auth.session import SESSIONS, remove_session

        self.rows.side_effect = [
            [
                {
                    "user_id": 907,
                    "username": "PSTU-0007",
                    "user_type": "STUDENT",
                    "account_status": "ACTIVE",
                    "student_id": 7,
                    "password": hash_password("Secret1234"),
                }
            ],
            [{"membership_status": "ACTIVE"}],
        ]
        try:
            response = asyncio.run(
                self.login(request({"username": "pstu-0007", "password": "Secret1234"}))
            )
            self.assertEqual(response.status_code, 200)
            sql = self.rows.call_args_list[0].args[0]
            self.assertIn("student_id=7 AND user_type='STUDENT'", sql)
        finally:
            for token, session in list(SESSIONS.items()):
                if session["user_id"] == 907:
                    remove_session(token)

    def test_recovery_requires_every_registered_detail_and_hashes_password(self):
        fields = {
            **self.fields,
            "rollNo": " 007 ",
            "registrationNo": "reg-007",
            "email": "Member@Example.com",
        }
        with patch("backend.auth.member_access.run_sql") as run:
            result = asyncio.run(self.reset(request(fields)))
        sql = run.call_args.args[0]
        self.assertIn(
            "reset_student_password_proc(7,'007','REG-007','01700000007','member@example.com','pbkdf2$",
            sql,
        )
        self.assertNotIn("Secret1234", sql)
        self.assertEqual(result["member_id"], "PSTU-0007")
        for key in fields:
            missing = {k: v for k, v in fields.items() if k != key}
            with (
                self.subTest(key=key),
                patch("backend.auth.member_access.run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(self.reset(request(missing)))
            run.assert_not_called()

    def test_recovery_rejects_staff_username_and_invalid_email(self):
        fields = {
            **self.fields,
            "rollNo": "007",
            "registrationNo": "REG-007",
            "email": "member@example.com",
        }
        for key, value in (
            ("memberId", "admin"),
            ("email", "bad-email"),
            ("confirmPassword", "different"),
        ):
            with (
                self.subTest(key=key),
                patch("backend.auth.member_access.run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(self.reset(request({**fields, key: value})))
            run.assert_not_called()

    def test_recovery_invalidates_only_the_members_sessions(self):
        from backend.auth.session import create_session, SESSIONS, remove_session

        member_token = create_session(
            {"user_id": 907, "username": "PSTU-0007", "user_type": "STUDENT", "student_id": 7}
        )
        staff_token = create_session({"user_id": 908, "username": "adminqa", "user_type": "ADMIN"})
        self.rows.return_value = [{"user_id": 907}]
        try:
            fields = {
                **self.fields,
                "rollNo": "007",
                "registrationNo": "REG-007",
                "email": "member@example.com",
            }
            with patch("backend.auth.member_access.run_sql"):
                asyncio.run(self.reset(request(fields)))
            self.assertNotIn(member_token, SESSIONS)
            self.assertIn(staff_token, SESSIONS)
        finally:
            remove_session(member_token)
            remove_session(staff_token)
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import asyncio</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from urllib.parse import urlencode</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from types import SimpleNamespace</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from pathlib import Path</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from unittest.mock import Mock</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from starlette.requests import Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from backend.auth.routes import member_number, register_auth_routes</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from backend.auth.passwords import verify_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>from backend.database import quote</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 14 | <code>from backend.validation import form_data, required</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>def request(fields):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 18 | <code>    async def receive():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 19 | <code>        return {&quot;type&quot;: &quot;http.request&quot;, &quot;body&quot;: urlencode(fields).encode(), &quot;more_body&quot;: False}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `receive` অংশে |
| 20 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 21 | <code>    return Request(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `request` অংশে |
| 22 | <code>        {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 23 | <code>            &quot;type&quot;: &quot;http&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 24 | <code>            &quot;method&quot;: &quot;POST&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 25 | <code>            &quot;scheme&quot;: &quot;http&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 26 | <code>            &quot;path&quot;: &quot;/api/auth/login&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 27 | <code>            &quot;server&quot;: (&quot;localhost&quot;, 8091),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 28 | <code>            &quot;headers&quot;: [],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 29 | <code>        },</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 30 | <code>        receive,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 31 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 34 | <code>class ActivationTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 35 | <code>    def setUp(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 36 | <code>        routes = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 37 | <code>        self.rows = Mock(return_value=[])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 38 | <code>        register_auth_routes(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 39 | <code>            SimpleNamespace(include_router=lambda router: routes.extend(router.routes)),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 40 | <code>            Path(&quot;frontend&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 41 | <code>            self.rows,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 42 | <code>            Mock(),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 43 | <code>            quote,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 44 | <code>            form_data,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 45 | <code>            required,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 46 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 47 | <code>        self.activate = next(r.endpoint for r in routes if r.path == &quot;/api/auth/activate&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 48 | <code>        self.login = next(r.endpoint for r in routes if r.path == &quot;/api/auth/login&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 49 | <code>        self.reset = next(r.endpoint for r in routes if r.path == &quot;/api/auth/reset-password&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 50 | <code>        self.fields = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 51 | <code>            &quot;memberId&quot;: &quot;pstu-0007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 52 | <code>            &quot;phone&quot;: &quot;01700000007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 53 | <code>            &quot;password&quot;: &quot;Secret1234&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 54 | <code>            &quot;confirmPassword&quot;: &quot;Secret1234&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 55 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>    def test_member_id_parsing_preserves_library_identity(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 58 | <code>        for value in (&quot;PSTU-0007&quot;, &quot;pstu-7&quot;, &quot;0007&quot;, &quot; 7 &quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_member_id_parsing_preserves_library_identity` অংশে |
| 59 | <code>            self.assertEqual(member_number(value), 7)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 60 | <code>        for value in (&quot;PSTU-0000&quot;, &quot;-7&quot;, &quot;roll-7&quot;, &quot;7 OR 1=1&quot;, &quot;7.0&quot;, &quot;&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_member_id_parsing_preserves_library_identity` অংশে |
| 61 | <code>            with self.subTest(value=value), self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 62 | <code>                member_number(value)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_parsing_preserves_library_identity` অংশে |
| 63 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 64 | <code>    def test_activation_uses_hash_and_atomic_database_procedure(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 65 | <code>        from backend.auth.passwords import hash_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 66 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 67 | <code>        password_hash = hash_password(self.fields[&quot;password&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 68 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 69 | <code>            patch(&quot;backend.auth.member_access.run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 70 | <code>            patch(&quot;backend.auth.member_access.hash_password&quot;, return_value=password_hash),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 71 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 72 | <code>            result = asyncio.run(self.activate(request(self.fields)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 73 | <code>        sql = run.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_activation_uses_hash_and_atomic_database_procedure` অংশে |
| 74 | <code>        self.assertIn(&quot;activate_student_proc(7,&#x27;01700000007&#x27;,&#x27;pbkdf2$&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 75 | <code>        self.assertNotIn(&quot;Secret1234&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 76 | <code>        self.assertTrue(verify_password(self.fields[&quot;password&quot;], password_hash))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 77 | <code>        self.assertEqual(result[&quot;member_id&quot;], &quot;PSTU-0007&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 78 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 79 | <code>    def test_invalid_fields_never_reach_database(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 80 | <code>        for field, value in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_invalid_fields_never_reach_database` অংশে |
| 81 | <code>            (&quot;phone&quot;, &quot;1700000007&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 82 | <code>            (&quot;phone&quot;, &quot;0170000000x&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 83 | <code>            (&quot;memberId&quot;, &quot;PSTU-0&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 84 | <code>            (&quot;password&quot;, &quot;123&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 85 | <code>            (&quot;confirmPassword&quot;, &quot;Different&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 86 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 87 | <code>            data = {**self.fields, field: value}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_fields_never_reach_database` অংশে |
| 88 | <code>            with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 89 | <code>                self.subTest(field=field, value=value),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_fields_never_reach_database` অংশে |
| 90 | <code>                patch(&quot;backend.auth.member_access.run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 91 | <code>                self.assertRaises(HTTPException),</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 92 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 93 | <code>                asyncio.run(self.activate(request(data)))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_fields_never_reach_database` অংশে |
| 94 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 95 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 96 | <code>    def test_member_id_login_queries_linked_student_and_redirect_role(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 97 | <code>        from backend.auth.passwords import hash_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 98 | <code>        from backend.auth.session import SESSIONS, remove_session</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 99 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 100 | <code>        self.rows.side_effect = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 101 | <code>            [</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 102 | <code>                {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 103 | <code>                    &quot;user_id&quot;: 907,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 104 | <code>                    &quot;username&quot;: &quot;PSTU-0007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 105 | <code>                    &quot;user_type&quot;: &quot;STUDENT&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 106 | <code>                    &quot;account_status&quot;: &quot;ACTIVE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 107 | <code>                    &quot;student_id&quot;: 7,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 108 | <code>                    &quot;password&quot;: hash_password(&quot;Secret1234&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 109 | <code>                }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 110 | <code>            ],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 111 | <code>            [{&quot;membership_status&quot;: &quot;ACTIVE&quot;}],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 112 | <code>        ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 113 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 114 | <code>            response = asyncio.run(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 115 | <code>                self.login(request({&quot;username&quot;: &quot;pstu-0007&quot;, &quot;password&quot;: &quot;Secret1234&quot;}))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 116 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 117 | <code>            self.assertEqual(response.status_code, 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 118 | <code>            sql = self.rows.call_args_list[0].args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 119 | <code>            self.assertIn(&quot;student_id=7 AND user_type=&#x27;STUDENT&#x27;&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 120 | <code>        finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 121 | <code>            for token, session in list(SESSIONS.items()):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 122 | <code>                if session[&quot;user_id&quot;] == 907:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 123 | <code>                    remove_session(token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_id_login_queries_linked_student_and_redirect_role` অংশে |
| 124 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 125 | <code>    def test_recovery_requires_every_registered_detail_and_hashes_password(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 126 | <code>        fields = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 127 | <code>            **self.fields,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 128 | <code>            &quot;rollNo&quot;: &quot; 007 &quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 129 | <code>            &quot;registrationNo&quot;: &quot;reg-007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 130 | <code>            &quot;email&quot;: &quot;Member@Example.com&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 131 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 132 | <code>        with patch(&quot;backend.auth.member_access.run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 133 | <code>            result = asyncio.run(self.reset(request(fields)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 134 | <code>        sql = run.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 135 | <code>        self.assertIn(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 136 | <code>            &quot;reset_student_password_proc(7,&#x27;007&#x27;,&#x27;REG-007&#x27;,&#x27;01700000007&#x27;,&#x27;member@example.com&#x27;,&#x27;pbkdf2$&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 137 | <code>            sql,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 138 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 139 | <code>        self.assertNotIn(&quot;Secret1234&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 140 | <code>        self.assertEqual(result[&quot;member_id&quot;], &quot;PSTU-0007&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 141 | <code>        for key in fields:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 142 | <code>            missing = {k: v for k, v in fields.items() if k != key}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 143 | <code>            with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 144 | <code>                self.subTest(key=key),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 145 | <code>                patch(&quot;backend.auth.member_access.run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 146 | <code>                self.assertRaises(HTTPException),</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 147 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 148 | <code>                asyncio.run(self.reset(request(missing)))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_requires_every_registered_detail_and_hashes_password` অংশে |
| 149 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 150 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 151 | <code>    def test_recovery_rejects_staff_username_and_invalid_email(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 152 | <code>        fields = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 153 | <code>            **self.fields,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 154 | <code>            &quot;rollNo&quot;: &quot;007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 155 | <code>            &quot;registrationNo&quot;: &quot;REG-007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 156 | <code>            &quot;email&quot;: &quot;member@example.com&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 157 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 158 | <code>        for key, value in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 159 | <code>            (&quot;memberId&quot;, &quot;admin&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 160 | <code>            (&quot;email&quot;, &quot;bad-email&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 161 | <code>            (&quot;confirmPassword&quot;, &quot;different&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 162 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 163 | <code>            with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 164 | <code>                self.subTest(key=key),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 165 | <code>                patch(&quot;backend.auth.member_access.run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 166 | <code>                self.assertRaises(HTTPException),</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 167 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 168 | <code>                asyncio.run(self.reset(request({**fields, key: value})))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_rejects_staff_username_and_invalid_email` অংশে |
| 169 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 170 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 171 | <code>    def test_recovery_invalidates_only_the_members_sessions(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 172 | <code>        from backend.auth.session import create_session, SESSIONS, remove_session</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 173 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 174 | <code>        member_token = create_session(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 175 | <code>            {&quot;user_id&quot;: 907, &quot;username&quot;: &quot;PSTU-0007&quot;, &quot;user_type&quot;: &quot;STUDENT&quot;, &quot;student_id&quot;: 7}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 176 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 177 | <code>        staff_token = create_session({&quot;user_id&quot;: 908, &quot;username&quot;: &quot;adminqa&quot;, &quot;user_type&quot;: &quot;ADMIN&quot;})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 178 | <code>        self.rows.return_value = [{&quot;user_id&quot;: 907}]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 179 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 180 | <code>            fields = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 181 | <code>                **self.fields,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 182 | <code>                &quot;rollNo&quot;: &quot;007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 183 | <code>                &quot;registrationNo&quot;: &quot;REG-007&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 184 | <code>                &quot;email&quot;: &quot;member@example.com&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 185 | <code>            }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 186 | <code>            with patch(&quot;backend.auth.member_access.run_sql&quot;):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 187 | <code>                asyncio.run(self.reset(request(fields)))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 188 | <code>            self.assertNotIn(member_token, SESSIONS)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 189 | <code>            self.assertIn(staff_token, SESSIONS)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 190 | <code>        finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 191 | <code>            remove_session(member_token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
| 192 | <code>            remove_session(staff_token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_recovery_invalidates_only_the_members_sessions` অংশে |
