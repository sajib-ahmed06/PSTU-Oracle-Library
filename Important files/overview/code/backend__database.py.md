# backend/database.py

Environment ও .env থেকে database configuration নেয়; SQL*Plus subprocess দিয়ে Oracle SQL চালায়; errors-কে HTTP status-এ রূপান্তর এবং delimiter-separated rows-কে dictionaries-এ decode করে।

Source: [মূল file](../../backend/database.py)। Snapshot 2026-10-04; 222 lines; SHA-256 `47336a2f21c3f2a875f2510dbffd6d2c69d31fa8fc80a9ff260b273fc6fc9898`।

## Function / object / element inventory

### `settings` — L27–L37

`def settings():`

.env থাকলে key=value lines পড়ে; process environment দিয়ে override করে। .env না থাকলে environment-এর copy ফেরত দেয়।

### `quote` — L44–L48

`def quote(value):`

SQL string literal-এর apostrophe দ্বিগুণ করে এবং control characters reject করে। এটি prepared/bind query নয়; SQL*Plus string construction helper।

### `run_sql` — L51–L147

`def run_sql(sql, *, read_batch=False):`

Single shared SQL slot নিয়ে Oracle client subprocess চালায়; handler cleanup-এর জন্য 150ms বিরতি দেয়। CONNECT success marker দিয়ে SQL execution শুরু হয়েছে কি না বোঝে; transient connection errors সর্বোচ্চ দুইবার retry। Read-only SELECT known disconnect errors-ও retry করে, executed writes/timeouts replay করে না। Actor, substitution off, rollback ও 20-second command timeout বজায় থাকে।

### `rows` — L150–L156

`def rows(sql, keys, numbers=()):`

SQL execute করে প্রতিটি nonblank line-কে | delimiter দিয়ে ভাগ করে keys-এর সঙ্গে মেলায়; ~ null marker এবং নির্দিষ্ট numeric fields decode করে। Unexpected field count হলে 502।

### `parse_rows` — L159–L172

`def parse_rows(output, keys, numbers=()):`

Decode pipe-delimited output, null markers and typed numeric fields; reject malformed rows.

### `execute_dml` — L175–L177

`def execute_dml(sql):`

DML statement-এর শেষে semicolon এবং COMMIT যোগ করে একই SQL*Plus execution-এ চালায়।

### `collect_reads` — L181–L188

`def collect_reads():`

Request-context-scoped query collector; rows records definitions without SQL execution, then resets the context in finally.

### `read_many` — L191–L222

`def read_many(queries):`

Validate read-only SELECTs, add section markers, run one SQLPlus session, verify complete ordered output and decode each result.

## সম্পূর্ণ original source

```python
"""Oracle SQL*Plus transport and row decoding for Oracle XE 10g."""

import logging
import os
import re
import threading
import time
import subprocess
from pathlib import Path
from contextlib import contextmanager
from contextvars import ContextVar

from fastapi import HTTPException
from backend.audit import audit_actor

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
ORACLE_HOME = Path(os.environ.get("ORACLE_HOME", r"C:\oraclexe\app\oracle\product\10.2.0\server"))
SQLPLUS = ORACLE_HOME / "bin" / "sqlplus.exe"
# Oracle XE 10g has few dedicated handlers; page reads must share a small limit.
SQL_SLOTS = threading.BoundedSemaphore(1)
CONNECT_ERRORS = {"ORA-12516", "ORA-12519", "ORA-12520", "ORA-12541", "ORA-12560", "ORA-12170"}
PENDING_READS = ContextVar("pending_reads", default=None)
READ_ERRORS = CONNECT_ERRORS | {"ORA-03113", "ORA-03114", "ORA-01012", "ORA-12535", "ORA-12537"}


def settings():
    result = {}
    env_file = ROOT / ".env"
    if not env_file.exists():
        return dict(os.environ)
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            result[key.strip()] = value.strip()
    result.update(os.environ)
    return result


config = settings()
LOGIN = f"{config.get('DB_USER', '')}/{config.get('DB_PASSWORD', '')}@{config.get('DB_DSN', 'XE')}"


def quote(value):
    text = "" if value is None else str(value)
    if any(ord(character) < 32 for character in text):
        raise HTTPException(400, "Text fields cannot contain control characters")
    return "'" + text.replace("'", "''") + "'"


def run_sql(sql, *, read_batch=False):
    if not SQLPLUS.exists():
        raise HTTPException(500, "Oracle XE SQL*Plus was not found")
    statement = sql.strip().rstrip(";")
    read_only = (
        read_batch
        or bool(re.match(r"^SELECT\b", statement, re.I))
        and ";" not in statement
        and not re.search(r"\bFOR\s+UPDATE\b", statement, re.I)
    )
    actor = audit_actor.get()
    actor_statement = (
        f"BEGIN DBMS_APPLICATION_INFO.SET_CLIENT_INFO({quote(actor)}); END;\n/\n" if actor else ""
    )
    sql = actor_statement + sql
    script = f"SET DEFINE OFF\nSET SQLBLANKLINES ON\nSET HEADING OFF FEEDBACK OFF PAGESIZE 0 LINESIZE 32767 TRIMSPOOL ON TAB OFF VERIFY OFF ECHO OFF\nWHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\n{sql}\nEXIT\n"
    environment = os.environ.copy()
    for key in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "http_proxy",
        "https_proxy",
        "no_proxy",
    ):
        environment.pop(key, None)
    environment["TNS_ADMIN"] = str(ROOT / "backend" / "oracle_config")
    environment["ORACLE_HOME"] = str(ORACLE_HOME)
    environment["PATH"] = str(ORACLE_HOME / "bin") + os.pathsep + environment.get("PATH", "")
    environment["NLS_LANG"] = "AMERICAN_AMERICA.WE8MSWIN1252"
    # Fail before executing SQL when CONNECT is rejected. Only then is retrying a
    # mutation safe; a timeout/disconnect after execution has an unknown outcome.
    connection = (
        "WHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\nCONNECT "
        + LOGIN
        + "\nPROMPT __LIBRARY_CONNECTED__\n"
    )
    for attempt in range(3):
        if not SQL_SLOTS.acquire(timeout=30):
            raise HTTPException(503, "Database is busy. Please try again shortly")
        try:
            result = subprocess.run(
                [str(SQLPLUS), "-S", "-L", "/nolog"],
                input=connection + script,
                text=True,
                capture_output=True,
                env=environment,
                cwd=ROOT,
                timeout=20,
            )
        except OSError as error:
            logging.getLogger(__name__).error("SQL*Plus could not start: %s", error)
            raise HTTPException(503, "Database client could not start")
        except subprocess.TimeoutExpired:
            raise HTTPException(504, "Oracle database did not respond in time")
        finally:
            # Let XE retire its dedicated handler before opening the next one.
            time.sleep(0.15)
            SQL_SLOTS.release()
        output_lines = (result.stdout + result.stderr).splitlines()
        connected = "__LIBRARY_CONNECTED__" in output_lines
        if connected:
            output_lines.remove("__LIBRARY_CONNECTED__")
        output = "\n".join(output_lines).strip()
        errors = [
            line.strip()
            for line in output.splitlines()
            if re.match(r"^(?:ORA|SP2)-\d+:", line.strip())
        ]
        if not result.returncode and not errors:
            return output
        message = errors[0] if errors else "Oracle command failed"
        code = message.split(":", 1)[0]
        if attempt < 2 and (
            (not connected and code in CONNECT_ERRORS) or (read_only and code in READ_ERRORS)
        ):
            logging.getLogger(__name__).warning(
                "Retrying transient Oracle connection error: %s", code
            )
            time.sleep(1 + attempt)
            continue
        break
    if result.returncode or errors:
        if "ORA-00001" in message:
            if "UQ_STUDENT_ROLL" in message:
                raise HTTPException(409, "ID/Roll number is already registered")
            if "UQ_STUDENT_REGISTRATION" in message:
                raise HTTPException(409, "Registration number is already registered")
            raise HTTPException(409, "A record with these details already exists")
        if "ORA-01403" in message:
            raise HTTPException(404, "The requested record was not found")
        if "ORA-200" in message:
            raise HTTPException(409, message.split(":", 1)[-1].strip())
        logging.getLogger(__name__).error("Oracle command failed: %s", message)
        raise HTTPException(503, "Database request failed. Please try again later")
    return output


def rows(sql, keys, numbers=()):
    pending = PENDING_READS.get()
    if pending is not None:
        pending.append((sql, keys, numbers))
        return []
    output = run_sql(sql.rstrip(";") + ";")
    return parse_rows(output, keys, numbers)


def parse_rows(output, keys, numbers=()):
    data = []
    for line in output.splitlines():
        if not line.strip():
            continue
        values = line.strip().split("|")
        if len(values) != len(keys):
            raise HTTPException(502, "The database returned an unexpected row format")
        item = dict(zip(keys, (None if value == "~" else value for value in values)))
        for key in numbers:
            if item.get(key) is not None:
                item[key] = float(item[key]) if "." in str(item[key]) else int(item[key])
        data.append(item)
    return data


def execute_dml(sql):
    statement = sql.rstrip().rstrip(";")
    run_sql(f"{statement};\nCOMMIT;")


@contextmanager
def collect_reads():
    """Collect existing read-query definitions without opening any connection."""
    queries = []
    token = PENDING_READS.set(queries)
    try:
        yield queries
    finally:
        PENDING_READS.reset(token)


def read_many(queries):
    """Execute read-only queries in one SQLPlus connection and decode each section."""
    script = []
    for index, (sql, keys, numbers) in enumerate(queries):
        statement = sql.strip().rstrip(";")
        if (
            not re.match(r"^SELECT\b", statement, re.I)
            or ";" in statement
            or re.search(r"\bFOR\s+UPDATE\b", statement, re.I)
        ):
            raise ValueError("Only read-only SELECT statements can be batched")
        script.extend((f"PROMPT __LIBRARY_READ_{index}__", statement + ";"))
    output = run_sql("\n".join(script), read_batch=True)
    sections = [[] for _ in queries]
    active = None
    for line in output.splitlines():
        marker = re.fullmatch(r"__LIBRARY_READ_(\d+)__", line.strip())
        if marker:
            index = int(marker.group(1))
            if index != (0 if active is None else active + 1) or index >= len(queries):
                raise HTTPException(502, "Unexpected database batch section")
            active = index
        elif active is not None:
            sections[active].append(line)
        elif line.strip():
            raise HTTPException(502, "Unexpected database batch output")
    if queries and active != len(queries) - 1:
        raise HTTPException(502, "Database batch returned incomplete results")
    return [
        parse_rows("\n".join(lines), keys, numbers)
        for lines, (_, keys, numbers) in zip(sections, queries)
    ]
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Oracle SQL*Plus transport and row decoding for Oracle XE 10g.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import logging</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import os</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>import threading</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>import time</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>import subprocess</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from pathlib import Path</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from contextlib import contextmanager</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from contextvars import ContextVar</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>from fastapi import HTTPException</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 14 | <code>from backend.audit import audit_actor</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>ROOT = Path(__file__).resolve().parent.parent</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 17 | <code>FRONTEND = ROOT / &quot;frontend&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 18 | <code>ORACLE_HOME = Path(os.environ.get(&quot;ORACLE_HOME&quot;, r&quot;C:\oraclexe\app\oracle\product\10.2.0\server&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 19 | <code>SQLPLUS = ORACLE_HOME / &quot;bin&quot; / &quot;sqlplus.exe&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 20 | <code># Oracle XE 10g has few dedicated handlers; page reads must share a small limit.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 21 | <code>SQL_SLOTS = threading.BoundedSemaphore(1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 22 | <code>CONNECT_ERRORS = {&quot;ORA-12516&quot;, &quot;ORA-12519&quot;, &quot;ORA-12520&quot;, &quot;ORA-12541&quot;, &quot;ORA-12560&quot;, &quot;ORA-12170&quot;}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 23 | <code>PENDING_READS = ContextVar(&quot;pending_reads&quot;, default=None)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 24 | <code>READ_ERRORS = CONNECT_ERRORS &#124; {&quot;ORA-03113&quot;, &quot;ORA-03114&quot;, &quot;ORA-01012&quot;, &quot;ORA-12535&quot;, &quot;ORA-12537&quot;}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 25 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 26 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 27 | <code>def settings():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 28 | <code>    result = {}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `settings` অংশে |
| 29 | <code>    env_file = ROOT / &quot;.env&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `settings` অংশে |
| 30 | <code>    if not env_file.exists():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `settings` অংশে |
| 31 | <code>        return dict(os.environ)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `settings` অংশে |
| 32 | <code>    for line in env_file.read_text(encoding=&quot;utf-8&quot;).splitlines():</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `settings` অংশে |
| 33 | <code>        if &quot;=&quot; in line and not line.startswith(&quot;#&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `settings` অংশে |
| 34 | <code>            key, value = line.split(&quot;=&quot;, 1)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `settings` অংশে |
| 35 | <code>            result[key.strip()] = value.strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `settings` অংশে |
| 36 | <code>    result.update(os.environ)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `settings` অংশে |
| 37 | <code>    return result</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `settings` অংশে |
| 38 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 39 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 40 | <code>config = settings()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 41 | <code>LOGIN = f&quot;{config.get(&#x27;DB_USER&#x27;, &#x27;&#x27;)}/{config.get(&#x27;DB_PASSWORD&#x27;, &#x27;&#x27;)}@{config.get(&#x27;DB_DSN&#x27;, &#x27;XE&#x27;)}&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 42 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 43 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 44 | <code>def quote(value):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 45 | <code>    text = &quot;&quot; if value is None else str(value)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `quote` অংশে |
| 46 | <code>    if any(ord(character) &lt; 32 for character in text):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `quote` অংশে |
| 47 | <code>        raise HTTPException(400, &quot;Text fields cannot contain control characters&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `quote` অংশে |
| 48 | <code>    return &quot;&#x27;&quot; + text.replace(&quot;&#x27;&quot;, &quot;&#x27;&#x27;&quot;) + &quot;&#x27;&quot;</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `quote` অংশে |
| 49 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 50 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 51 | <code>def run_sql(sql, *, read_batch=False):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 52 | <code>    if not SQLPLUS.exists():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 53 | <code>        raise HTTPException(500, &quot;Oracle XE SQL*Plus was not found&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 54 | <code>    statement = sql.strip().rstrip(&quot;;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 55 | <code>    read_only = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 56 | <code>        read_batch</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 57 | <code>        or bool(re.match(r&quot;^SELECT\b&quot;, statement, re.I))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 58 | <code>        and &quot;;&quot; not in statement</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 59 | <code>        and not re.search(r&quot;\bFOR\s+UPDATE\b&quot;, statement, re.I)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 60 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 61 | <code>    actor = audit_actor.get()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 62 | <code>    actor_statement = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 63 | <code>        f&quot;BEGIN DBMS_APPLICATION_INFO.SET_CLIENT_INFO({quote(actor)}); END;\n/\n&quot; if actor else &quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 64 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 65 | <code>    sql = actor_statement + sql</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 66 | <code>    script = f&quot;SET DEFINE OFF\nSET SQLBLANKLINES ON\nSET HEADING OFF FEEDBACK OFF PAGESIZE 0 LINESIZE 32767 TRIMSPOOL ON TAB OFF VERIFY OFF ECHO OFF\nWHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\n{sql}\nEXIT\n&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 67 | <code>    environment = os.environ.copy()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 68 | <code>    for key in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `run_sql` অংশে |
| 69 | <code>        &quot;HTTP_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 70 | <code>        &quot;HTTPS_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 71 | <code>        &quot;ALL_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 72 | <code>        &quot;NO_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 73 | <code>        &quot;http_proxy&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 74 | <code>        &quot;https_proxy&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 75 | <code>        &quot;no_proxy&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 76 | <code>    ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 77 | <code>        environment.pop(key, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 78 | <code>    environment[&quot;TNS_ADMIN&quot;] = str(ROOT / &quot;backend&quot; / &quot;oracle_config&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 79 | <code>    environment[&quot;ORACLE_HOME&quot;] = str(ORACLE_HOME)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 80 | <code>    environment[&quot;PATH&quot;] = str(ORACLE_HOME / &quot;bin&quot;) + os.pathsep + environment.get(&quot;PATH&quot;, &quot;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 81 | <code>    environment[&quot;NLS_LANG&quot;] = &quot;AMERICAN_AMERICA.WE8MSWIN1252&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 82 | <code>    # Fail before executing SQL when CONNECT is rejected. Only then is retrying a</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 83 | <code>    # mutation safe; a timeout/disconnect after execution has an unknown outcome.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 84 | <code>    connection = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 85 | <code>        &quot;WHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\nCONNECT &quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 86 | <code>        + LOGIN</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 87 | <code>        + &quot;\nPROMPT __LIBRARY_CONNECTED__\n&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 88 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 89 | <code>    for attempt in range(3):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `run_sql` অংশে |
| 90 | <code>        if not SQL_SLOTS.acquire(timeout=30):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 91 | <code>            raise HTTPException(503, &quot;Database is busy. Please try again shortly&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 92 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_sql` অংশে |
| 93 | <code>            result = subprocess.run(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 94 | <code>                [str(SQLPLUS), &quot;-S&quot;, &quot;-L&quot;, &quot;/nolog&quot;],</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 95 | <code>                input=connection + script,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 96 | <code>                text=True,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 97 | <code>                capture_output=True,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 98 | <code>                env=environment,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 99 | <code>                cwd=ROOT,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 100 | <code>                timeout=20,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 101 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 102 | <code>        except OSError as error:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_sql` অংশে |
| 103 | <code>            logging.getLogger(__name__).error(&quot;SQL*Plus could not start: %s&quot;, error)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 104 | <code>            raise HTTPException(503, &quot;Database client could not start&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 105 | <code>        except subprocess.TimeoutExpired:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_sql` অংশে |
| 106 | <code>            raise HTTPException(504, &quot;Oracle database did not respond in time&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 107 | <code>        finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_sql` অংশে |
| 108 | <code>            # Let XE retire its dedicated handler before opening the next one.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 109 | <code>            time.sleep(0.15)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 110 | <code>            SQL_SLOTS.release()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 111 | <code>        output_lines = (result.stdout + result.stderr).splitlines()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 112 | <code>        connected = &quot;__LIBRARY_CONNECTED__&quot; in output_lines</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 113 | <code>        if connected:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 114 | <code>            output_lines.remove(&quot;__LIBRARY_CONNECTED__&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 115 | <code>        output = &quot;\n&quot;.join(output_lines).strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 116 | <code>        errors = [</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 117 | <code>            line.strip()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 118 | <code>            for line in output.splitlines()</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `run_sql` অংশে |
| 119 | <code>            if re.match(r&quot;^(?:ORA&#124;SP2)-\d+:&quot;, line.strip())</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 120 | <code>        ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 121 | <code>        if not result.returncode and not errors:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 122 | <code>            return output</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `run_sql` অংশে |
| 123 | <code>        message = errors[0] if errors else &quot;Oracle command failed&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 124 | <code>        code = message.split(&quot;:&quot;, 1)[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_sql` অংশে |
| 125 | <code>        if attempt &lt; 2 and (</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 126 | <code>            (not connected and code in CONNECT_ERRORS) or (read_only and code in READ_ERRORS)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 127 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 128 | <code>            logging.getLogger(__name__).warning(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 129 | <code>                &quot;Retrying transient Oracle connection error: %s&quot;, code</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 130 | <code>            )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 131 | <code>            time.sleep(1 + attempt)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 132 | <code>            continue</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 133 | <code>        break</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 134 | <code>    if result.returncode or errors:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 135 | <code>        if &quot;ORA-00001&quot; in message:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 136 | <code>            if &quot;UQ_STUDENT_ROLL&quot; in message:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 137 | <code>                raise HTTPException(409, &quot;ID/Roll number is already registered&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 138 | <code>            if &quot;UQ_STUDENT_REGISTRATION&quot; in message:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 139 | <code>                raise HTTPException(409, &quot;Registration number is already registered&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 140 | <code>            raise HTTPException(409, &quot;A record with these details already exists&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 141 | <code>        if &quot;ORA-01403&quot; in message:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 142 | <code>            raise HTTPException(404, &quot;The requested record was not found&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 143 | <code>        if &quot;ORA-200&quot; in message:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_sql` অংশে |
| 144 | <code>            raise HTTPException(409, message.split(&quot;:&quot;, 1)[-1].strip())</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 145 | <code>        logging.getLogger(__name__).error(&quot;Oracle command failed: %s&quot;, message)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_sql` অংশে |
| 146 | <code>        raise HTTPException(503, &quot;Database request failed. Please try again later&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `run_sql` অংশে |
| 147 | <code>    return output</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `run_sql` অংশে |
| 148 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 149 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 150 | <code>def rows(sql, keys, numbers=()):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 151 | <code>    pending = PENDING_READS.get()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `rows` অংশে |
| 152 | <code>    if pending is not None:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `rows` অংশে |
| 153 | <code>        pending.append((sql, keys, numbers))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `rows` অংশে |
| 154 | <code>        return []</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `rows` অংশে |
| 155 | <code>    output = run_sql(sql.rstrip(&quot;;&quot;) + &quot;;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `rows` অংশে |
| 156 | <code>    return parse_rows(output, keys, numbers)</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `rows` অংশে |
| 157 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 158 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 159 | <code>def parse_rows(output, keys, numbers=()):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 160 | <code>    data = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `parse_rows` অংশে |
| 161 | <code>    for line in output.splitlines():</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `parse_rows` অংশে |
| 162 | <code>        if not line.strip():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `parse_rows` অংশে |
| 163 | <code>            continue</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `parse_rows` অংশে |
| 164 | <code>        values = line.strip().split(&quot;&#124;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `parse_rows` অংশে |
| 165 | <code>        if len(values) != len(keys):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `parse_rows` অংশে |
| 166 | <code>            raise HTTPException(502, &quot;The database returned an unexpected row format&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `parse_rows` অংশে |
| 167 | <code>        item = dict(zip(keys, (None if value == &quot;~&quot; else value for value in values)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `parse_rows` অংশে |
| 168 | <code>        for key in numbers:</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `parse_rows` অংশে |
| 169 | <code>            if item.get(key) is not None:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `parse_rows` অংশে |
| 170 | <code>                item[key] = float(item[key]) if &quot;.&quot; in str(item[key]) else int(item[key])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `parse_rows` অংশে |
| 171 | <code>        data.append(item)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `parse_rows` অংশে |
| 172 | <code>    return data</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `parse_rows` অংশে |
| 173 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 174 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 175 | <code>def execute_dml(sql):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 176 | <code>    statement = sql.rstrip().rstrip(&quot;;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute_dml` অংশে |
| 177 | <code>    run_sql(f&quot;{statement};\nCOMMIT;&quot;)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `execute_dml` অংশে |
| 178 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 179 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 180 | <code>@contextmanager</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 181 | <code>def collect_reads():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 182 | <code>    &quot;&quot;&quot;Collect existing read-query definitions without opening any connection.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `collect_reads` অংশে |
| 183 | <code>    queries = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `collect_reads` অংশে |
| 184 | <code>    token = PENDING_READS.set(queries)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `collect_reads` অংশে |
| 185 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `collect_reads` অংশে |
| 186 | <code>        yield queries</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `collect_reads` অংশে |
| 187 | <code>    finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `collect_reads` অংশে |
| 188 | <code>        PENDING_READS.reset(token)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `collect_reads` অংশে |
| 189 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 190 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 191 | <code>def read_many(queries):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 192 | <code>    &quot;&quot;&quot;Execute read-only queries in one SQLPlus connection and decode each section.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 193 | <code>    script = []</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 194 | <code>    for index, (sql, keys, numbers) in enumerate(queries):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `read_many` অংশে |
| 195 | <code>        statement = sql.strip().rstrip(&quot;;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 196 | <code>        if (</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `read_many` অংশে |
| 197 | <code>            not re.match(r&quot;^SELECT\b&quot;, statement, re.I)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 198 | <code>            or &quot;;&quot; in statement</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 199 | <code>            or re.search(r&quot;\bFOR\s+UPDATE\b&quot;, statement, re.I)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 200 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 201 | <code>            raise ValueError(&quot;Only read-only SELECT statements can be batched&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `read_many` অংশে |
| 202 | <code>        script.extend((f&quot;PROMPT __LIBRARY_READ_{index}__&quot;, statement + &quot;;&quot;))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 203 | <code>    output = run_sql(&quot;\n&quot;.join(script), read_batch=True)</code> | Constructed SQL database helper-এ পাঠায়; transaction/Oracle errors helper দিয়ে handle হয়। `read_many` অংশে |
| 204 | <code>    sections = [[] for _ in queries]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 205 | <code>    active = None</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 206 | <code>    for line in output.splitlines():</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `read_many` অংশে |
| 207 | <code>        marker = re.fullmatch(r&quot;__LIBRARY_READ_(\d+)__&quot;, line.strip())</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 208 | <code>        if marker:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `read_many` অংশে |
| 209 | <code>            index = int(marker.group(1))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 210 | <code>            if index != (0 if active is None else active + 1) or index &gt;= len(queries):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `read_many` অংশে |
| 211 | <code>                raise HTTPException(502, &quot;Unexpected database batch section&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `read_many` অংশে |
| 212 | <code>            active = index</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `read_many` অংশে |
| 213 | <code>        elif active is not None:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `read_many` অংশে |
| 214 | <code>            sections[active].append(line)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
| 215 | <code>        elif line.strip():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `read_many` অংশে |
| 216 | <code>            raise HTTPException(502, &quot;Unexpected database batch output&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `read_many` অংশে |
| 217 | <code>    if queries and active != len(queries) - 1:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `read_many` অংশে |
| 218 | <code>        raise HTTPException(502, &quot;Database batch returned incomplete results&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `read_many` অংশে |
| 219 | <code>    return [</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `read_many` অংশে |
| 220 | <code>        parse_rows(&quot;\n&quot;.join(lines), keys, numbers)</code> | SELECT result named dictionary rows হিসেবে নেওয়ার call শুরু/চালায়। `read_many` অংশে |
| 221 | <code>        for lines, (_, keys, numbers) in zip(sections, queries)</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `read_many` অংশে |
| 222 | <code>    ]</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `read_many` অংশে |
