# tests/test_reservations.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_reservations.py)। Snapshot 2026-10-04; 94 lines; SHA-256 `3874c003fcff8e69fef6cc31bcc5fabb4eb88530839c673af4e55485accfdf51`।

## Function / object / element inventory

### `setUp` — L12–L15

`def setUp(self):`

Test/setup helper: setUp; নিচের assertions/calls সেই behavior define করে।

### `tearDown` — L17–L18

`def tearDown(self):`

Test/setup helper: tearDown; নিচের assertions/calls সেই behavior define করে।

### `request` — L20–L31

`def request(self, body=""):`

Test/setup helper: request; নিচের assertions/calls সেই behavior define করে।

### `receive` — L21–L22

`async def receive():`

Test/setup helper: receive; নিচের assertions/calls সেই behavior define করে।

### `endpoint` — L33–L38

`def endpoint(self, path, method=None):`

Test/setup helper: endpoint; নিচের assertions/calls সেই behavior define করে।

### `test_student_cannot_reserve_for_another_member` — L40–L48

`def test_student_cannot_reserve_for_another_member(self):`

Test/setup helper: test student cannot reserve for another member; নিচের assertions/calls সেই behavior define করে।

### `test_student_cancellation_checks_owner_in_sql` — L50–L58

`def test_student_cancellation_checks_owner_in_sql(self):`

Test/setup helper: test student cancellation checks owner in sql; নিচের assertions/calls সেই behavior define করে।

### `test_student_cannot_collect` — L60–L71

`def test_student_cannot_collect(self):`

Test/setup helper: test student cannot collect; নিচের assertions/calls সেই behavior define করে।

### `test_disabled_membership_blocks_student_data` — L73–L79

`def test_disabled_membership_blocks_student_data(self):`

Test/setup helper: test disabled membership blocks student data; নিচের assertions/calls সেই behavior define করে।

### `test_dashboard_queries_scope_loans_and_fines_before_execution` — L81–L94

`def test_dashboard_queries_scope_loans_and_fines_before_execution(self):`

Test/setup helper: test dashboard queries scope loans and fines before execution; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import asyncio
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from starlette.requests import Request
from backend import main, reservations
from backend.auth.session import create_session, remove_session, SESSION_COOKIE


class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.token = create_session(
            {"user_id": 500, "username": "studentqa", "user_type": "STUDENT", "student_id": 17}
        )

    def tearDown(self):
        remove_session(self.token)

    def request(self, body=""):
        async def receive():
            return {"type": "http.request", "body": body.encode(), "more_body": False}

        return Request(
            {
                "type": "http",
                "method": "POST",
                "headers": [(b"cookie", f"{SESSION_COOKIE}={self.token}".encode())],
            },
            receive,
        )

    def endpoint(self, path, method=None):
        return next(
            route.endpoint
            for route in main.app.routes
            if getattr(route, "path", None) == path and (method is None or method in route.methods)
        )

    def test_student_cannot_reserve_for_another_member(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "ACTIVE"}]),
            patch.object(reservations, "run_sql") as run,
        ):
            asyncio.run(
                self.endpoint("/api/reservations", "POST")(self.request("bookId=4&studentId=99"))
            )
        self.assertIn("reserve_book_proc(17,4)", run.call_args.args[0])

    def test_student_cancellation_checks_owner_in_sql(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "ACTIVE"}]),
            patch.object(reservations, "run_sql") as run,
        ):
            asyncio.run(
                self.endpoint("/api/reservations/{reservation_id}/cancel")(88, self.request())
            )
        self.assertEqual(run.call_args.args[0].count("AND student_id=17"), 2)

    def test_student_cannot_collect(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "ACTIVE"}]),
            patch.object(reservations, "run_sql") as run,
        ):
            for path, args in (
                ("/api/reservations/{reservation_id}/collect", (88, self.request())),
            ):
                with self.subTest(path=path), self.assertRaises(HTTPException) as error:
                    asyncio.run(self.endpoint(path)(*args))
                self.assertEqual(error.exception.status_code, 403)
        run.assert_not_called()

    def test_disabled_membership_blocks_student_data(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "DISABLED"}]),
            self.assertRaises(HTTPException) as error,
        ):
            self.endpoint("/api/student/dashboard")(self.request())
        self.assertEqual(error.exception.status_code, 403)

    def test_dashboard_queries_scope_loans_and_fines_before_execution(self):
        # Keep the real query collector; replace only the Oracle transport.
        with (
            patch.object(reservations, "rows", wraps=reservations.rows) as query,
            patch("backend.database.run_sql", return_value="ACTIVE"),
            patch.object(
                reservations, "read_many", return_value=[[], [{"student_id": 17}], [], [], []]
            ) as batch,
        ):
            self.endpoint("/api/student/dashboard")(self.request())
        queries = batch.call_args.args[0]
        self.assertIn("WHERE i.student_id=17", queries[2][0])
        self.assertIn("WHERE i.student_id=17", queries[3][0])
        self.assertIn("WHERE r.student_id=17", queries[4][0])
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import asyncio</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from starlette.requests import Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from backend import main, reservations</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend.auth.session import create_session, remove_session, SESSION_COOKIE</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>class ReservationTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 12 | <code>    def setUp(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 13 | <code>        self.token = create_session(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `setUp` অংশে |
| 14 | <code>            {&quot;user_id&quot;: 500, &quot;username&quot;: &quot;studentqa&quot;, &quot;user_type&quot;: &quot;STUDENT&quot;, &quot;student_id&quot;: 17}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 15 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `setUp` অংশে |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>    def tearDown(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 18 | <code>        remove_session(self.token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `tearDown` অংশে |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>    def request(self, body=&quot;&quot;):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 21 | <code>        async def receive():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 22 | <code>            return {&quot;type&quot;: &quot;http.request&quot;, &quot;body&quot;: body.encode(), &quot;more_body&quot;: False}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `receive` অংশে |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>        return Request(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `request` অংশে |
| 25 | <code>            {</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 26 | <code>                &quot;type&quot;: &quot;http&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 27 | <code>                &quot;method&quot;: &quot;POST&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 28 | <code>                &quot;headers&quot;: [(b&quot;cookie&quot;, f&quot;{SESSION_COOKIE}={self.token}&quot;.encode())],</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `request` অংশে |
| 29 | <code>            },</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 30 | <code>            receive,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 31 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `request` অংশে |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>    def endpoint(self, path, method=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 34 | <code>        return next(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `endpoint` অংশে |
| 35 | <code>            route.endpoint</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `endpoint` অংশে |
| 36 | <code>            for route in main.app.routes</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `endpoint` অংশে |
| 37 | <code>            if getattr(route, &quot;path&quot;, None) == path and (method is None or method in route.methods)</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `endpoint` অংশে |
| 38 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `endpoint` অংশে |
| 39 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 40 | <code>    def test_student_cannot_reserve_for_another_member(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 41 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_reserve_for_another_member` অংশে |
| 42 | <code>            patch.object(reservations, &quot;rows&quot;, return_value=[{&quot;membership_status&quot;: &quot;ACTIVE&quot;}]),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_student_cannot_reserve_for_another_member` অংশে |
| 43 | <code>            patch.object(reservations, &quot;run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_reserve_for_another_member` অংশে |
| 44 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_reserve_for_another_member` অংশে |
| 45 | <code>            asyncio.run(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_reserve_for_another_member` অংশে |
| 46 | <code>                self.endpoint(&quot;/api/reservations&quot;, &quot;POST&quot;)(self.request(&quot;bookId=4&amp;studentId=99&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_student_cannot_reserve_for_another_member` অংশে |
| 47 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_reserve_for_another_member` অংশে |
| 48 | <code>        self.assertIn(&quot;reserve_book_proc(17,4)&quot;, run.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 49 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 50 | <code>    def test_student_cancellation_checks_owner_in_sql(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 51 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 52 | <code>            patch.object(reservations, &quot;rows&quot;, return_value=[{&quot;membership_status&quot;: &quot;ACTIVE&quot;}]),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 53 | <code>            patch.object(reservations, &quot;run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 54 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 55 | <code>            asyncio.run(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 56 | <code>                self.endpoint(&quot;/api/reservations/{reservation_id}/cancel&quot;)(88, self.request())</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 57 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cancellation_checks_owner_in_sql` অংশে |
| 58 | <code>        self.assertEqual(run.call_args.args[0].count(&quot;AND student_id=17&quot;), 2)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 59 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 60 | <code>    def test_student_cannot_collect(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 61 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_collect` অংশে |
| 62 | <code>            patch.object(reservations, &quot;rows&quot;, return_value=[{&quot;membership_status&quot;: &quot;ACTIVE&quot;}]),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_student_cannot_collect` অংশে |
| 63 | <code>            patch.object(reservations, &quot;run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_collect` অংশে |
| 64 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_collect` অংশে |
| 65 | <code>            for path, args in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_student_cannot_collect` অংশে |
| 66 | <code>                (&quot;/api/reservations/{reservation_id}/collect&quot;, (88, self.request())),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_collect` অংশে |
| 67 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_collect` অংশে |
| 68 | <code>                with self.subTest(path=path), self.assertRaises(HTTPException) as error:</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 69 | <code>                    asyncio.run(self.endpoint(path)(*args))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_student_cannot_collect` অংশে |
| 70 | <code>                self.assertEqual(error.exception.status_code, 403)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 71 | <code>        run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 72 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 73 | <code>    def test_disabled_membership_blocks_student_data(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 74 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_disabled_membership_blocks_student_data` অংশে |
| 75 | <code>            patch.object(reservations, &quot;rows&quot;, return_value=[{&quot;membership_status&quot;: &quot;DISABLED&quot;}]),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_disabled_membership_blocks_student_data` অংশে |
| 76 | <code>            self.assertRaises(HTTPException) as error,</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 77 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_disabled_membership_blocks_student_data` অংশে |
| 78 | <code>            self.endpoint(&quot;/api/student/dashboard&quot;)(self.request())</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_disabled_membership_blocks_student_data` অংশে |
| 79 | <code>        self.assertEqual(error.exception.status_code, 403)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 80 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 81 | <code>    def test_dashboard_queries_scope_loans_and_fines_before_execution(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 82 | <code>        # Keep the real query collector; replace only the Oracle transport.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 83 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 84 | <code>            patch.object(reservations, &quot;rows&quot;, wraps=reservations.rows) as query,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 85 | <code>            patch(&quot;backend.database.run_sql&quot;, return_value=&quot;ACTIVE&quot;),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 86 | <code>            patch.object(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 87 | <code>                reservations, &quot;read_many&quot;, return_value=[[], [{&quot;student_id&quot;: 17}], [], [], []]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 88 | <code>            ) as batch,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 89 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 90 | <code>            self.endpoint(&quot;/api/student/dashboard&quot;)(self.request())</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 91 | <code>        queries = batch.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_dashboard_queries_scope_loans_and_fines_before_execution` অংশে |
| 92 | <code>        self.assertIn(&quot;WHERE i.student_id=17&quot;, queries[2][0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 93 | <code>        self.assertIn(&quot;WHERE i.student_id=17&quot;, queries[3][0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 94 | <code>        self.assertIn(&quot;WHERE r.student_id=17&quot;, queries[4][0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
