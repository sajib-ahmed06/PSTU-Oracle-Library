# backend/reminders/providers.py

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../backend/reminders/providers.py)। Snapshot 2026-10-04; 85 lines; SHA-256 `f08a5f3eb8a57446cad185171b88d66cb64834542ba679ab118733b90b89e501`।

## Function / object / element inventory

### `ready` — L18–L26

`def ready(channel, config):`

Test/setup helper: ready; নিচের assertions/calls সেই behavior define করে।

### `send_sms` — L29–L56

`def send_sms(message, config):`

Test/setup helper: send sms; নিচের assertions/calls সেই behavior define করে।

### `send_email` — L59–L85

`def send_email(message, config):`

Test/setup helper: send email; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
"""Twilio SMS and authenticated SMTP email adapters."""

import base64
import json
import re
import smtplib
import ssl
from email.message import EmailMessage
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class DeliveryRejected(Exception):
    """Provider explicitly rejected the message; a later retry is safe."""


def ready(channel, config):
    names = (
        ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER")
        if channel == "SMS"
        else ("SMTP_HOST", "SMTP_FROM", "SMTP_USERNAME", "SMTP_PASSWORD")
    )
    return config.get(f"{channel}_REMINDERS_ENABLED", "false").lower() == "true" and all(
        config.get(name) for name in names
    )


def send_sms(message, config):
    phone = message["recipient"]
    if re.fullmatch(r"01[0-9]{9}", phone or ""):
        phone = "+88" + phone
    if not re.fullmatch(r"\+[0-9]{8,15}", phone or ""):
        raise DeliveryRejected("Invalid recipient phone")
    sid = config["TWILIO_ACCOUNT_SID"]
    if not re.fullmatch(r"AC[a-fA-F0-9]{32}", sid):
        raise DeliveryRejected("Invalid account configuration")
    authorization = base64.b64encode(f"{sid}:{config['TWILIO_AUTH_TOKEN']}".encode()).decode()
    request = Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
        data=urlencode(
            {"To": phone, "From": config["TWILIO_FROM_NUMBER"], "Body": message["body"]}
        ).encode(),
        headers={
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)["sid"]
    except HTTPError as error:
        if 400 <= error.code < 500:
            raise DeliveryRejected("SMS provider rejected the message") from None
        raise


def send_email(message, config):
    email = EmailMessage()
    email["From"] = config["SMTP_FROM"]
    email["To"] = message["recipient"]
    email["Subject"] = message["subject"]
    email.set_content(message["body"])
    context = ssl.create_default_context()
    implicit_tls = config.get("SMTP_SECURITY", "starttls").lower() == "ssl"
    client = smtplib.SMTP_SSL if implicit_tls else smtplib.SMTP
    port = int(config.get("SMTP_PORT", "465" if implicit_tls else "587"))
    options = {"context": context} if implicit_tls else {}
    try:
        with client(config["SMTP_HOST"], port, timeout=20, **options) as connection:
            if not implicit_tls:
                connection.starttls(context=context)
            connection.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
            refused = connection.send_message(email)
            if refused:
                raise DeliveryRejected("Email recipient rejected")
    except (
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPDataError,
    ) as error:
        raise DeliveryRejected("Email provider rejected the message") from error
    return "smtp-accepted"
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;&quot;&quot;Twilio SMS and authenticated SMTP email adapters.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>import base64</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>import json</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 5 | <code>import re</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>import smtplib</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 7 | <code>import ssl</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 8 | <code>from email.message import EmailMessage</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 9 | <code>from urllib.error import HTTPError</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 10 | <code>from urllib.parse import urlencode</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 11 | <code>from urllib.request import Request, urlopen</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 14 | <code>class DeliveryRejected(Exception):</code> | Class definition; related test/helper behavior একত্র করে। |
| 15 | <code>    &quot;&quot;&quot;Provider explicitly rejected the message; a later retry is safe.&quot;&quot;&quot;</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>def ready(channel, config):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 19 | <code>    names = (</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `ready` অংশে |
| 20 | <code>        (&quot;TWILIO_ACCOUNT_SID&quot;, &quot;TWILIO_AUTH_TOKEN&quot;, &quot;TWILIO_FROM_NUMBER&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `ready` অংশে |
| 21 | <code>        if channel == &quot;SMS&quot;</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `ready` অংশে |
| 22 | <code>        else (&quot;SMTP_HOST&quot;, &quot;SMTP_FROM&quot;, &quot;SMTP_USERNAME&quot;, &quot;SMTP_PASSWORD&quot;)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `ready` অংশে |
| 23 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `ready` অংশে |
| 24 | <code>    return config.get(f&quot;{channel}_REMINDERS_ENABLED&quot;, &quot;false&quot;).lower() == &quot;true&quot; and all(</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `ready` অংশে |
| 25 | <code>        config.get(name) for name in names</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `ready` অংশে |
| 26 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `ready` অংশে |
| 27 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>def send_sms(message, config):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 30 | <code>    phone = message[&quot;recipient&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 31 | <code>    if re.fullmatch(r&quot;01[0-9]{9}&quot;, phone or &quot;&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `send_sms` অংশে |
| 32 | <code>        phone = &quot;+88&quot; + phone</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 33 | <code>    if not re.fullmatch(r&quot;\+[0-9]{8,15}&quot;, phone or &quot;&quot;):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `send_sms` অংশে |
| 34 | <code>        raise DeliveryRejected(&quot;Invalid recipient phone&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `send_sms` অংশে |
| 35 | <code>    sid = config[&quot;TWILIO_ACCOUNT_SID&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 36 | <code>    if not re.fullmatch(r&quot;AC[a-fA-F0-9]{32}&quot;, sid):</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `send_sms` অংশে |
| 37 | <code>        raise DeliveryRejected(&quot;Invalid account configuration&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `send_sms` অংশে |
| 38 | <code>    authorization = base64.b64encode(f&quot;{sid}:{config[&#x27;TWILIO_AUTH_TOKEN&#x27;]}&quot;.encode()).decode()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 39 | <code>    request = Request(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 40 | <code>        f&quot;https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 41 | <code>        data=urlencode(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 42 | <code>            {&quot;To&quot;: phone, &quot;From&quot;: config[&quot;TWILIO_FROM_NUMBER&quot;], &quot;Body&quot;: message[&quot;body&quot;]}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 43 | <code>        ).encode(),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 44 | <code>        headers={</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 45 | <code>            &quot;Authorization&quot;: f&quot;Basic {authorization}&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 46 | <code>            &quot;Content-Type&quot;: &quot;application/x-www-form-urlencoded&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 47 | <code>        },</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 48 | <code>        method=&quot;POST&quot;,</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 49 | <code>    )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 50 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `send_sms` অংশে |
| 51 | <code>        with urlopen(request, timeout=20) as response:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_sms` অংশে |
| 52 | <code>            return json.load(response)[&quot;sid&quot;]</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `send_sms` অংশে |
| 53 | <code>    except HTTPError as error:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `send_sms` অংশে |
| 54 | <code>        if 400 &lt;= error.code &lt; 500:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `send_sms` অংশে |
| 55 | <code>            raise DeliveryRejected(&quot;SMS provider rejected the message&quot;) from None</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `send_sms` অংশে |
| 56 | <code>        raise</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_sms` অংশে |
| 57 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 58 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 59 | <code>def send_email(message, config):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 60 | <code>    email = EmailMessage()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 61 | <code>    email[&quot;From&quot;] = config[&quot;SMTP_FROM&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 62 | <code>    email[&quot;To&quot;] = message[&quot;recipient&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 63 | <code>    email[&quot;Subject&quot;] = message[&quot;subject&quot;]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 64 | <code>    email.set_content(message[&quot;body&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 65 | <code>    context = ssl.create_default_context()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 66 | <code>    implicit_tls = config.get(&quot;SMTP_SECURITY&quot;, &quot;starttls&quot;).lower() == &quot;ssl&quot;</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 67 | <code>    client = smtplib.SMTP_SSL if implicit_tls else smtplib.SMTP</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 68 | <code>    port = int(config.get(&quot;SMTP_PORT&quot;, &quot;465&quot; if implicit_tls else &quot;587&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 69 | <code>    options = {&quot;context&quot;: context} if implicit_tls else {}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 70 | <code>    try:</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `send_email` অংশে |
| 71 | <code>        with client(config[&quot;SMTP_HOST&quot;], port, timeout=20, **options) as connection:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 72 | <code>            if not implicit_tls:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `send_email` অংশে |
| 73 | <code>                connection.starttls(context=context)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 74 | <code>            connection.login(config[&quot;SMTP_USERNAME&quot;], config[&quot;SMTP_PASSWORD&quot;])</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 75 | <code>            refused = connection.send_message(email)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `send_email` অংশে |
| 76 | <code>            if refused:</code> | Condition অনুযায়ী success/failure/alternative branch নির্বাচন করে। `send_email` অংশে |
| 77 | <code>                raise DeliveryRejected(&quot;Email recipient rejected&quot;)</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `send_email` অংশে |
| 78 | <code>    except (</code> | Exceptions ধরার বা success/failure নির্বিশেষে cleanup করার block। `send_email` অংশে |
| 79 | <code>        smtplib.SMTPRecipientsRefused,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 80 | <code>        smtplib.SMTPAuthenticationError,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 81 | <code>        smtplib.SMTPSenderRefused,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 82 | <code>        smtplib.SMTPDataError,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 83 | <code>    ) as error:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `send_email` অংশে |
| 84 | <code>        raise DeliveryRejected(&quot;Email provider rejected the message&quot;) from error</code> | Failure condition-এ exception তোলে; HTTP validation/database/test failure caller-এর কাছে যায়। `send_email` অংশে |
| 85 | <code>    return &quot;smtp-accepted&quot;</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `send_email` অংশে |
