# tests/test_fine_collection.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_fine_collection.py)। Snapshot 2026-10-04; 27 lines; SHA-256 `3e2ec76e9bef7e1972cfe69df75fa02117732b82f2ec3f39c6f6ad50c786d8a3`।

## Function / object / element inventory

### `test_totals_use_paid_balances_and_dated_receipts` — L9–L22

`def test_totals_use_paid_balances_and_dated_receipts(self):`

Test/setup helper: test totals use paid balances and dated receipts; নিচের assertions/calls সেই behavior define করে।

### `test_empty_collections_return_zero` — L24–L27

`def test_empty_collections_return_zero(self):`

Test/setup helper: test empty collections return zero; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import unittest
from datetime import datetime
from unittest.mock import patch

from backend.routes import fines


class FineCollectionTests(unittest.TestCase):
    def test_totals_use_paid_balances_and_dated_receipts(self):
        with patch.object(fines, "datetime") as clock, patch.object(fines, "rows") as read:
            clock.now.return_value = datetime(2026, 10, 5)
            read.return_value = [{"total": 1250.5, "today": 100, "month": 450.5}]
            result = fines.get_collection_summary()
        self.assertEqual(result["total"], 1250.5)
        self.assertEqual(result["date"], "2026-10-05")
        self.assertEqual(result["month_start"], "2026-10-01")
        sql = read.call_args.args[0]
        self.assertIn("SUM(paid_amount)", sql)
        self.assertIn("FROM fine_payment", sql)
        self.assertIn("paid_at<ADD_MONTHS", sql)
        self.assertIn("'2026-10-05'", sql)
        self.assertIn("'2026-10-01'", sql)

    def test_empty_collections_return_zero(self):
        with patch.object(fines, "rows", return_value=[{"total": 0, "today": 0, "month": 0}]):
            result = fines.get_collection_summary()
        self.assertEqual([result[key] for key in ("total", "today", "month")], [0, 0, 0])
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>from datetime import datetime</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from backend.routes import fines</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>class FineCollectionTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 9 | <code>    def test_totals_use_paid_balances_and_dated_receipts(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 10 | <code>        with patch.object(fines, &quot;datetime&quot;) as clock, patch.object(fines, &quot;rows&quot;) as read:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_totals_use_paid_balances_and_dated_receipts` অংশে |
| 11 | <code>            clock.now.return_value = datetime(2026, 10, 5)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_totals_use_paid_balances_and_dated_receipts` অংশে |
| 12 | <code>            read.return_value = [{&quot;total&quot;: 1250.5, &quot;today&quot;: 100, &quot;month&quot;: 450.5}]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_totals_use_paid_balances_and_dated_receipts` অংশে |
| 13 | <code>            result = fines.get_collection_summary()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_totals_use_paid_balances_and_dated_receipts` অংশে |
| 14 | <code>        self.assertEqual(result[&quot;total&quot;], 1250.5)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 15 | <code>        self.assertEqual(result[&quot;date&quot;], &quot;2026-10-05&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 16 | <code>        self.assertEqual(result[&quot;month_start&quot;], &quot;2026-10-01&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 17 | <code>        sql = read.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_totals_use_paid_balances_and_dated_receipts` অংশে |
| 18 | <code>        self.assertIn(&quot;SUM(paid_amount)&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 19 | <code>        self.assertIn(&quot;FROM fine_payment&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 20 | <code>        self.assertIn(&quot;paid_at&lt;ADD_MONTHS&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 21 | <code>        self.assertIn(&quot;&#x27;2026-10-05&#x27;&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 22 | <code>        self.assertIn(&quot;&#x27;2026-10-01&#x27;&quot;, sql)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>    def test_empty_collections_return_zero(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 25 | <code>        with patch.object(fines, &quot;rows&quot;, return_value=[{&quot;total&quot;: 0, &quot;today&quot;: 0, &quot;month&quot;: 0}]):</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_empty_collections_return_zero` অংশে |
| 26 | <code>            result = fines.get_collection_summary()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_empty_collections_return_zero` অংশে |
| 27 | <code>        self.assertEqual([result[key] for key in (&quot;total&quot;, &quot;today&quot;, &quot;month&quot;)], [0, 0, 0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
