# backend/setup_database.py

Windows SQL*Plus দিয়ে SYSDBA/bootstrap, sample database reset অথবা existing database migration চালায়।

Source: [মূল file](../../backend/setup_database.py)। Snapshot 2026-10-04; 114 lines; SHA-256 `acd2963e49f85a843cf366f00fb6ad07983536b49c2f7d7c0858983b0ff1c515`।

## Function / object / element inventory

### `oracle_environment` — L15–L38

`def oracle_environment(use_local_auth=False):`

Oracle home/SID/client language/PATH বসায় এবং proxy settings বাদ দেয়; local SYSDBA mode-এ TNS_ADMIN বাদ দেয়।

### `execute` — L41–L59

`def execute(login, script_path, use_local_auth=False, initialization=""):`

SQL*Plus /nolog subprocess-এ CONNECT এবং script পাঠায়; 120-second timeout/OS errors friendly failure message দেয়; command-line arguments-এ password দেয় না।

### `main` — L62–L110

`def main():`

এই file-এর entry point; setup/migration flags বা test launcher অনুযায়ী প্রয়োজনীয় workflow শুরু করে। setup_database.py-এর main-এ --migrate preserving upgrade, অন্যথায় RESET confirmation-সহ demo setup।

### `bind` — L88–L90

`def bind(name, value):`

Test/setup helper: bind; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import getpass
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
ORACLE_HOME = Path(os.environ.get("ORACLE_HOME", r"C:\oraclexe\app\oracle\product\10.2.0\server"))
SQLPLUS = ORACLE_HOME / "bin" / "sqlplus.exe"
TNS_ADMIN = ROOT / "backend" / "oracle_config"


def oracle_environment(use_local_auth=False):
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

    environment["ORACLE_HOME"] = str(ORACLE_HOME)
    environment["ORACLE_SID"] = "XE"
    environment["NLS_LANG"] = "AMERICAN_AMERICA.WE8MSWIN1252"
    environment["PATH"] = str(ORACLE_HOME / "bin") + os.pathsep + environment.get("PATH", "")

    if use_local_auth:
        environment.pop("TNS_ADMIN", None)
    else:
        environment["TNS_ADMIN"] = str(TNS_ADMIN)

    return environment


def execute(login, script_path, use_local_auth=False, initialization=""):
    command = [str(SQLPLUS), "-L", "/nolog"]
    script = f'SET ECHO OFF\nSET VERIFY OFF\nSET DEFINE OFF\nWHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\nCONNECT {login}\n{initialization}\n@"{script_path}"\nEXIT\n'
    try:
        result = subprocess.run(
            command,
            input=script,
            text=True,
            env=oracle_environment(use_local_auth),
            cwd=ROOT,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        print("Database setup timed out. Check the Oracle service and try again.")
        return False
    except OSError as error:
        print(f"Could not start SQL*Plus: {error}")
        return False
    return result.returncode == 0


def main():
    print("This setup deletes existing library tables and loads sample records.")
    if input("Type RESET to continue: ").strip() != "RESET":
        print("Setup cancelled.")
        return 1
    if not SQLPLUS.exists():
        print(f"Oracle SQL*Plus was not found: {SQLPLUS}")
        return 1

    print("\nPSTU Library Database Setup")
    print("---------------------------")
    from backend.database import settings
    from backend.auth.passwords import hash_password

    config = settings()
    username = config.get("DB_USER", "")
    db_password = config.get("DB_PASSWORD", "")
    dsn = config.get("DB_DSN", "XE")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,29}", username) or not re.fullmatch(r"[A-Za-z0-9_#]{1,30}", db_password):
        print("Set DB_USER and DB_PASSWORD in your private .env first (Oracle identifiers and a password using letters, numbers, _ or #).")
        return 1
    admin_username = input("Choose the initial administrator username: ").strip()
    admin_password = getpass.getpass("Choose the initial administrator password (at least 8 characters): ")
    if not admin_username or len(admin_password) < 8 or any(ord(c) < 32 for c in admin_username):
        print("A username and a password of at least 8 characters are required.")
        return 1
    def bind(name, value):
        escaped = value.replace("'", "''")
        return f"VARIABLE {name} VARCHAR2(4000)\nBEGIN :{name} := '{escaped}'; END;\n/\n"
    bootstrap_values = bind("bootstrap_user", username.upper()) + bind("bootstrap_password", db_password)
    seed_values = bind("seed_admin_username", admin_username) + bind("seed_admin_password", hash_password(admin_password))
    print("Trying Windows SYSDBA authentication...")

    bootstrap = ROOT / "database" / "bootstrap.sql"
    if not execute("/ as sysdba", bootstrap, use_local_auth=True, initialization=bootstrap_values):
        print("\nWindows SYSDBA login is unavailable.")
        password = getpass.getpass("Enter the Oracle SYSTEM password: ")
        if not password or not execute(f"system/{password}@{dsn}", bootstrap, initialization=bootstrap_values):
            print("\nCould not create the configured application schema. Read the Oracle error above.")
            return 1

    print("\nLoading tables and sample data...")
    setup = ROOT / "database" / "setup.sql"
    if not execute(f"{username}/{db_password}@{dsn}", setup, initialization=seed_values):
        print("\nDatabase tables could not be created.")
        return 1

    print("\nDatabase setup completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import getpass</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>import os</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import subprocess</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>import sys</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>from pathlib import Path</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>ROOT = Path(__file__).resolve().parent.parent</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 9 | <code>sys.path.insert(0, str(ROOT))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 10 | <code>ORACLE_HOME = Path(os.environ.get(&quot;ORACLE_HOME&quot;, r&quot;C:\oraclexe\app\oracle\product\10.2.0\server&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 11 | <code>SQLPLUS = ORACLE_HOME / &quot;bin&quot; / &quot;sqlplus.exe&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 12 | <code>TNS_ADMIN = ROOT / &quot;backend&quot; / &quot;oracle_config&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 15 | <code>def oracle_environment(use_local_auth=False):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 16 | <code>    environment = os.environ.copy()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `oracle_environment` অংশে |
| 17 | <code>    for key in (</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `oracle_environment` অংশে |
| 18 | <code>        &quot;HTTP_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 19 | <code>        &quot;HTTPS_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 20 | <code>        &quot;ALL_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 21 | <code>        &quot;NO_PROXY&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 22 | <code>        &quot;http_proxy&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 23 | <code>        &quot;https_proxy&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 24 | <code>        &quot;no_proxy&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 25 | <code>    ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 26 | <code>        environment.pop(key, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>    environment[&quot;ORACLE_HOME&quot;] = str(ORACLE_HOME)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `oracle_environment` অংশে |
| 29 | <code>    environment[&quot;ORACLE_SID&quot;] = &quot;XE&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `oracle_environment` অংশে |
| 30 | <code>    environment[&quot;NLS_LANG&quot;] = &quot;AMERICAN_AMERICA.WE8MSWIN1252&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `oracle_environment` অংশে |
| 31 | <code>    environment[&quot;PATH&quot;] = str(ORACLE_HOME / &quot;bin&quot;) + os.pathsep + environment.get(&quot;PATH&quot;, &quot;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `oracle_environment` অংশে |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>    if use_local_auth:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `oracle_environment` অংশে |
| 34 | <code>        environment.pop(&quot;TNS_ADMIN&quot;, None)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `oracle_environment` অংশে |
| 35 | <code>    else:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `oracle_environment` অংশে |
| 36 | <code>        environment[&quot;TNS_ADMIN&quot;] = str(TNS_ADMIN)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `oracle_environment` অংশে |
| 37 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 38 | <code>    return environment</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `oracle_environment` অংশে |
| 39 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 40 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 41 | <code>def execute(login, script_path, use_local_auth=False, initialization=&quot;&quot;):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 42 | <code>    command = [str(SQLPLUS), &quot;-L&quot;, &quot;/nolog&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 43 | <code>    script = f&#x27;SET ECHO OFF\nSET VERIFY OFF\nSET DEFINE OFF\nWHENEVER OSERROR EXIT FAILURE\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\nCONNECT {login}\n{initialization}\n@&quot;{script_path}&quot;\nEXIT\n&#x27;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 44 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `execute` অংশে |
| 45 | <code>        result = subprocess.run(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 46 | <code>            command,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `execute` অংশে |
| 47 | <code>            input=script,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 48 | <code>            text=True,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 49 | <code>            env=oracle_environment(use_local_auth),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 50 | <code>            cwd=ROOT,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 51 | <code>            timeout=120,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `execute` অংশে |
| 52 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `execute` অংশে |
| 53 | <code>    except subprocess.TimeoutExpired:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `execute` অংশে |
| 54 | <code>        print(&quot;Database setup timed out. Check the Oracle service and try again.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `execute` অংশে |
| 55 | <code>        return False</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `execute` অংশে |
| 56 | <code>    except OSError as error:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `execute` অংশে |
| 57 | <code>        print(f&quot;Could not start SQL*Plus: {error}&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `execute` অংশে |
| 58 | <code>        return False</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `execute` অংশে |
| 59 | <code>    return result.returncode == 0</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `execute` অংশে |
| 60 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 61 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 62 | <code>def main():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 63 | <code>    print(&quot;This setup deletes existing library tables and loads sample records.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 64 | <code>    if input(&quot;Type RESET to continue: &quot;).strip() != &quot;RESET&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 65 | <code>        print(&quot;Setup cancelled.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 66 | <code>        return 1</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 67 | <code>    if not SQLPLUS.exists():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 68 | <code>        print(f&quot;Oracle SQL*Plus was not found: {SQLPLUS}&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 69 | <code>        return 1</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 70 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 71 | <code>    print(&quot;\nPSTU Library Database Setup&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 72 | <code>    print(&quot;---------------------------&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 73 | <code>    from backend.database import settings</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 74 | <code>    from backend.auth.passwords import hash_password</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 75 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 76 | <code>    config = settings()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 77 | <code>    username = config.get(&quot;DB_USER&quot;, &quot;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 78 | <code>    db_password = config.get(&quot;DB_PASSWORD&quot;, &quot;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 79 | <code>    dsn = config.get(&quot;DB_DSN&quot;, &quot;XE&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 80 | <code>    if not re.fullmatch(r&quot;[A-Za-z][A-Za-z0-9_]{0,29}&quot;, username) or not re.fullmatch(r&quot;[A-Za-z0-9_#]{1,30}&quot;, db_password):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 81 | <code>        print(&quot;Set DB_USER and DB_PASSWORD in your private .env first (Oracle identifiers and a password using letters, numbers, _ or #).&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 82 | <code>        return 1</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 83 | <code>    admin_username = input(&quot;Choose the initial administrator username: &quot;).strip()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 84 | <code>    admin_password = getpass.getpass(&quot;Choose the initial administrator password (at least 8 characters): &quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 85 | <code>    if not admin_username or len(admin_password) &lt; 8 or any(ord(c) &lt; 32 for c in admin_username):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 86 | <code>        print(&quot;A username and a password of at least 8 characters are required.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 87 | <code>        return 1</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 88 | <code>    def bind(name, value):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 89 | <code>        escaped = value.replace(&quot;&#x27;&quot;, &quot;&#x27;&#x27;&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `bind` অংশে |
| 90 | <code>        return f&quot;VARIABLE {name} VARCHAR2(4000)\nBEGIN :{name} := &#x27;{escaped}&#x27;; END;\n/\n&quot;</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `bind` অংশে |
| 91 | <code>    bootstrap_values = bind(&quot;bootstrap_user&quot;, username.upper()) + bind(&quot;bootstrap_password&quot;, db_password)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 92 | <code>    seed_values = bind(&quot;seed_admin_username&quot;, admin_username) + bind(&quot;seed_admin_password&quot;, hash_password(admin_password))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 93 | <code>    print(&quot;Trying Windows SYSDBA authentication...&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 94 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 95 | <code>    bootstrap = ROOT / &quot;database&quot; / &quot;bootstrap.sql&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 96 | <code>    if not execute(&quot;/ as sysdba&quot;, bootstrap, use_local_auth=True, initialization=bootstrap_values):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 97 | <code>        print(&quot;\nWindows SYSDBA login is unavailable.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 98 | <code>        password = getpass.getpass(&quot;Enter the Oracle SYSTEM password: &quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 99 | <code>        if not password or not execute(f&quot;system/{password}@{dsn}&quot;, bootstrap, initialization=bootstrap_values):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 100 | <code>            print(&quot;\nCould not create the configured application schema. Read the Oracle error above.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 101 | <code>            return 1</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 102 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 103 | <code>    print(&quot;\nLoading tables and sample data...&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 104 | <code>    setup = ROOT / &quot;database&quot; / &quot;setup.sql&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 105 | <code>    if not execute(f&quot;{username}/{db_password}@{dsn}&quot;, setup, initialization=seed_values):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 106 | <code>        print(&quot;\nDatabase tables could not be created.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 107 | <code>        return 1</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 108 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 109 | <code>    print(&quot;\nDatabase setup completed successfully.&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 110 | <code>    return 0</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `main` অংশে |
| 111 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 112 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 113 | <code>if __name__ == &quot;__main__&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। |
| 114 | <code>    sys.exit(main())</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
