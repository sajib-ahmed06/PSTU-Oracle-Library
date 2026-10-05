# backend/reminders/worker.py

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../backend/reminders/worker.py)। Snapshot 2026-10-04; 115 lines; SHA-256 `2b27861576a7fa9b726dba53c5a8d700e537b25abbcc903fecc9e9716dce0bae`।

## Function / object / element inventory

### `prepare_message` — L17–L27

`def prepare_message(loan, today=None, settings=None):`

Test/setup helper: prepare message; নিচের assertions/calls সেই behavior define করে।

### `run_once` — L30–L62

`def run_once(settings=None, stop=None):`

Test/setup helper: run once; নিচের assertions/calls সেই behavior define করে।

### `loop` — L65–L73

`def loop(stop):`

Test/setup helper: loop; নিচের assertions/calls সেই behavior define করে।

### `lifespan` — L77–L88

`async def lifespan(app):`

Test/setup helper: lifespan; নিচের assertions/calls সেই behavior define করে।

### `main` — L91–L111

`def main():`

এই file-এর entry point; setup/migration flags বা test launcher অনুযায়ী প্রয়োজনীয় workflow শুরু করে। setup_database.py-এর main-এ --migrate preserving upgrade, অন্যথায় RESET confirmation-সহ demo setup।

## সম্পূর্ণ original source

```python
"""Scheduled delivery while the app runs; a CLI supports an external scheduler."""

import argparse
import asyncio
import logging
import threading
from contextlib import asynccontextmanager
from datetime import datetime

from backend.database import config
from . import providers, store
from .messages import DHAKA, reminder_for

logger = logging.getLogger(__name__)


def prepare_message(loan, today=None, settings=None):
    settings = settings or config
    message = reminder_for(loan, today)
    if message and message["channel"] == "SMS":
        channel = settings.get("DUE_REMINDER_CHANNEL", "email").upper()
        if channel not in {"SMS", "EMAIL"}:
            raise ValueError("DUE_REMINDER_CHANNEL must be sms or email")
        message["channel"] = channel
        if channel == "EMAIL":
            message["recipient"] = loan["email"]
    return message


def run_once(settings=None, stop=None):
    settings = settings or config
    if settings.get("REMINDERS_ENABLED", "false").lower() != "true":
        return
    if not any(providers.ready(channel, settings) for channel in ("SMS", "EMAIL")):
        return
    now = datetime.now(DHAKA)
    if now.hour < int(settings.get("REMINDER_SEND_HOUR", "9")):
        return
    store.recover_abandoned()
    for loan in store.loans():
        if stop and stop.is_set():
            break
        message = prepare_message(loan, now.date(), settings)
        if not message or not providers.ready(message["channel"], settings):
            continue
        # Refresh just before claiming: a returned book/paid fine must not get an obsolete reminder.
        current = store.loans(loan["issue_id"])
        latest = prepare_message(current[0], now.date(), settings) if current else None
        if not latest or latest["key"] != message["key"]:
            continue
        if not store.claim(latest):
            continue
        try:
            send = providers.send_sms if latest["channel"] == "SMS" else providers.send_email
            provider_id = send(latest, settings)
        except providers.DeliveryRejected:
            store.finish(latest["key"], "FAILED")
        except Exception:
            store.finish(latest["key"], "UNKNOWN")
            logger.warning("Reminder outcome requires review: %s", latest["key"])
        else:
            store.finish(latest["key"], "ACCEPTED", provider_id)


def loop(stop):
    interval = max(60, int(config.get("REMINDER_CHECK_SECONDS", "300")))
    while not stop.is_set():
        try:
            run_once(stop=stop)
        except Exception as error:
            # Do not log provider responses, contact details or credentials.
            logger.warning("Reminder check failed (%s)", type(error).__name__)
        stop.wait(interval)


@asynccontextmanager
async def lifespan(app):
    stop = threading.Event()
    thread = None
    if config.get("REMINDERS_ENABLED", "false").lower() == "true":
        thread = threading.Thread(target=loop, args=(stop,), name="library-reminders", daemon=True)
        thread.start()
    try:
        yield
    finally:
        stop.set()
        if thread:
            await asyncio.to_thread(thread.join, 30)


def main():
    parser = argparse.ArgumentParser(description="Library SMS/email reminders")
    parser.add_argument("--check", action="store_true", help="Check configuration without sending")
    parser.add_argument(
        "--preview", action="store_true", help="Preview due messages without sending"
    )
    parser.add_argument("--once", action="store_true", help="Send enabled scheduled reminders once")
    args = parser.parse_args()
    if args.check:
        print("Scheduler enabled:", config.get("REMINDERS_ENABLED", "false"))
        for channel in ("SMS", "EMAIL"):
            print(channel, "ready:", providers.ready(channel, config))
    elif args.preview:
        for loan in store.loans():
            message = prepare_message(loan)
            if message:
                print(message["key"], message["channel"], message["body"])
    elif args.once:
        run_once()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Scheduled delivery while the app runs; a CLI supports an external scheduler.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import argparse</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import asyncio</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>import logging</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>import threading</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>from contextlib import asynccontextmanager</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from datetime import datetime</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 10 | <code>from backend.database import config</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from . import providers, store</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>from .messages import DHAKA, reminder_for</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>logger = logging.getLogger(__name__)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>def prepare_message(loan, today=None, settings=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 18 | <code>    settings = settings or config</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `prepare_message` অংশে |
| 19 | <code>    message = reminder_for(loan, today)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `prepare_message` অংশে |
| 20 | <code>    if message and message[&quot;channel&quot;] == &quot;SMS&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `prepare_message` অংশে |
| 21 | <code>        channel = settings.get(&quot;DUE_REMINDER_CHANNEL&quot;, &quot;email&quot;).upper()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `prepare_message` অংশে |
| 22 | <code>        if channel not in {&quot;SMS&quot;, &quot;EMAIL&quot;}:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `prepare_message` অংশে |
| 23 | <code>            raise ValueError(&quot;DUE_REMINDER_CHANNEL must be sms or email&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `prepare_message` অংশে |
| 24 | <code>        message[&quot;channel&quot;] = channel</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `prepare_message` অংশে |
| 25 | <code>        if channel == &quot;EMAIL&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `prepare_message` অংশে |
| 26 | <code>            message[&quot;recipient&quot;] = loan[&quot;email&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `prepare_message` অংশে |
| 27 | <code>    return message</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `prepare_message` অংশে |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 30 | <code>def run_once(settings=None, stop=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 31 | <code>    settings = settings or config</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 32 | <code>    if settings.get(&quot;REMINDERS_ENABLED&quot;, &quot;false&quot;).lower() != &quot;true&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 33 | <code>        return</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 34 | <code>    if not any(providers.ready(channel, settings) for channel in (&quot;SMS&quot;, &quot;EMAIL&quot;)):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 35 | <code>        return</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 36 | <code>    now = datetime.now(DHAKA)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 37 | <code>    if now.hour &lt; int(settings.get(&quot;REMINDER_SEND_HOUR&quot;, &quot;9&quot;)):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 38 | <code>        return</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 39 | <code>    store.recover_abandoned()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 40 | <code>    for loan in store.loans():</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `run_once` অংশে |
| 41 | <code>        if stop and stop.is_set():</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 42 | <code>            break</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 43 | <code>        message = prepare_message(loan, now.date(), settings)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 44 | <code>        if not message or not providers.ready(message[&quot;channel&quot;], settings):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 45 | <code>            continue</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 46 | <code>        # Refresh just before claiming: a returned book/paid fine must not get an obsolete reminder.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 47 | <code>        current = store.loans(loan[&quot;issue_id&quot;])</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 48 | <code>        latest = prepare_message(current[0], now.date(), settings) if current else None</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 49 | <code>        if not latest or latest[&quot;key&quot;] != message[&quot;key&quot;]:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 50 | <code>            continue</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 51 | <code>        if not store.claim(latest):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 52 | <code>            continue</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 53 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_once` অংশে |
| 54 | <code>            send = providers.send_sms if latest[&quot;channel&quot;] == &quot;SMS&quot; else providers.send_email</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 55 | <code>            provider_id = send(latest, settings)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `run_once` অংশে |
| 56 | <code>        except providers.DeliveryRejected:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_once` অংশে |
| 57 | <code>            store.finish(latest[&quot;key&quot;], &quot;FAILED&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 58 | <code>        except Exception:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `run_once` অংশে |
| 59 | <code>            store.finish(latest[&quot;key&quot;], &quot;UNKNOWN&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 60 | <code>            logger.warning(&quot;Reminder outcome requires review: %s&quot;, latest[&quot;key&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 61 | <code>        else:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `run_once` অংশে |
| 62 | <code>            store.finish(latest[&quot;key&quot;], &quot;ACCEPTED&quot;, provider_id)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `run_once` অংশে |
| 63 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>def loop(stop):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 66 | <code>    interval = max(60, int(config.get(&quot;REMINDER_CHECK_SECONDS&quot;, &quot;300&quot;)))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loop` অংশে |
| 67 | <code>    while not stop.is_set():</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `loop` অংশে |
| 68 | <code>        try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `loop` অংশে |
| 69 | <code>            run_once(stop=stop)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loop` অংশে |
| 70 | <code>        except Exception as error:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `loop` অংশে |
| 71 | <code>            # Do not log provider responses, contact details or credentials.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 72 | <code>            logger.warning(&quot;Reminder check failed (%s)&quot;, type(error).__name__)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loop` অংশে |
| 73 | <code>        stop.wait(interval)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loop` অংশে |
| 74 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 75 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 76 | <code>@asynccontextmanager</code> | Decorator; HTTP route অথবা test/classmethod behavior নিবন্ধন করে। |
| 77 | <code>async def lifespan(app):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 78 | <code>    stop = threading.Event()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `lifespan` অংশে |
| 79 | <code>    thread = None</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `lifespan` অংশে |
| 80 | <code>    if config.get(&quot;REMINDERS_ENABLED&quot;, &quot;false&quot;).lower() == &quot;true&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `lifespan` অংশে |
| 81 | <code>        thread = threading.Thread(target=loop, args=(stop,), name=&quot;library-reminders&quot;, daemon=True)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `lifespan` অংশে |
| 82 | <code>        thread.start()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `lifespan` অংশে |
| 83 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `lifespan` অংশে |
| 84 | <code>        yield</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `lifespan` অংশে |
| 85 | <code>    finally:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `lifespan` অংশে |
| 86 | <code>        stop.set()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `lifespan` অংশে |
| 87 | <code>        if thread:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `lifespan` অংশে |
| 88 | <code>            await asyncio.to_thread(thread.join, 30)</code> | Asynchronous operation-এর result-এর জন্য অপেক্ষা করে। `lifespan` অংশে |
| 89 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 90 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 91 | <code>def main():</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 92 | <code>    parser = argparse.ArgumentParser(description=&quot;Library SMS/email reminders&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 93 | <code>    parser.add_argument(&quot;--check&quot;, action=&quot;store_true&quot;, help=&quot;Check configuration without sending&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 94 | <code>    parser.add_argument(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 95 | <code>        &quot;--preview&quot;, action=&quot;store_true&quot;, help=&quot;Preview due messages without sending&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 96 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 97 | <code>    parser.add_argument(&quot;--once&quot;, action=&quot;store_true&quot;, help=&quot;Send enabled scheduled reminders once&quot;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 98 | <code>    args = parser.parse_args()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 99 | <code>    if args.check:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 100 | <code>        print(&quot;Scheduler enabled:&quot;, config.get(&quot;REMINDERS_ENABLED&quot;, &quot;false&quot;))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 101 | <code>        for channel in (&quot;SMS&quot;, &quot;EMAIL&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `main` অংশে |
| 102 | <code>            print(channel, &quot;ready:&quot;, providers.ready(channel, config))</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 103 | <code>    elif args.preview:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 104 | <code>        for loan in store.loans():</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `main` অংশে |
| 105 | <code>            message = prepare_message(loan)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `main` অংশে |
| 106 | <code>            if message:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 107 | <code>                print(message[&quot;key&quot;], message[&quot;channel&quot;], message[&quot;body&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 108 | <code>    elif args.once:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 109 | <code>        run_once()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 110 | <code>    else:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `main` অংশে |
| 111 | <code>        parser.print_help()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `main` অংশে |
| 112 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 113 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 114 | <code>if __name__ == &quot;__main__&quot;:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। |
| 115 | <code>    main()</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
