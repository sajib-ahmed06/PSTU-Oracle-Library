# tests/test_members_audit.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_members_audit.py)। Snapshot 2026-10-04; 169 lines; SHA-256 `fb974a623e542bf7fc2a58480e7013420ba00c4fe6a7d091b8491ae3dc235dd6`।

## Function / object / element inventory

### `tearDown` — L16–L17

`def tearDown(self):`

Test/setup helper: tearDown; নিচের assertions/calls সেই behavior define করে।

### `request` — L19–L23

`def request(self, body):`

Test/setup helper: request; নিচের assertions/calls সেই behavior define করে।

### `read_body` — L20–L21

`async def read_body():`

Test/setup helper: read body; নিচের assertions/calls সেই behavior define করে।

### `test_identifiers_keep_leading_zeros_and_normalize_case` — L25–L30

`def test_identifiers_keep_leading_zeros_and_normalize_case(self):`

Test/setup helper: test identifiers keep leading zeros and normalize case; নিচের assertions/calls সেই behavior define করে।

### `test_new_members_require_both_identifiers` — L32–L39

`def test_new_members_require_both_identifiers(self):`

Test/setup helper: test new members require both identifiers; নিচের assertions/calls সেই behavior define করে।

### `test_member_insert_passes_both_identifiers_to_database` — L41–L49

`def test_member_insert_passes_both_identifiers_to_database(self):`

Test/setup helper: test member insert passes both identifiers to database; নিচের assertions/calls সেই behavior define করে।

### `test_duplicate_constraint_errors_have_specific_messages` — L51–L67

`def test_duplicate_constraint_errors_have_specific_messages(self):`

Test/setup helper: test duplicate constraint errors have specific messages; নিচের assertions/calls সেই behavior define করে।

### `test_edit_identifiers_checks_missing_member` — L69–L76

`def test_edit_identifiers_checks_missing_member(self):`

Test/setup helper: test edit identifiers checks missing member; নিচের assertions/calls সেই behavior define করে।

### `test_full_member_edit_validates_and_updates_all_fields` — L78–L94

`def test_full_member_edit_validates_and_updates_all_fields(self):`

Test/setup helper: test full member edit validates and updates all fields; নিচের assertions/calls সেই behavior define করে।

### `test_full_member_edit_rejects_invalid_contact_and_status` — L96–L123

`def test_full_member_edit_rejects_invalid_contact_and_status(self):`

Test/setup helper: test full member edit rejects invalid contact and status; নিচের assertions/calls সেই behavior define করে।

### `test_audit_requires_administrator` — L125–L130

`def test_audit_requires_administrator(self):`

Test/setup helper: test audit requires administrator; নিচের assertions/calls সেই behavior define করে।

### `test_audit_decodes_snapshots_and_paginates` — L132–L152

`def test_audit_decodes_snapshots_and_paginates(self):`

Test/setup helper: test audit decodes snapshots and paginates; নিচের assertions/calls সেই behavior define করে।

### `test_request_actor_is_sent_to_oracle_session` — L154–L165

`def test_request_actor_is_sent_to_oracle_session(self):`

Test/setup helper: test request actor is sent to oracle session; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
from backend.routes import members, audit
import asyncio
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from backend import database, main
from backend.audit import audit_actor
from backend.auth.session import SESSIONS, create_session
from backend.validation import academic_identifier


class MemberAuditTests(unittest.TestCase):
    def tearDown(self):
        SESSIONS.clear()

    def request(self, body):
        async def read_body():
            return body

        return SimpleNamespace(body=read_body)

    def test_identifiers_keep_leading_zeros_and_normalize_case(self):
        self.assertEqual(academic_identifier(" 0012-ab ", "Roll"), "0012-AB")
        self.assertEqual(academic_identifier("2024/001", "Registration"), "2024/001")
        for invalid in ("", "  ", "a b", "A|B", "x" * 41, "???"):
            with self.subTest(invalid=invalid), self.assertRaises(HTTPException):
                academic_identifier(invalid, "Roll")

    def test_new_members_require_both_identifiers(self):
        request = self.request(
            b"name=Test&department=CSE&phone=01700000099&email=test%40example.com"
        )
        with patch.object(members, "run_sql") as run, self.assertRaises(HTTPException) as error:
            asyncio.run(main.add_student(request))
        self.assertEqual(error.exception.status_code, 400)
        run.assert_not_called()

    def test_member_insert_passes_both_identifiers_to_database(self):
        request = self.request(
            b"name=Test&department=CSE&phone=01700000099&email=test%40example.com&roll_no=001-ab&registration_no=reg-001&academic_session=2023-2024"
        )
        with patch.object(members, "run_sql", return_value="0") as run:
            asyncio.run(main.add_student(request))
        sql = run.call_args.args[0]
        self.assertIn("'001-AB'", sql)
        self.assertIn("'REG-001'", sql)

    def test_duplicate_constraint_errors_have_specific_messages(self):
        for index, message in (
            ("UQ_STUDENT_ROLL", "ID/Roll"),
            ("UQ_STUDENT_REGISTRATION", "Registration"),
        ):
            result = SimpleNamespace(
                stdout=f"ORA-00001: unique constraint (CONFIGURED_SCHEMA.{index}) violated",
                stderr="",
                returncode=1,
            )
            with (
                patch.object(database.subprocess, "run", return_value=result),
                self.assertRaises(HTTPException) as error,
            ):
                database.run_sql("UPDATE student SET roll_no='001';")
            self.assertEqual(error.exception.status_code, 409)
            self.assertIn(message, error.exception.detail)

    def test_edit_identifiers_checks_missing_member(self):
        with patch.object(members, "run_sql") as run:
            asyncio.run(
                main.update_student_identity(
                    999, self.request(b"roll_no=001&registration_no=REG-001")
                )
            )
        self.assertIn("SQL%ROWCOUNT = 0", run.call_args.args[0])

    def test_full_member_edit_validates_and_updates_all_fields(self):
        body = b"name=Updated+Name&department=EEE&phone=01700000099&email=updated%40example.com&roll_no=001-ab&registration_no=REG-001&membership_status=ACTIVE&academic_session=2023-2024"
        with patch.object(members, "run_sql") as run:
            asyncio.run(main.edit_student(1, self.request(body)))
        sql = run.call_args.args[0]
        for value in (
            "Updated Name",
            "EEE",
            "01700000099",
            "updated@example.com",
            "001-AB",
            "REG-001",
        ):
            self.assertIn(value, sql)
        self.assertIn("FOR UPDATE", sql)
        self.assertIn("Return all issued books", sql)
        self.assertIn("Pay all fines", sql)

    def test_full_member_edit_rejects_invalid_contact_and_status(self):
        from urllib.parse import urlencode

        data = {
            "name": "Test",
            "department": "CSE",
            "phone": "01700000099",
            "email": "test@example.com",
            "roll_no": "001",
            "registration_no": "REG-001",
            "membership_status": "ACTIVE",
            "academic_session": "2023-2024",
        }
        for field, value in (
            ("phone", "123"),
            ("email", "invalid"),
            ("membership_status", "UNKNOWN"),
        ):
            with (
                self.subTest(field=field),
                patch.object(members, "run_sql") as run,
                self.assertRaises(HTTPException) as error,
            ):
                asyncio.run(
                    main.edit_student(1, self.request(urlencode({**data, field: value}).encode()))
                )
            self.assertEqual(error.exception.status_code, 400)
            run.assert_not_called()

    def test_audit_requires_administrator(self):
        token = create_session({"user_id": 1, "username": "staff", "user_type": "LIBRARIAN"})
        with patch.object(audit, "rows") as query, self.assertRaises(HTTPException) as error:
            main.get_audit(SimpleNamespace(cookies={"library_session": token}))
        self.assertEqual(error.exception.status_code, 403)
        query.assert_not_called()

    def test_audit_decodes_snapshots_and_paginates(self):
        token = create_session({"user_id": 1, "username": "admin", "user_type": "ADMIN"})
        request = SimpleNamespace(cookies={"library_session": token})
        snapshot = {"name": "O'Reilly | Test", "roll_no": "001"}
        encoded = json.dumps(snapshot).encode().hex()
        item = {
            "audit_id": 26,
            "occurred_at": "2026-10-03T12:00:00.000Z",
            "actor": "admin".encode().hex(),
            "action": "UPDATE",
            "entity": "STUDENT",
            "record_id": 1,
            "before": None,
            "after": encoded,
        }
        with patch.object(audit, "rows", side_effect=[[{"total": 26}], [item]]) as query:
            result = main.get_audit(request, entity="STUDENT", page=2)
        self.assertEqual(result["items"][0]["after"], snapshot)
        self.assertEqual(result["items"][0]["actor"], "admin")
        self.assertIn("ROWNUM <= 50", query.call_args.args[0])
        self.assertIn("row_number > 25", query.call_args.args[0])

    def test_request_actor_is_sent_to_oracle_session(self):
        token = audit_actor.set("admin")
        try:
            with patch.object(
                database.subprocess,
                "run",
                return_value=SimpleNamespace(stdout="", stderr="", returncode=0),
            ) as run:
                database.run_sql("SELECT 1 FROM dual;")
            self.assertIn("SET_CLIENT_INFO('admin')", run.call_args.kwargs["input"])
        finally:
            audit_actor.reset(token)


if __name__ == "__main__":
    unittest.main()
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>from backend.routes import members, audit</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import asyncio</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>import json</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>from types import SimpleNamespace</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend import database, main</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from backend.audit import audit_actor</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from backend.auth.session import SESSIONS, create_session</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from backend.validation import academic_identifier</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 15 | <code>class MemberAuditTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 16 | <code>    def tearDown(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 17 | <code>        SESSIONS.clear()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `tearDown` অংশে |
| 18 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 19 | <code>    def request(self, body):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 20 | <code>        async def read_body():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 21 | <code>            return body</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `read_body` অংশে |
| 22 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 23 | <code>        return SimpleNamespace(body=read_body)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `request` অংশে |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>    def test_identifiers_keep_leading_zeros_and_normalize_case(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 26 | <code>        self.assertEqual(academic_identifier(&quot; 0012-ab &quot;, &quot;Roll&quot;), &quot;0012-AB&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 27 | <code>        self.assertEqual(academic_identifier(&quot;2024/001&quot;, &quot;Registration&quot;), &quot;2024/001&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 28 | <code>        for invalid in (&quot;&quot;, &quot;  &quot;, &quot;a b&quot;, &quot;A&#124;B&quot;, &quot;x&quot; * 41, &quot;???&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_identifiers_keep_leading_zeros_and_normalize_case` অংশে |
| 29 | <code>            with self.subTest(invalid=invalid), self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 30 | <code>                academic_identifier(invalid, &quot;Roll&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_identifiers_keep_leading_zeros_and_normalize_case` অংশে |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>    def test_new_members_require_both_identifiers(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 33 | <code>        request = self.request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_new_members_require_both_identifiers` অংশে |
| 34 | <code>            b&quot;name=Test&amp;department=CSE&amp;phone=01700000099&amp;email=test%40example.com&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_new_members_require_both_identifiers` অংশে |
| 35 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_new_members_require_both_identifiers` অংশে |
| 36 | <code>        with patch.object(members, &quot;run_sql&quot;) as run, self.assertRaises(HTTPException) as error:</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 37 | <code>            asyncio.run(main.add_student(request))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_new_members_require_both_identifiers` অংশে |
| 38 | <code>        self.assertEqual(error.exception.status_code, 400)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 39 | <code>        run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 40 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 41 | <code>    def test_member_insert_passes_both_identifiers_to_database(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 42 | <code>        request = self.request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_insert_passes_both_identifiers_to_database` অংশে |
| 43 | <code>            b&quot;name=Test&amp;department=CSE&amp;phone=01700000099&amp;email=test%40example.com&amp;roll_no=001-ab&amp;registration_no=reg-001&amp;academic_session=2023-2024&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_insert_passes_both_identifiers_to_database` অংশে |
| 44 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_insert_passes_both_identifiers_to_database` অংশে |
| 45 | <code>        with patch.object(members, &quot;run_sql&quot;, return_value=&quot;0&quot;) as run:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_insert_passes_both_identifiers_to_database` অংশে |
| 46 | <code>            asyncio.run(main.add_student(request))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_member_insert_passes_both_identifiers_to_database` অংশে |
| 47 | <code>        sql = run.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_member_insert_passes_both_identifiers_to_database` অংশে |
| 48 | <code>        self.assertIn(&quot;&#x27;001-AB&#x27;&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 49 | <code>        self.assertIn(&quot;&#x27;REG-001&#x27;&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 50 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 51 | <code>    def test_duplicate_constraint_errors_have_specific_messages(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 52 | <code>        for index, message in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 53 | <code>            (&quot;UQ_STUDENT_ROLL&quot;, &quot;ID/Roll&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 54 | <code>            (&quot;UQ_STUDENT_REGISTRATION&quot;, &quot;Registration&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 55 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 56 | <code>            result = SimpleNamespace(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 57 | <code>                stdout=f&quot;ORA-00001: unique constraint (CONFIGURED_SCHEMA.{index}) violated&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 58 | <code>                stderr=&quot;&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 59 | <code>                returncode=1,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 60 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 61 | <code>            with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 62 | <code>                patch.object(database.subprocess, &quot;run&quot;, return_value=result),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 63 | <code>                self.assertRaises(HTTPException) as error,</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 64 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 65 | <code>                database.run_sql(&quot;UPDATE student SET roll_no=&#x27;001&#x27;;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_duplicate_constraint_errors_have_specific_messages` অংশে |
| 66 | <code>            self.assertEqual(error.exception.status_code, 409)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 67 | <code>            self.assertIn(message, error.exception.detail)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 68 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 69 | <code>    def test_edit_identifiers_checks_missing_member(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 70 | <code>        with patch.object(members, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_edit_identifiers_checks_missing_member` অংশে |
| 71 | <code>            asyncio.run(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_edit_identifiers_checks_missing_member` অংশে |
| 72 | <code>                main.update_student_identity(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_edit_identifiers_checks_missing_member` অংশে |
| 73 | <code>                    999, self.request(b&quot;roll_no=001&amp;registration_no=REG-001&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_edit_identifiers_checks_missing_member` অংশে |
| 74 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_edit_identifiers_checks_missing_member` অংশে |
| 75 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_edit_identifiers_checks_missing_member` অংশে |
| 76 | <code>        self.assertIn(&quot;SQL%ROWCOUNT = 0&quot;, run.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 77 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 78 | <code>    def test_full_member_edit_validates_and_updates_all_fields(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 79 | <code>        body = b&quot;name=Updated+Name&amp;department=EEE&amp;phone=01700000099&amp;email=updated%40example.com&amp;roll_no=001-ab&amp;registration_no=REG-001&amp;membership_status=ACTIVE&amp;academic_session=2023-2024&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 80 | <code>        with patch.object(members, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 81 | <code>            asyncio.run(main.edit_student(1, self.request(body)))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 82 | <code>        sql = run.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 83 | <code>        for value in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 84 | <code>            &quot;Updated Name&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 85 | <code>            &quot;EEE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 86 | <code>            &quot;01700000099&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 87 | <code>            &quot;updated@example.com&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 88 | <code>            &quot;001-AB&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 89 | <code>            &quot;REG-001&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 90 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_validates_and_updates_all_fields` অংশে |
| 91 | <code>            self.assertIn(value, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 92 | <code>        self.assertIn(&quot;FOR UPDATE&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 93 | <code>        self.assertIn(&quot;Return all issued books&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 94 | <code>        self.assertIn(&quot;Pay all fines&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 95 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 96 | <code>    def test_full_member_edit_rejects_invalid_contact_and_status(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 97 | <code>        from urllib.parse import urlencode</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 98 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 99 | <code>        data = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 100 | <code>            &quot;name&quot;: &quot;Test&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 101 | <code>            &quot;department&quot;: &quot;CSE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 102 | <code>            &quot;phone&quot;: &quot;01700000099&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 103 | <code>            &quot;email&quot;: &quot;test@example.com&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 104 | <code>            &quot;roll_no&quot;: &quot;001&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 105 | <code>            &quot;registration_no&quot;: &quot;REG-001&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 106 | <code>            &quot;membership_status&quot;: &quot;ACTIVE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 107 | <code>            &quot;academic_session&quot;: &quot;2023-2024&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 108 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 109 | <code>        for field, value in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 110 | <code>            (&quot;phone&quot;, &quot;123&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 111 | <code>            (&quot;email&quot;, &quot;invalid&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 112 | <code>            (&quot;membership_status&quot;, &quot;UNKNOWN&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 113 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 114 | <code>            with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 115 | <code>                self.subTest(field=field),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 116 | <code>                patch.object(members, &quot;run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 117 | <code>                self.assertRaises(HTTPException) as error,</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 118 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 119 | <code>                asyncio.run(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 120 | <code>                    main.edit_student(1, self.request(urlencode({**data, field: value}).encode()))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 121 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_full_member_edit_rejects_invalid_contact_and_status` অংশে |
| 122 | <code>            self.assertEqual(error.exception.status_code, 400)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 123 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 124 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 125 | <code>    def test_audit_requires_administrator(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 126 | <code>        token = create_session({&quot;user_id&quot;: 1, &quot;username&quot;: &quot;staff&quot;, &quot;user_type&quot;: &quot;LIBRARIAN&quot;})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_requires_administrator` অংশে |
| 127 | <code>        with patch.object(audit, &quot;rows&quot;) as query, self.assertRaises(HTTPException) as error:</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 128 | <code>            main.get_audit(SimpleNamespace(cookies={&quot;library_session&quot;: token}))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_requires_administrator` অংশে |
| 129 | <code>        self.assertEqual(error.exception.status_code, 403)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 130 | <code>        query.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 131 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 132 | <code>    def test_audit_decodes_snapshots_and_paginates(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 133 | <code>        token = create_session({&quot;user_id&quot;: 1, &quot;username&quot;: &quot;admin&quot;, &quot;user_type&quot;: &quot;ADMIN&quot;})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 134 | <code>        request = SimpleNamespace(cookies={&quot;library_session&quot;: token})</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 135 | <code>        snapshot = {&quot;name&quot;: &quot;O&#x27;Reilly &#124; Test&quot;, &quot;roll_no&quot;: &quot;001&quot;}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 136 | <code>        encoded = json.dumps(snapshot).encode().hex()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 137 | <code>        item = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 138 | <code>            &quot;audit_id&quot;: 26,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 139 | <code>            &quot;occurred_at&quot;: &quot;2026-10-03T12:00:00.000Z&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 140 | <code>            &quot;actor&quot;: &quot;admin&quot;.encode().hex(),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 141 | <code>            &quot;action&quot;: &quot;UPDATE&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 142 | <code>            &quot;entity&quot;: &quot;STUDENT&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 143 | <code>            &quot;record_id&quot;: 1,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 144 | <code>            &quot;before&quot;: None,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 145 | <code>            &quot;after&quot;: encoded,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 146 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 147 | <code>        with patch.object(audit, &quot;rows&quot;, side_effect=[[{&quot;total&quot;: 26}], [item]]) as query:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 148 | <code>            result = main.get_audit(request, entity=&quot;STUDENT&quot;, page=2)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_audit_decodes_snapshots_and_paginates` অংশে |
| 149 | <code>        self.assertEqual(result[&quot;items&quot;][0][&quot;after&quot;], snapshot)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 150 | <code>        self.assertEqual(result[&quot;items&quot;][0][&quot;actor&quot;], &quot;admin&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 151 | <code>        self.assertIn(&quot;ROWNUM &lt;= 50&quot;, query.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 152 | <code>        self.assertIn(&quot;row_number &gt; 25&quot;, query.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 153 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 154 | <code>    def test_request_actor_is_sent_to_oracle_session(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 155 | <code>        token = audit_actor.set(&quot;admin&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 156 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 157 | <code>            with patch.object(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 158 | <code>                database.subprocess,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 159 | <code>                &quot;run&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 160 | <code>                return_value=SimpleNamespace(stdout=&quot;&quot;, stderr=&quot;&quot;, returncode=0),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 161 | <code>            ) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 162 | <code>                database.run_sql(&quot;SELECT 1 FROM dual;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 163 | <code>            self.assertIn(&quot;SET_CLIENT_INFO(&#x27;admin&#x27;)&quot;, run.call_args.kwargs[&quot;input&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 164 | <code>        finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 165 | <code>            audit_actor.reset(token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_request_actor_is_sent_to_oracle_session` অংশে |
| 166 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 167 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 168 | <code>if __name__ == &quot;__main__&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। |
| 169 | <code>    unittest.main()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
