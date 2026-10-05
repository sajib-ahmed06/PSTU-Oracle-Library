# tests/test_connection_recovery.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_connection_recovery.py)। Snapshot 2026-10-04; 94 lines; SHA-256 `befda6c6e2266a4429bec0e36bc9aeac87877adec5d02617f499bc1f61461179`।

## Function / object / element inventory

### `result` — L11–L12

`def result(self, text="1", code=0):`

Test/setup helper: result; নিচের assertions/calls সেই behavior define করে।

### `test_listener_rejection_retries_before_sql_execution` — L14–L23

`def test_listener_rejection_retries_before_sql_execution(self):`

Test/setup helper: test listener rejection retries before sql execution; নিচের assertions/calls সেই behavior define করে।

### `test_read_disconnect_retries_but_mutation_never_replays` — L25–L39

`def test_read_disconnect_retries_but_mutation_never_replays(self):`

Test/setup helper: test read disconnect retries but mutation never replays; নিচের assertions/calls সেই behavior define করে।

### `test_timeout_does_not_replay_mutation_and_releases_slot` — L41–L53

`def test_timeout_does_not_replay_mutation_and_releases_slot(self):`

Test/setup helper: test timeout does not replay mutation and releases slot; নিচের assertions/calls সেই behavior define করে।

### `test_normal_data_containing_oracle_error_text_is_not_an_error` — L55–L64

`def test_normal_data_containing_oracle_error_text_is_not_an_error(self):`

Test/setup helper: test normal data containing oracle error text is not an error; নিচের assertions/calls সেই behavior define করে।

### `test_batch_uses_one_connection_and_keeps_sections_separate` — L66–L77

`def test_batch_uses_one_connection_and_keeps_sections_separate(self):`

Test/setup helper: test batch uses one connection and keeps sections separate; নিচের assertions/calls সেই behavior define করে।

### `test_collect_reads_is_scoped_and_does_not_execute_queries` — L79–L85

`def test_collect_reads_is_scoped_and_does_not_execute_queries(self):`

Test/setup helper: test collect reads is scoped and does not execute queries; নিচের assertions/calls সেই behavior define করে।

### `test_batch_rejects_incomplete_output_and_writes` — L87–L94

`def test_batch_rejects_incomplete_output_and_writes(self):`

Test/setup helper: test batch rejects incomplete output and writes; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from backend import database


class ConnectionRecoveryTests(unittest.TestCase):
    def result(self, text="1", code=0):
        return SimpleNamespace(stdout=text, stderr="", returncode=code)

    def test_listener_rejection_retries_before_sql_execution(self):
        error = self.result("ORA-12520: listener has no available handler", 1)
        with (
            patch.object(database.subprocess, "run", side_effect=[error, self.result()]) as run,
            patch.object(database.time, "sleep"),
        ):
            self.assertEqual(database.run_sql("SELECT 1 FROM dual;"), "1")
        self.assertEqual(run.call_count, 2)
        script = run.call_args.kwargs["input"]
        self.assertLess(script.index("WHENEVER SQLERROR"), script.index("CONNECT "))

    def test_read_disconnect_retries_but_mutation_never_replays(self):
        error = self.result("ORA-03113: end-of-file on communication channel", 1)
        with (
            patch.object(database.subprocess, "run", side_effect=[error, self.result()]) as run,
            patch.object(database.time, "sleep"),
        ):
            database.run_sql("SELECT 1 FROM dual;")
            self.assertEqual(run.call_count, 2)
        with (
            patch.object(database.subprocess, "run", return_value=error) as run,
            patch.object(database.time, "sleep"),
            self.assertRaises(HTTPException),
        ):
            database.run_sql("UPDATE fine SET payment_status='PAID'; COMMIT;")
        self.assertEqual(run.call_count, 1)

    def test_timeout_does_not_replay_mutation_and_releases_slot(self):
        with (
            patch.object(
                database.subprocess, "run", side_effect=subprocess.TimeoutExpired("sqlplus", 20)
            ) as run,
            patch.object(database.time, "sleep"),
            self.assertRaises(HTTPException) as error,
        ):
            database.run_sql("UPDATE fine SET payment_status='PAID'; COMMIT;")
        self.assertEqual(error.exception.status_code, 504)
        self.assertEqual(run.call_count, 1)
        self.assertTrue(database.SQL_SLOTS.acquire(blocking=False))
        database.SQL_SLOTS.release()

    def test_normal_data_containing_oracle_error_text_is_not_an_error(self):
        with (
            patch.object(
                database.subprocess, "run", return_value=self.result("1|A book about ORA-12520")
            ),
            patch.object(database.time, "sleep"),
        ):
            self.assertEqual(
                database.run_sql("SELECT title FROM book;"), "1|A book about ORA-12520"
            )

    def test_batch_uses_one_connection_and_keeps_sections_separate(self):
        output = "__LIBRARY_READ_0__\n1|First\n__LIBRARY_READ_1__\n__LIBRARY_READ_2__\n2|Second"
        queries = [
            ("SELECT 1 FROM dual", ["id", "name"], {"id"}),
            ("SELECT 2 FROM dual", ["id"], {"id"}),
            ("SELECT 3 FROM dual", ["id", "name"], {"id"}),
        ]
        with patch.object(database, "run_sql", return_value=output) as run:
            result = database.read_many(queries)
        self.assertEqual(result, [[{"id": 1, "name": "First"}], [], [{"id": 2, "name": "Second"}]])
        run.assert_called_once()
        self.assertTrue(run.call_args.kwargs["read_batch"])

    def test_collect_reads_is_scoped_and_does_not_execute_queries(self):
        with patch.object(database, "run_sql") as run:
            with database.collect_reads() as queries:
                self.assertEqual(database.rows("SELECT 1 FROM dual", ["id"], {"id"}), [])
            run.assert_not_called()
        self.assertEqual(len(queries), 1)
        self.assertIsNone(database.PENDING_READS.get())

    def test_batch_rejects_incomplete_output_and_writes(self):
        with patch.object(database, "run_sql", return_value=""):
            with self.assertRaises(HTTPException):
                database.read_many([("SELECT 1 FROM dual", ["id"], {"id"})])
        with patch.object(database, "run_sql") as run:
            with self.assertRaises(ValueError):
                database.read_many([("UPDATE book SET quantity=1", ["id"], set())])
            run.assert_not_called()
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import subprocess</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>from types import SimpleNamespace</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from backend import database</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>class ConnectionRecoveryTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 11 | <code>    def result(self, text=&quot;1&quot;, code=0):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 12 | <code>        return SimpleNamespace(stdout=text, stderr=&quot;&quot;, returncode=code)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `result` অংশে |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>    def test_listener_rejection_retries_before_sql_execution(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 15 | <code>        error = self.result(&quot;ORA-12520: listener has no available handler&quot;, 1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_listener_rejection_retries_before_sql_execution` অংশে |
| 16 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_listener_rejection_retries_before_sql_execution` অংশে |
| 17 | <code>            patch.object(database.subprocess, &quot;run&quot;, side_effect=[error, self.result()]) as run,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_listener_rejection_retries_before_sql_execution` অংশে |
| 18 | <code>            patch.object(database.time, &quot;sleep&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_listener_rejection_retries_before_sql_execution` অংশে |
| 19 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_listener_rejection_retries_before_sql_execution` অংশে |
| 20 | <code>            self.assertEqual(database.run_sql(&quot;SELECT 1 FROM dual;&quot;), &quot;1&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 21 | <code>        self.assertEqual(run.call_count, 2)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 22 | <code>        script = run.call_args.kwargs[&quot;input&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_listener_rejection_retries_before_sql_execution` অংশে |
| 23 | <code>        self.assertLess(script.index(&quot;WHENEVER SQLERROR&quot;), script.index(&quot;CONNECT &quot;))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>    def test_read_disconnect_retries_but_mutation_never_replays(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 26 | <code>        error = self.result(&quot;ORA-03113: end-of-file on communication channel&quot;, 1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 27 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 28 | <code>            patch.object(database.subprocess, &quot;run&quot;, side_effect=[error, self.result()]) as run,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 29 | <code>            patch.object(database.time, &quot;sleep&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 30 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 31 | <code>            database.run_sql(&quot;SELECT 1 FROM dual;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 32 | <code>            self.assertEqual(run.call_count, 2)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 33 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 34 | <code>            patch.object(database.subprocess, &quot;run&quot;, return_value=error) as run,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 35 | <code>            patch.object(database.time, &quot;sleep&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 36 | <code>            self.assertRaises(HTTPException),</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 37 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 38 | <code>            database.run_sql(&quot;UPDATE fine SET payment_status=&#x27;PAID&#x27;; COMMIT;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_read_disconnect_retries_but_mutation_never_replays` অংশে |
| 39 | <code>        self.assertEqual(run.call_count, 1)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 40 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 41 | <code>    def test_timeout_does_not_replay_mutation_and_releases_slot(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 42 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 43 | <code>            patch.object(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 44 | <code>                database.subprocess, &quot;run&quot;, side_effect=subprocess.TimeoutExpired(&quot;sqlplus&quot;, 20)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 45 | <code>            ) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 46 | <code>            patch.object(database.time, &quot;sleep&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 47 | <code>            self.assertRaises(HTTPException) as error,</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 48 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 49 | <code>            database.run_sql(&quot;UPDATE fine SET payment_status=&#x27;PAID&#x27;; COMMIT;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 50 | <code>        self.assertEqual(error.exception.status_code, 504)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 51 | <code>        self.assertEqual(run.call_count, 1)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 52 | <code>        self.assertTrue(database.SQL_SLOTS.acquire(blocking=False))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 53 | <code>        database.SQL_SLOTS.release()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_timeout_does_not_replay_mutation_and_releases_slot` অংশে |
| 54 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 55 | <code>    def test_normal_data_containing_oracle_error_text_is_not_an_error(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 56 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 57 | <code>            patch.object(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 58 | <code>                database.subprocess, &quot;run&quot;, return_value=self.result(&quot;1&#124;A book about ORA-12520&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 59 | <code>            ),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 60 | <code>            patch.object(database.time, &quot;sleep&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 61 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 62 | <code>            self.assertEqual(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 63 | <code>                database.run_sql(&quot;SELECT title FROM book;&quot;), &quot;1&#124;A book about ORA-12520&quot;</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 64 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_normal_data_containing_oracle_error_text_is_not_an_error` অংশে |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>    def test_batch_uses_one_connection_and_keeps_sections_separate(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 67 | <code>        output = &quot;__LIBRARY_READ_0__\n1&#124;First\n__LIBRARY_READ_1__\n__LIBRARY_READ_2__\n2&#124;Second&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 68 | <code>        queries = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 69 | <code>            (&quot;SELECT 1 FROM dual&quot;, [&quot;id&quot;, &quot;name&quot;], {&quot;id&quot;}),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 70 | <code>            (&quot;SELECT 2 FROM dual&quot;, [&quot;id&quot;], {&quot;id&quot;}),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 71 | <code>            (&quot;SELECT 3 FROM dual&quot;, [&quot;id&quot;, &quot;name&quot;], {&quot;id&quot;}),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 72 | <code>        ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 73 | <code>        with patch.object(database, &quot;run_sql&quot;, return_value=output) as run:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 74 | <code>            result = database.read_many(queries)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_uses_one_connection_and_keeps_sections_separate` অংশে |
| 75 | <code>        self.assertEqual(result, [[{&quot;id&quot;: 1, &quot;name&quot;: &quot;First&quot;}], [], [{&quot;id&quot;: 2, &quot;name&quot;: &quot;Second&quot;}]])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 76 | <code>        run.assert_called_once()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 77 | <code>        self.assertTrue(run.call_args.kwargs[&quot;read_batch&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 78 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 79 | <code>    def test_collect_reads_is_scoped_and_does_not_execute_queries(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 80 | <code>        with patch.object(database, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_collect_reads_is_scoped_and_does_not_execute_queries` অংশে |
| 81 | <code>            with database.collect_reads() as queries:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_collect_reads_is_scoped_and_does_not_execute_queries` অংশে |
| 82 | <code>                self.assertEqual(database.rows(&quot;SELECT 1 FROM dual&quot;, [&quot;id&quot;], {&quot;id&quot;}), [])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 83 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 84 | <code>        self.assertEqual(len(queries), 1)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 85 | <code>        self.assertIsNone(database.PENDING_READS.get())</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 86 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 87 | <code>    def test_batch_rejects_incomplete_output_and_writes(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 88 | <code>        with patch.object(database, &quot;run_sql&quot;, return_value=&quot;&quot;):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_rejects_incomplete_output_and_writes` অংশে |
| 89 | <code>            with self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 90 | <code>                database.read_many([(&quot;SELECT 1 FROM dual&quot;, [&quot;id&quot;], {&quot;id&quot;})])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_rejects_incomplete_output_and_writes` অংশে |
| 91 | <code>        with patch.object(database, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_rejects_incomplete_output_and_writes` অংশে |
| 92 | <code>            with self.assertRaises(ValueError):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 93 | <code>                database.read_many([(&quot;UPDATE book SET quantity=1&quot;, [&quot;id&quot;], set())])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_rejects_incomplete_output_and_writes` অংশে |
| 94 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
