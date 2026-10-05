# tests/test_academic_session.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_academic_session.py)। Snapshot 2026-10-04; 27 lines; SHA-256 `e839fffbc133328e276cae4fae6a643538be2707bfddff6d24bd706664e6b8eb`।

## Function / object / element inventory

### `test_accepts_consecutive_years_and_trims` — L8–L9

`def test_accepts_consecutive_years_and_trims(self):`

Test/setup helper: test accepts consecutive years and trims; নিচের assertions/calls সেই behavior define করে।

### `test_rejects_invalid_formats_and_year_ranges` — L11–L23

`def test_rejects_invalid_formats_and_year_ranges(self):`

Test/setup helper: test rejects invalid formats and year ranges; নিচের assertions/calls সেই behavior define করে।

### `test_short_format_normalizes_and_handles_century_boundary` — L25–L27

`def test_short_format_normalizes_and_handles_century_boundary(self):`

Test/setup helper: test short format normalizes and handles century boundary; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import unittest

from fastapi import HTTPException
from backend.validation import academic_session


class AcademicSessionTests(unittest.TestCase):
    def test_accepts_consecutive_years_and_trims(self):
        self.assertEqual(academic_session(" 2023-2024 "), "2023-2024")

    def test_rejects_invalid_formats_and_year_ranges(self):
        for value in (
            "",
            "2023",
            "2023/2024",
            "2023-2025",
            "2024-2023",
            "２０２３-２０２４",
            "2023-25",
            "9999-00",
        ):
            with self.subTest(value=value), self.assertRaises(HTTPException):
                academic_session(value)

    def test_short_format_normalizes_and_handles_century_boundary(self):
        self.assertEqual(academic_session(" 2023-24 "), "2023-2024")
        self.assertEqual(academic_session("1999-00"), "1999-2000")
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>from backend.validation import academic_session</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>class AcademicSessionTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 8 | <code>    def test_accepts_consecutive_years_and_trims(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 9 | <code>        self.assertEqual(academic_session(&quot; 2023-2024 &quot;), &quot;2023-2024&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>    def test_rejects_invalid_formats_and_year_ranges(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 12 | <code>        for value in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 13 | <code>            &quot;&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 14 | <code>            &quot;2023&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 15 | <code>            &quot;2023/2024&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 16 | <code>            &quot;2023-2025&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 17 | <code>            &quot;2024-2023&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 18 | <code>            &quot;２０２３-２０２４&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 19 | <code>            &quot;2023-25&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 20 | <code>            &quot;9999-00&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 21 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 22 | <code>            with self.subTest(value=value), self.assertRaises(HTTPException):</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 23 | <code>                academic_session(value)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_rejects_invalid_formats_and_year_ranges` অংশে |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>    def test_short_format_normalizes_and_handles_century_boundary(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 26 | <code>        self.assertEqual(academic_session(&quot; 2023-24 &quot;), &quot;2023-2024&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 27 | <code>        self.assertEqual(academic_session(&quot;1999-00&quot;), &quot;1999-2000&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
