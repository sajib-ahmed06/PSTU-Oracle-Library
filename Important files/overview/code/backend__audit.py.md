# backend/audit.py

ContextVar-এ request actor রাখে; একই request-এর database কাজ কে করছে সেই পরিচয় Oracle session-এ পাঠানোর ব্যবস্থা করে।

Source: [মূল file](../../backend/audit.py)। Snapshot 2026-10-04; 5 lines; SHA-256 `5a53bfabaa6bef37a128da6af0d500e56f4981114c5252cf1af6301c4d5175b2`।

## Function / object / element inventory

## সম্পূর্ণ original source

```python
"""Request actor propagation for transactional Oracle audit triggers."""

from contextvars import ContextVar

audit_actor = ContextVar("audit_actor", default="")
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Request actor propagation for transactional Oracle audit triggers.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>from contextvars import ContextVar</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>audit_actor = ContextVar(&quot;audit_actor&quot;, default=&quot;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
