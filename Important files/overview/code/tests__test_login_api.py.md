# tests/test_login_api.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_login_api.py)। Snapshot 2026-10-04; 210 lines; SHA-256 `b21775cfc02f4f6b300bfcb0082169fbdf37490397ecf15c8efdd6c172500d2f`।

## Function / object / element inventory

### `setUpClass` — L24–L81

`def setUpClass(cls):`

Test/setup helper: setUpClass; নিচের assertions/calls সেই behavior define করে।

### `rows` — L32–L55

`def rows(sql, *args):`

SQL execute করে প্রতিটি nonblank line-কে | delimiter দিয়ে ভাগ করে keys-এর সঙ্গে মেলায়; ~ null marker এবং নির্দিষ্ট numeric fields decode করে। Unexpected field count হলে 502।

### `private` — L62–L63

`def private():`

Test/setup helper: private; নিচের assertions/calls সেই behavior define করে।

### `health` — L66–L67

`def health():`

dual-এ SELECT 1 চালিয়ে actual Oracle connectivity যাচাই করে CONNECTED metadata দেয়। এটি public endpoint।

### `tearDownClass` — L84–L88

`def tearDownClass(cls):`

Test/setup helper: tearDownClass; নিচের assertions/calls সেই behavior define করে।

### `setUp` — L90–L92

`def setUp(self):`

Test/setup helper: setUp; নিচের assertions/calls সেই behavior define করে।

### `request` — L94–L102

`def request(self, path, data=None, headers=None):`

Test/setup helper: request; নিচের assertions/calls সেই behavior define করে।

### `test_login_session_and_logout` — L104–L116

`def test_login_session_and_logout(self):`

Test/setup helper: test login session and logout; নিচের assertions/calls সেই behavior define করে।

### `test_wrong_password_disabled_and_student` — L118–L131

`def test_wrong_password_disabled_and_student(self):`

Test/setup helper: test wrong password disabled and student; নিচের assertions/calls সেই behavior define করে।

### `test_linked_student_can_login_but_cannot_access_management` — L133–L149

`def test_linked_student_can_login_but_cannot_access_management(self):`

Test/setup helper: test linked student can login but cannot access management; নিচের assertions/calls সেই behavior define করে।

### `test_invalid_and_duplicate_form_fields` — L151–L162

`def test_invalid_and_duplicate_form_fields(self):`

Test/setup helper: test invalid and duplicate form fields; নিচের assertions/calls সেই behavior define করে।

### `test_cross_origin_login_blocked` — L164–L172

`def test_cross_origin_login_blocked(self):`

Test/setup helper: test cross origin login blocked; নিচের assertions/calls সেই behavior define করে।

### `test_activation_is_public_and_cross_origin_changes_are_blocked` — L174–L183

`def test_activation_is_public_and_cross_origin_changes_are_blocked(self):`

Test/setup helper: test activation is public and cross origin changes are blocked; নিচের assertions/calls সেই behavior define করে।

### `test_slow_database_does_not_block_health` — L185–L206

`def test_slow_database_does_not_block_health(self):`

Test/setup helper: test slow database does not block health; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
"""Exercise the login API over HTTP without changing real Oracle records."""

import http.cookiejar
import json
import socket
import threading
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

import uvicorn
from fastapi import FastAPI
from backend.auth.routes import register_auth_routes
from backend.auth.session import SESSIONS, install_authentication
from backend.database import quote
from backend.validation import form_data, required


class LoginApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = FastAPI()
        install_authentication(cls.app)
        cls.writes = []
        cls.block_database = False
        cls.query_started = threading.Event()
        cls.release_query = threading.Event()

        def rows(sql, *args):
            if "SELECT membership_status FROM student" in sql:
                return [{"membership_status": "ACTIVE"}]
            if cls.block_database:
                cls.query_started.set()
                cls.release_query.wait(3)
            for name, role, status in (
                ("admin", "ADMIN", "ACTIVE"),
                ("disabled", "LIBRARIAN", "DISABLED"),
                ("student", "STUDENT", "ACTIVE"),
                ("linkedstudent", "STUDENT", "ACTIVE"),
            ):
                if f"LOWER('{name}')" in sql:
                    return [
                        {
                            "user_id": 1,
                            "username": name,
                            "user_type": role,
                            "account_status": status,
                            "password": "test1234",
                            "student_id": 17 if name == "linkedstudent" else None,
                        }
                    ]
            return []

        register_auth_routes(
            cls.app, Path("frontend"), rows, cls.writes.append, quote, form_data, required
        )

        @cls.app.get("/api/private")
        def private():
            return {"ok": True}

        @cls.app.get("/api/health")
        def health():
            return {"ok": True}

        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        cls.base = f"http://127.0.0.1:{listener.getsockname()[1]}"
        cls.server = uvicorn.Server(uvicorn.Config(cls.app, log_level="critical", lifespan="off"))
        cls.thread = threading.Thread(
            target=cls.server.run, kwargs={"sockets": [listener]}, daemon=True
        )
        cls.thread.start()
        deadline = time.monotonic() + 5
        while not cls.server.started and time.monotonic() < deadline:
            time.sleep(0.01)
        if not cls.server.started:
            raise RuntimeError("Test server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.release_query.set()
        cls.server.should_exit = True
        cls.thread.join(5)
        SESSIONS.clear()

    def setUp(self):
        SESSIONS.clear()
        self.client = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def request(self, path, data=None, headers=None):
        body = urlencode(data).encode() if isinstance(data, dict) else data
        request = Request(self.base + path, data=body, headers=headers or {})
        try:
            response = self.client.open(request, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.loads(response.read()), response.headers

    def test_login_session_and_logout(self):
        self.assertEqual(self.request("/api/private")[0], 401)
        status, data, headers = self.request(
            "/api/auth/login", {"username": " admin ", "password": "test1234"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(data["user_type"], "ADMIN")
        self.assertIn("HttpOnly", headers["Set-Cookie"])
        self.assertIn("SameSite=strict", headers["Set-Cookie"])
        self.assertEqual(self.request("/api/auth/session")[0], 200)
        self.assertEqual(self.request("/api/private")[0], 200)
        self.assertEqual(self.request("/api/auth/logout", b"")[0], 200)
        self.assertEqual(self.request("/api/private")[0], 401)

    def test_wrong_password_disabled_and_student(self):
        for username, password, status in (
            ("admin", "wrong", 401),
            ("missing", "test1234", 401),
            ("disabled", "test1234", 403),
            ("student", "test1234", 403),
        ):
            with self.subTest(username=username):
                self.assertEqual(
                    self.request("/api/auth/login", {"username": username, "password": password})[
                        0
                    ],
                    status,
                )

    def test_linked_student_can_login_but_cannot_access_management(self):
        status, data, _ = self.request(
            "/api/auth/login", {"username": "linkedstudent", "password": "test1234"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(data["user_type"], "STUDENT")
        self.assertEqual(self.request("/api/auth/session")[0], 200)
        for path, body in (
            ("/api/private", None),
            ("/api/snapshot", None),
            ("/api/students", None),
            ("/api/student-access", b""),
            ("/api/reservations/1/collect", b""),
            ("/api/books", b""),
        ):
            with self.subTest(path=path):
                self.assertEqual(self.request(path, body)[0], 403)

    def test_invalid_and_duplicate_form_fields(self):
        for body in (
            b"username=admin&username=student&password=test1234",
            b"username=%FF&password=test1234",
            b"username=%ZZ&password=test1234",
            b"username=%20&password=test1234",
        ):
            with self.subTest(body=body):
                self.assertEqual(self.request("/api/auth/login", body)[0], 400)
        self.assertEqual(
            self.request("/api/auth/login", {"username": "admin", "password": "x" * 129})[0], 400
        )

    def test_cross_origin_login_blocked(self):
        self.assertEqual(
            self.request(
                "/api/auth/login",
                {"username": "admin", "password": "test1234"},
                {"Origin": "https://example.invalid"},
            )[0],
            403,
        )

    def test_activation_is_public_and_cross_origin_changes_are_blocked(self):
        self.assertEqual(self.request("/api/auth/activate", {"memberId": "bad"})[0], 400)
        self.assertEqual(
            self.request("/api/auth/activate", {}, {"Origin": "https://example.invalid"})[0], 403
        )
        self.assertEqual(self.request("/api/auth/reset-password", {"memberId": "admin"})[0], 400)
        self.assertEqual(
            self.request("/api/auth/reset-password", {}, {"Origin": "https://example.invalid"})[0],
            403,
        )

    def test_slow_database_does_not_block_health(self):
        cls = type(self)
        cls.query_started.clear()
        cls.release_query.clear()
        cls.block_database = True
        worker = threading.Thread(
            target=lambda: self.request(
                "/api/auth/login", {"username": "admin", "password": "test1234"}
            )
        )
        try:
            worker.start()
            self.assertTrue(cls.query_started.wait(2))
            started = time.monotonic()
            response = build_opener().open(cls.base + "/api/health", timeout=1)
            with response:
                self.assertEqual(response.status, 200)
            self.assertLess(time.monotonic() - started, 1)
        finally:
            cls.block_database = False
            cls.release_query.set()
            worker.join(5)


if __name__ == "__main__":
    unittest.main()
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Exercise the login API over HTTP without changing real Oracle records.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import http.cookiejar</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import json</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>import socket</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>import threading</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>import time</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from pathlib import Path</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from urllib.error import HTTPError</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from urllib.parse import urlencode</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from urllib.request import HTTPCookieProcessor, Request, build_opener</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>import uvicorn</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 15 | <code>from fastapi import FastAPI</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 16 | <code>from backend.auth.routes import register_auth_routes</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 17 | <code>from backend.auth.session import SESSIONS, install_authentication</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 18 | <code>from backend.database import quote</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 19 | <code>from backend.validation import form_data, required</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 20 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 21 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 22 | <code>class LoginApiTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 23 | <code>    @classmethod</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 24 | <code>    def setUpClass(cls):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 25 | <code>        cls.app = FastAPI()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 26 | <code>        install_authentication(cls.app)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 27 | <code>        cls.writes = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 28 | <code>        cls.block_database = False</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 29 | <code>        cls.query_started = threading.Event()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 30 | <code>        cls.release_query = threading.Event()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>        def rows(sql, *args):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 33 | <code>            if &quot;SELECT membership_status FROM student&quot; in sql:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `rows` অংশে |
| 34 | <code>                return [{&quot;membership_status&quot;: &quot;ACTIVE&quot;}]</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `rows` অংশে |
| 35 | <code>            if cls.block_database:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `rows` অংশে |
| 36 | <code>                cls.query_started.set()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 37 | <code>                cls.release_query.wait(3)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 38 | <code>            for name, role, status in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `rows` অংশে |
| 39 | <code>                (&quot;admin&quot;, &quot;ADMIN&quot;, &quot;ACTIVE&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 40 | <code>                (&quot;disabled&quot;, &quot;LIBRARIAN&quot;, &quot;DISABLED&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 41 | <code>                (&quot;student&quot;, &quot;STUDENT&quot;, &quot;ACTIVE&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 42 | <code>                (&quot;linkedstudent&quot;, &quot;STUDENT&quot;, &quot;ACTIVE&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 43 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 44 | <code>                if f&quot;LOWER(&#x27;{name}&#x27;)&quot; in sql:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `rows` অংশে |
| 45 | <code>                    return [</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `rows` অংশে |
| 46 | <code>                        {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 47 | <code>                            &quot;user_id&quot;: 1,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 48 | <code>                            &quot;username&quot;: name,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 49 | <code>                            &quot;user_type&quot;: role,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 50 | <code>                            &quot;account_status&quot;: status,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 51 | <code>                            &quot;password&quot;: &quot;test1234&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 52 | <code>                            &quot;student_id&quot;: 17 if name == &quot;linkedstudent&quot; else None,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `rows` অংশে |
| 53 | <code>                        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 54 | <code>                    ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 55 | <code>            return []</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `rows` অংশে |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>        register_auth_routes(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 58 | <code>            cls.app, Path(&quot;frontend&quot;), rows, cls.writes.append, quote, form_data, required</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 59 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 60 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 61 | <code>        @cls.app.get(&quot;/api/private&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 62 | <code>        def private():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 63 | <code>            return {&quot;ok&quot;: True}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `private` অংশে |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>        @cls.app.get(&quot;/api/health&quot;)</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 66 | <code>        def health():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 67 | <code>            return {&quot;ok&quot;: True}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `health` অংশে |
| 68 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 69 | <code>        listener = socket.socket()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 70 | <code>        listener.bind((&quot;127.0.0.1&quot;, 0))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 71 | <code>        cls.base = f&quot;http://127.0.0.1:{listener.getsockname()[1]}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 72 | <code>        cls.server = uvicorn.Server(uvicorn.Config(cls.app, log_level=&quot;critical&quot;, lifespan=&quot;off&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 73 | <code>        cls.thread = threading.Thread(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 74 | <code>            target=cls.server.run, kwargs={&quot;sockets&quot;: [listener]}, daemon=True</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 75 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 76 | <code>        cls.thread.start()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 77 | <code>        deadline = time.monotonic() + 5</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUpClass` অংশে |
| 78 | <code>        while not cls.server.started and time.monotonic() &lt; deadline:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `setUpClass` অংশে |
| 79 | <code>            time.sleep(0.01)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUpClass` অংশে |
| 80 | <code>        if not cls.server.started:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `setUpClass` অংশে |
| 81 | <code>            raise RuntimeError(&quot;Test server did not start&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `setUpClass` অংশে |
| 82 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 83 | <code>    @classmethod</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 84 | <code>    def tearDownClass(cls):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 85 | <code>        cls.release_query.set()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `tearDownClass` অংশে |
| 86 | <code>        cls.server.should_exit = True</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `tearDownClass` অংশে |
| 87 | <code>        cls.thread.join(5)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `tearDownClass` অংশে |
| 88 | <code>        SESSIONS.clear()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `tearDownClass` অংশে |
| 89 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 90 | <code>    def setUp(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 91 | <code>        SESSIONS.clear()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 92 | <code>        self.client = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 93 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 94 | <code>    def request(self, path, data=None, headers=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 95 | <code>        body = urlencode(data).encode() if isinstance(data, dict) else data</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `request` অংশে |
| 96 | <code>        request = Request(self.base + path, data=body, headers=headers or {})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `request` অংশে |
| 97 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `request` অংশে |
| 98 | <code>            response = self.client.open(request, timeout=5)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `request` অংশে |
| 99 | <code>        except HTTPError as error:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `request` অংশে |
| 100 | <code>            response = error</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `request` অংশে |
| 101 | <code>        with response:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 102 | <code>            return response.status, json.loads(response.read()), response.headers</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `request` অংশে |
| 103 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 104 | <code>    def test_login_session_and_logout(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 105 | <code>        self.assertEqual(self.request(&quot;/api/private&quot;)[0], 401)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 106 | <code>        status, data, headers = self.request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_login_session_and_logout` অংশে |
| 107 | <code>            &quot;/api/auth/login&quot;, {&quot;username&quot;: &quot; admin &quot;, &quot;password&quot;: &quot;test1234&quot;}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_session_and_logout` অংশে |
| 108 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_login_session_and_logout` অংশে |
| 109 | <code>        self.assertEqual(status, 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 110 | <code>        self.assertEqual(data[&quot;user_type&quot;], &quot;ADMIN&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 111 | <code>        self.assertIn(&quot;HttpOnly&quot;, headers[&quot;Set-Cookie&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 112 | <code>        self.assertIn(&quot;SameSite=strict&quot;, headers[&quot;Set-Cookie&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 113 | <code>        self.assertEqual(self.request(&quot;/api/auth/session&quot;)[0], 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 114 | <code>        self.assertEqual(self.request(&quot;/api/private&quot;)[0], 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 115 | <code>        self.assertEqual(self.request(&quot;/api/auth/logout&quot;, b&quot;&quot;)[0], 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 116 | <code>        self.assertEqual(self.request(&quot;/api/private&quot;)[0], 401)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 117 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 118 | <code>    def test_wrong_password_disabled_and_student(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 119 | <code>        for username, password, status in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_wrong_password_disabled_and_student` অংশে |
| 120 | <code>            (&quot;admin&quot;, &quot;wrong&quot;, 401),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 121 | <code>            (&quot;missing&quot;, &quot;test1234&quot;, 401),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 122 | <code>            (&quot;disabled&quot;, &quot;test1234&quot;, 403),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 123 | <code>            (&quot;student&quot;, &quot;test1234&quot;, 403),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 124 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 125 | <code>            with self.subTest(username=username):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_wrong_password_disabled_and_student` অংশে |
| 126 | <code>                self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 127 | <code>                    self.request(&quot;/api/auth/login&quot;, {&quot;username&quot;: username, &quot;password&quot;: password})[</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 128 | <code>                        0</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 129 | <code>                    ],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 130 | <code>                    status,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 131 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_wrong_password_disabled_and_student` অংশে |
| 132 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 133 | <code>    def test_linked_student_can_login_but_cannot_access_management(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 134 | <code>        status, data, _ = self.request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 135 | <code>            &quot;/api/auth/login&quot;, {&quot;username&quot;: &quot;linkedstudent&quot;, &quot;password&quot;: &quot;test1234&quot;}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 136 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 137 | <code>        self.assertEqual(status, 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 138 | <code>        self.assertEqual(data[&quot;user_type&quot;], &quot;STUDENT&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 139 | <code>        self.assertEqual(self.request(&quot;/api/auth/session&quot;)[0], 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 140 | <code>        for path, body in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 141 | <code>            (&quot;/api/private&quot;, None),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 142 | <code>            (&quot;/api/snapshot&quot;, None),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 143 | <code>            (&quot;/api/students&quot;, None),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 144 | <code>            (&quot;/api/student-access&quot;, b&quot;&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 145 | <code>            (&quot;/api/reservations/1/collect&quot;, b&quot;&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 146 | <code>            (&quot;/api/books&quot;, b&quot;&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 147 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 148 | <code>            with self.subTest(path=path):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_linked_student_can_login_but_cannot_access_management` অংশে |
| 149 | <code>                self.assertEqual(self.request(path, body)[0], 403)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 150 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 151 | <code>    def test_invalid_and_duplicate_form_fields(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 152 | <code>        for body in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_invalid_and_duplicate_form_fields` অংশে |
| 153 | <code>            b&quot;username=admin&amp;username=student&amp;password=test1234&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_and_duplicate_form_fields` অংশে |
| 154 | <code>            b&quot;username=%FF&amp;password=test1234&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_and_duplicate_form_fields` অংশে |
| 155 | <code>            b&quot;username=%ZZ&amp;password=test1234&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_and_duplicate_form_fields` অংশে |
| 156 | <code>            b&quot;username=%20&amp;password=test1234&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_and_duplicate_form_fields` অংশে |
| 157 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_and_duplicate_form_fields` অংশে |
| 158 | <code>            with self.subTest(body=body):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_and_duplicate_form_fields` অংশে |
| 159 | <code>                self.assertEqual(self.request(&quot;/api/auth/login&quot;, body)[0], 400)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 160 | <code>        self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 161 | <code>            self.request(&quot;/api/auth/login&quot;, {&quot;username&quot;: &quot;admin&quot;, &quot;password&quot;: &quot;x&quot; * 129})[0], 400</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_and_duplicate_form_fields` অংশে |
| 162 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_invalid_and_duplicate_form_fields` অংশে |
| 163 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 164 | <code>    def test_cross_origin_login_blocked(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 165 | <code>        self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 166 | <code>            self.request(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 167 | <code>                &quot;/api/auth/login&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 168 | <code>                {&quot;username&quot;: &quot;admin&quot;, &quot;password&quot;: &quot;test1234&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 169 | <code>                {&quot;Origin&quot;: &quot;https://example.invalid&quot;},</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 170 | <code>            )[0],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 171 | <code>            403,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 172 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_cross_origin_login_blocked` অংশে |
| 173 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 174 | <code>    def test_activation_is_public_and_cross_origin_changes_are_blocked(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 175 | <code>        self.assertEqual(self.request(&quot;/api/auth/activate&quot;, {&quot;memberId&quot;: &quot;bad&quot;})[0], 400)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 176 | <code>        self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 177 | <code>            self.request(&quot;/api/auth/activate&quot;, {}, {&quot;Origin&quot;: &quot;https://example.invalid&quot;})[0], 403</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_is_public_and_cross_origin_changes_are_blocked` অংশে |
| 178 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_is_public_and_cross_origin_changes_are_blocked` অংশে |
| 179 | <code>        self.assertEqual(self.request(&quot;/api/auth/reset-password&quot;, {&quot;memberId&quot;: &quot;admin&quot;})[0], 400)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 180 | <code>        self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 181 | <code>            self.request(&quot;/api/auth/reset-password&quot;, {}, {&quot;Origin&quot;: &quot;https://example.invalid&quot;})[0],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_is_public_and_cross_origin_changes_are_blocked` অংশে |
| 182 | <code>            403,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_is_public_and_cross_origin_changes_are_blocked` অংশে |
| 183 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_activation_is_public_and_cross_origin_changes_are_blocked` অংশে |
| 184 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 185 | <code>    def test_slow_database_does_not_block_health(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 186 | <code>        cls = type(self)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 187 | <code>        cls.query_started.clear()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 188 | <code>        cls.release_query.clear()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 189 | <code>        cls.block_database = True</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 190 | <code>        worker = threading.Thread(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 191 | <code>            target=lambda: self.request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 192 | <code>                &quot;/api/auth/login&quot;, {&quot;username&quot;: &quot;admin&quot;, &quot;password&quot;: &quot;test1234&quot;}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 193 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 194 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 195 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_slow_database_does_not_block_health` অংশে |
| 196 | <code>            worker.start()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 197 | <code>            self.assertTrue(cls.query_started.wait(2))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 198 | <code>            started = time.monotonic()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 199 | <code>            response = build_opener().open(cls.base + &quot;/api/health&quot;, timeout=1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 200 | <code>            with response:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 201 | <code>                self.assertEqual(response.status, 200)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 202 | <code>            self.assertLess(time.monotonic() - started, 1)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 203 | <code>        finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_slow_database_does_not_block_health` অংশে |
| 204 | <code>            cls.block_database = False</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_slow_database_does_not_block_health` অংশে |
| 205 | <code>            cls.release_query.set()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 206 | <code>            worker.join(5)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_slow_database_does_not_block_health` অংশে |
| 207 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 208 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 209 | <code>if __name__ == &quot;__main__&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। |
| 210 | <code>    unittest.main()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
