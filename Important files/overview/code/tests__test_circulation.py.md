# tests/test_circulation.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_circulation.py)। Snapshot 2026-10-04; 62 lines; SHA-256 `a70084d60875fa8289334befb19fab41ccc8e2ccce3235242efe502a43858fa6`।

## Function / object / element inventory

### `request` — L12–L16

`def request(body):`

Test/setup helper: request; নিচের assertions/calls সেই behavior define করে।

### `receive` — L13–L14

`async def receive():`

Test/setup helper: receive; নিচের assertions/calls সেই behavior define করে।

### `test_batch_has_one_commit_and_preserves_copy_selection` — L20–L34

`def test_batch_has_one_commit_and_preserves_copy_selection(self):`

Test/setup helper: test batch has one commit and preserves copy selection; নিচের assertions/calls সেই behavior define করে।

### `test_invalid_copy_never_executes_sql` — L36–L39

`def test_invalid_copy_never_executes_sql(self):`

Test/setup helper: test invalid copy never executes sql; নিচের assertions/calls সেই behavior define করে।

### `test_money_uses_decimal_and_rejects_invalid_values` — L41–L46

`def test_money_uses_decimal_and_rejects_invalid_values(self):`

Test/setup helper: test money uses decimal and rejects invalid values; নিচের assertions/calls সেই behavior define করে।

### `test_payment_rejects_custom_amount_and_invalid_note` — L48–L56

`def test_payment_rejects_custom_amount_and_invalid_note(self):`

Test/setup helper: test payment rejects custom amount and invalid note; নিচের assertions/calls সেই behavior define করে।

### `test_payment_uses_locked_database_balance` — L58–L62

`def test_payment_uses_locked_database_balance(self):`

Test/setup helper: test payment uses locked database balance; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
from backend.routes import circulation, fines
import asyncio
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from starlette.requests import Request
from backend import main
from backend.validation import payment_amount


def request(body):
    async def receive():
        return {"type": "http.request", "body": body.encode(), "more_body": False}

    return Request({"type": "http", "method": "POST", "headers": []}, receive)


class CirculationTests(unittest.TestCase):
    def test_batch_has_one_commit_and_preserves_copy_selection(self):
        with patch.object(circulation, "run_sql") as run:
            result = asyncio.run(
                main.add_issue(
                    request(
                        "studentId=2&bookId=1&copyId=11&bookId2=1&copyId2=12&bookId3=3&copyId3=31"
                    )
                )
            )
        sql = run.call_args.args[0]
        self.assertEqual(sql.count("COMMIT"), 1)
        self.assertIn("issue_book_proc(2, 1, 11)", sql)
        self.assertIn("issue_book_proc(2, 1, 12)", sql)
        self.assertIn("issue_book_proc(2, 3, 31)", sql)
        self.assertEqual(result["message"], "3 book copies issued")

    def test_invalid_copy_never_executes_sql(self):
        with patch.object(circulation, "run_sql") as run, self.assertRaises(HTTPException):
            asyncio.run(main.add_issue(request("studentId=2&bookId=1&copyId=-1")))
        run.assert_not_called()

    def test_money_uses_decimal_and_rejects_invalid_values(self):
        self.assertEqual(payment_amount("0.10"), "0.10")
        self.assertEqual(payment_amount("35.25"), "35.25")
        for value in ("0", "-1", "NaN", "Infinity", "1.001", "abc", "10000000000"):
            with self.subTest(value=value), self.assertRaises(HTTPException):
                payment_amount(value)

    def test_payment_rejects_custom_amount_and_invalid_note(self):
        for body in ("amount=35.25", "amount=0", "note=%00"):
            with (
                self.subTest(body=body),
                patch.object(fines, "run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(main.pay_fine(1, request(body)))
            run.assert_not_called()

    def test_payment_uses_locked_database_balance(self):
        with patch.object(fines, "run_sql") as run:
            result = asyncio.run(main.pay_fine(1, request("note=Full+payment")))
        self.assertIn("pay_fine_proc(1, NULL, 'Full payment')", run.call_args.args[0])
        self.assertEqual(result["message"], "Fine paid in full")
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>from backend.routes import circulation, fines</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import asyncio</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from starlette.requests import Request</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from backend import main</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from backend.validation import payment_amount</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 12 | <code>def request(body):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 13 | <code>    async def receive():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 14 | <code>        return {&quot;type&quot;: &quot;http.request&quot;, &quot;body&quot;: body.encode(), &quot;more_body&quot;: False}</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `receive` অংশে |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>    return Request({&quot;type&quot;: &quot;http&quot;, &quot;method&quot;: &quot;POST&quot;, &quot;headers&quot;: []}, receive)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `request` অংশে |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 19 | <code>class CirculationTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 20 | <code>    def test_batch_has_one_commit_and_preserves_copy_selection(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 21 | <code>        with patch.object(circulation, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 22 | <code>            result = asyncio.run(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 23 | <code>                main.add_issue(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 24 | <code>                    request(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 25 | <code>                        &quot;studentId=2&amp;bookId=1&amp;copyId=11&amp;bookId2=1&amp;copyId2=12&amp;bookId3=3&amp;copyId3=31&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 26 | <code>                    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 27 | <code>                )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 28 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 29 | <code>        sql = run.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_batch_has_one_commit_and_preserves_copy_selection` অংশে |
| 30 | <code>        self.assertEqual(sql.count(&quot;COMMIT&quot;), 1)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 31 | <code>        self.assertIn(&quot;issue_book_proc(2, 1, 11)&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 32 | <code>        self.assertIn(&quot;issue_book_proc(2, 1, 12)&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 33 | <code>        self.assertIn(&quot;issue_book_proc(2, 3, 31)&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 34 | <code>        self.assertEqual(result[&quot;message&quot;], &quot;3 book copies issued&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 35 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 36 | <code>    def test_invalid_copy_never_executes_sql(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 37 | <code>        with patch.object(circulation, &quot;run_sql&quot;) as run, self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 38 | <code>            asyncio.run(main.add_issue(request(&quot;studentId=2&amp;bookId=1&amp;copyId=-1&quot;)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_invalid_copy_never_executes_sql` অংশে |
| 39 | <code>        run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 40 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 41 | <code>    def test_money_uses_decimal_and_rejects_invalid_values(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 42 | <code>        self.assertEqual(payment_amount(&quot;0.10&quot;), &quot;0.10&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 43 | <code>        self.assertEqual(payment_amount(&quot;35.25&quot;), &quot;35.25&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 44 | <code>        for value in (&quot;0&quot;, &quot;-1&quot;, &quot;NaN&quot;, &quot;Infinity&quot;, &quot;1.001&quot;, &quot;abc&quot;, &quot;10000000000&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_money_uses_decimal_and_rejects_invalid_values` অংশে |
| 45 | <code>            with self.subTest(value=value), self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 46 | <code>                payment_amount(value)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_money_uses_decimal_and_rejects_invalid_values` অংশে |
| 47 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 48 | <code>    def test_payment_rejects_custom_amount_and_invalid_note(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 49 | <code>        for body in (&quot;amount=35.25&quot;, &quot;amount=0&quot;, &quot;note=%00&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_payment_rejects_custom_amount_and_invalid_note` অংশে |
| 50 | <code>            with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_payment_rejects_custom_amount_and_invalid_note` অংশে |
| 51 | <code>                self.subTest(body=body),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_payment_rejects_custom_amount_and_invalid_note` অংশে |
| 52 | <code>                patch.object(fines, &quot;run_sql&quot;) as run,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_payment_rejects_custom_amount_and_invalid_note` অংশে |
| 53 | <code>                self.assertRaises(HTTPException),</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 54 | <code>            ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_payment_rejects_custom_amount_and_invalid_note` অংশে |
| 55 | <code>                asyncio.run(main.pay_fine(1, request(body)))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_payment_rejects_custom_amount_and_invalid_note` অংশে |
| 56 | <code>            run.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 57 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 58 | <code>    def test_payment_uses_locked_database_balance(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 59 | <code>        with patch.object(fines, &quot;run_sql&quot;) as run:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_payment_uses_locked_database_balance` অংশে |
| 60 | <code>            result = asyncio.run(main.pay_fine(1, request(&quot;note=Full+payment&quot;)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_payment_uses_locked_database_balance` অংশে |
| 61 | <code>        self.assertIn(&quot;pay_fine_proc(1, NULL, &#x27;Full payment&#x27;)&quot;, run.call_args.args[0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 62 | <code>        self.assertEqual(result[&quot;message&quot;], &quot;Fine paid in full&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
