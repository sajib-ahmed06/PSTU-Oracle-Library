# backend/upgrade_circulation.py

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../backend/upgrade_circulation.py)। Snapshot 2026-10-04; 19 lines; SHA-256 `b3052f0b6c92cbdaf162c7184a5a0e1c6cf3588d87a0d2b1b1a54d9832dca617`।

## Function / object / element inventory

### `main` — L6–L15

`def main():`

এই file-এর entry point; setup/migration flags বা test launcher অনুযায়ী প্রয়োজনীয় workflow শুরু করে। setup_database.py-এর main-এ --migrate preserving upgrade, অন্যথায় RESET confirmation-সহ demo setup।

## সম্পূর্ণ original source

```python
"""Apply the data-preserving circulation upgrade, without running setup/reset."""

from backend.database import ROOT, run_sql


def main():
    print(
        run_sql(
            f'@"{ROOT / "database" / "circulation_upgrade.sql"}"\n@"{ROOT / "database" / "circulation_audit_upgrade.sql"}"\n@"{ROOT / "database" / "reservations_upgrade.sql"}"\n@"{ROOT / "database" / "reservations_audit_upgrade.sql"}"\n@"{ROOT / "database" / "student_activation_upgrade.sql"}"'
        )
    )
    errors = run_sql("SELECT name||':'||line||':'||text FROM user_errors ORDER BY name,sequence;")
    if errors:
        raise RuntimeError(errors)
    print("Circulation upgrade completed; existing data preserved.")


if __name__ == "__main__":
    main()
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Apply the data-preserving circulation upgrade, without running setup/reset.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from backend.database import ROOT, run_sql</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>def main():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 7 | <code>    print(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 8 | <code>        run_sql(</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `main` অংশে |
| 9 | <code>            f&#x27;@&quot;{ROOT / &quot;database&quot; / &quot;circulation_upgrade.sql&quot;}&quot;\n@&quot;{ROOT / &quot;database&quot; / &quot;circulation_audit_upgrade.sql&quot;}&quot;\n@&quot;{ROOT / &quot;database&quot; / &quot;reservations_upgrade.sql&quot;}&quot;\n@&quot;{ROOT / &quot;database&quot; / &quot;reservations_audit_upgrade.sql&quot;}&quot;\n@&quot;{ROOT / &quot;database&quot; / &quot;student_activation_upgrade.sql&quot;}&quot;&#x27;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 10 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 11 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 12 | <code>    errors = run_sql(&quot;SELECT name&#124;&#124;&#x27;:&#x27;&#124;&#124;line&#124;&#124;&#x27;:&#x27;&#124;&#124;text FROM user_errors ORDER BY name,sequence;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `main` অংশে |
| 13 | <code>    if errors:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 14 | <code>        raise RuntimeError(errors)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `main` অংশে |
| 15 | <code>    print(&quot;Circulation upgrade completed; existing data preserved.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>if __name__ == &quot;__main__&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। |
| 19 | <code>    main()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
