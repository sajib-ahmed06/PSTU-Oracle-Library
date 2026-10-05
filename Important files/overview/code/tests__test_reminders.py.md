# tests/test_reminders.py

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/test_reminders.py)। Snapshot 2026-10-04; 158 lines; SHA-256 `5b80021563f630443932fc28d0c87a08dcad320ac704107c086d22a3169c1550`।

## Function / object / element inventory

### `loan` — L8–L22

`def loan(**changes):`

Test/setup helper: loan; নিচের assertions/calls সেই behavior define করে।

### `test_three_day_message_has_book_deadline_and_daily_rate` — L26–L31

`def test_three_day_message_has_book_deadline_and_daily_rate(self):`

Test/setup helper: test three day message has book deadline and daily rate; নিচের assertions/calls সেই behavior define করে।

### `test_pre_due_catchup_keeps_one_event_key` — L33–L37

`def test_pre_due_catchup_keeps_one_event_key(self):`

Test/setup helper: test pre due catchup keeps one event key; নিচের assertions/calls সেই behavior define করে।

### `test_first_day_and_ten_day_milestones_use_todays_amount` — L39–L47

`def test_first_day_and_ten_day_milestones_use_todays_amount(self):`

Test/setup helper: test first day and ten day milestones use todays amount; নিচের assertions/calls সেই behavior define করে।

### `test_return_freezes_fine_and_payment_stops_reminders` — L49–L58

`def test_return_freezes_fine_and_payment_stops_reminders(self):`

Test/setup helper: test return freezes fine and payment stops reminders; নিচের assertions/calls সেই behavior define করে।

### `test_due_email_fallback_uses_registered_email` — L60–L65

`def test_due_email_fallback_uses_registered_email(self):`

Test/setup helper: test due email fallback uses registered email; নিচের assertions/calls সেই behavior define করে।

### `test_disabled_channels_never_report_ready` — L67–L69

`def test_disabled_channels_never_report_ready(self):`

Test/setup helper: test disabled channels never report ready; নিচের assertions/calls সেই behavior define করে।

### `dispatch` — L73–L89

`def dispatch(self, error=None, claimed=True, current=None):`

Test/setup helper: dispatch; নিচের assertions/calls সেই behavior define করে।

### `test_provider_acceptance_is_recorded` — L91–L94

`def test_provider_acceptance_is_recorded(self):`

Test/setup helper: test provider acceptance is recorded; নিচের assertions/calls সেই behavior define করে।

### `test_existing_claim_prevents_duplicate_sending` — L96–L99

`def test_existing_claim_prevents_duplicate_sending(self):`

Test/setup helper: test existing claim prevents duplicate sending; নিচের assertions/calls সেই behavior define করে।

### `test_returned_book_is_rechecked_before_sending` — L101–L103

`def test_returned_book_is_rechecked_before_sending(self):`

Test/setup helper: test returned book is rechecked before sending; নিচের assertions/calls সেই behavior define করে।

### `test_timeout_is_unknown_and_not_marked_retryable` — L105–L107

`def test_timeout_is_unknown_and_not_marked_retryable(self):`

Test/setup helper: test timeout is unknown and not marked retryable; নিচের assertions/calls সেই behavior define করে।

### `test_explicit_rejection_is_retryable` — L109–L111

`def test_explicit_rejection_is_retryable(self):`

Test/setup helper: test explicit rejection is retryable; নিচের assertions/calls সেই behavior define করে।

### `test_global_disable_does_not_touch_database` — L113–L116

`def test_global_disable_does_not_touch_database(self):`

Test/setup helper: test global disable does not touch database; নিচের assertions/calls সেই behavior define করে।

### `test_oracle_claim_guards_retries_and_commits_before_send` — L118–L125

`def test_oracle_claim_guards_retries_and_commits_before_send(self):`

Test/setup helper: test oracle claim guards retries and commits before send; নিচের assertions/calls সেই behavior define করে।

### `test_smtp_uses_tls_and_only_registered_recipient` — L127–L140

`def test_smtp_uses_tls_and_only_registered_recipient(self):`

Test/setup helper: test smtp uses tls and only registered recipient; নিচের assertions/calls সেই behavior define করে।

### `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` — L142–L158

`def test_sms_uses_registered_bangladeshi_number_and_provider_acceptance(self):`

Test/setup helper: test sms uses registered bangladeshi number and provider acceptance; নিচের assertions/calls সেই behavior define করে।

## সম্পূর্ণ original source

```python
import unittest
from datetime import date, datetime
from unittest.mock import patch

from backend.reminders import messages, providers, store, worker


def loan(**changes):
    item = {
        "issue_id": 7,
        "student_id": 2,
        "name": "Test Member",
        "title": "Clean Code",
        "phone": "01700000001",
        "email": "member@example.test",
        "copy_no": 3,
        "due_date": "2026-10-10",
        "status": "ISSUED",
        "balance": 0,
    }
    item.update(changes)
    return item


class ReminderRulesTests(unittest.TestCase):
    def test_three_day_message_has_book_deadline_and_daily_rate(self):
        result = messages.reminder_for(loan(), date(2026, 10, 7))
        self.assertEqual(result["channel"], "SMS")
        for text in ("Clean Code", "Copy #3", "2026-10-10", "Tk 10/day", "2026-10-11", "PSTU-0002"):
            self.assertIn(text, result["body"])
        self.assertIsNone(messages.reminder_for(loan(), date(2026, 10, 6)))

    def test_pre_due_catchup_keeps_one_event_key(self):
        early = messages.reminder_for(loan(), date(2026, 10, 7))
        later = messages.reminder_for(loan(), date(2026, 10, 9))
        self.assertEqual(early["key"], later["key"])
        self.assertIn("1 day(s) left", later["body"])

    def test_first_day_and_ten_day_milestones_use_todays_amount(self):
        first = messages.reminder_for(loan(), date(2026, 10, 11))
        between = messages.reminder_for(loan(), date(2026, 10, 20))
        next_reminder = messages.reminder_for(loan(), date(2026, 10, 21))
        self.assertEqual(first["key"], between["key"])
        self.assertNotEqual(first["key"], next_reminder["key"])
        self.assertIn("Tk 10", first["body"])
        self.assertIn("Tk 110", next_reminder["body"])
        self.assertEqual(next_reminder["channel"], "EMAIL")

    def test_return_freezes_fine_and_payment_stops_reminders(self):
        result = messages.reminder_for(loan(status="RETURNED", balance=80), date(2026, 11, 1))
        self.assertIn("Tk 80", result["body"])
        self.assertIn("no longer increases", result["body"])
        self.assertIsNone(
            messages.reminder_for(loan(status="RETURNED", balance=0), date(2026, 11, 1))
        )
        self.assertIsNone(
            messages.reminder_for(loan(status="RETURNED", balance=0), date(2026, 10, 7))
        )

    def test_due_email_fallback_uses_registered_email(self):
        result = worker.prepare_message(
            loan(), date(2026, 10, 7), {"DUE_REMINDER_CHANNEL": "email"}
        )
        self.assertEqual(result["channel"], "EMAIL")
        self.assertEqual(result["recipient"], "member@example.test")

    def test_disabled_channels_never_report_ready(self):
        self.assertFalse(providers.ready("EMAIL", {}))
        self.assertFalse(providers.ready("SMS", {"SMS_REMINDERS_ENABLED": "true"}))


class DeliveryTests(unittest.TestCase):
    def dispatch(self, error=None, claimed=True, current=None):
        settings = {"REMINDERS_ENABLED": "true", "DUE_REMINDER_CHANNEL": "email"}
        item = loan()
        with (
            patch.object(worker, "datetime") as clock,
            patch.object(providers, "ready", return_value=True),
            patch.object(store, "recover_abandoned"),
            patch.object(store, "loans", side_effect=[[item], [current or item]]),
            patch.object(store, "claim", return_value=claimed),
            patch.object(store, "finish") as finish,
            patch.object(
                providers, "send_email", return_value="accepted", side_effect=error
            ) as send,
        ):
            clock.now.return_value = datetime(2026, 10, 7, 10)
            worker.run_once(settings)
        return send, finish

    def test_provider_acceptance_is_recorded(self):
        send, finish = self.dispatch()
        send.assert_called_once()
        self.assertEqual(finish.call_args.args[1:], ("ACCEPTED", "accepted"))

    def test_existing_claim_prevents_duplicate_sending(self):
        send, finish = self.dispatch(claimed=False)
        send.assert_not_called()
        finish.assert_not_called()

    def test_returned_book_is_rechecked_before_sending(self):
        send, finish = self.dispatch(current=loan(status="RETURNED"))
        send.assert_not_called()

    def test_timeout_is_unknown_and_not_marked_retryable(self):
        send, finish = self.dispatch(error=TimeoutError())
        self.assertEqual(finish.call_args.args[1], "UNKNOWN")

    def test_explicit_rejection_is_retryable(self):
        send, finish = self.dispatch(error=providers.DeliveryRejected())
        self.assertEqual(finish.call_args.args[1], "FAILED")

    def test_global_disable_does_not_touch_database(self):
        with patch.object(store, "loans") as read:
            worker.run_once({"REMINDERS_ENABLED": "false"})
        read.assert_not_called()

    def test_oracle_claim_guards_retries_and_commits_before_send(self):
        with patch.object(store, "run_sql", return_value="CLAIMED") as sql:
            self.assertTrue(store.claim({"key": "test:7", "issue_id": 7, "channel": "EMAIL"}))
        statement = sql.call_args.args[0]
        self.assertIn("DUP_VAL_ON_INDEX", statement)
        self.assertIn("attempts<3", statement)
        self.assertIn("next_attempt<=SYSDATE", statement)
        self.assertIn("COMMIT", statement)

    def test_smtp_uses_tls_and_only_registered_recipient(self):
        settings = {
            "SMTP_HOST": "smtp.example.test",
            "SMTP_USERNAME": "test",
            "SMTP_PASSWORD": "fake",
            "SMTP_FROM": "library@example.test",
        }
        message = messages.reminder_for(loan(), date(2026, 10, 11))
        with patch.object(providers.smtplib, "SMTP") as smtp:
            connection = smtp.return_value.__enter__.return_value
            connection.send_message.return_value = {}
            self.assertEqual(providers.send_email(message, settings), "smtp-accepted")
        connection.starttls.assert_called_once()
        self.assertEqual(connection.send_message.call_args.args[0]["To"], "member@example.test")

    def test_sms_uses_registered_bangladeshi_number_and_provider_acceptance(self):
        from io import BytesIO
        from urllib.parse import parse_qs

        settings = {
            "TWILIO_ACCOUNT_SID": "AC" + "1" * 32,
            "TWILIO_AUTH_TOKEN": "fake",
            "TWILIO_FROM_NUMBER": "+12025550123",
        }
        message = messages.reminder_for(loan(), date(2026, 10, 7))
        with patch.object(providers, "urlopen") as request:
            request.return_value.__enter__.return_value = BytesIO(b'{"sid":"SM-test"}')
            self.assertEqual(providers.send_sms(message, settings), "SM-test")
        body = parse_qs(request.call_args.args[0].data.decode())
        self.assertEqual(body["To"], ["+8801700000001"])
        self.assertIn("2026-10-10", body["Body"][0])
        self.assertEqual(request.call_args.args[0].method, "POST")
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>import unittest</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 2 | <code>from datetime import date, datetime</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 3 | <code>from unittest.mock import patch</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>from backend.reminders import messages, providers, store, worker</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>def loan(**changes):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 9 | <code>    item = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `loan` অংশে |
| 10 | <code>        &quot;issue_id&quot;: 7,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 11 | <code>        &quot;student_id&quot;: 2,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 12 | <code>        &quot;name&quot;: &quot;Test Member&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 13 | <code>        &quot;title&quot;: &quot;Clean Code&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 14 | <code>        &quot;phone&quot;: &quot;01700000001&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 15 | <code>        &quot;email&quot;: &quot;member@example.test&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 16 | <code>        &quot;copy_no&quot;: 3,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 17 | <code>        &quot;due_date&quot;: &quot;2026-10-10&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 18 | <code>        &quot;status&quot;: &quot;ISSUED&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 19 | <code>        &quot;balance&quot;: 0,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 20 | <code>    }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 21 | <code>    item.update(changes)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `loan` অংশে |
| 22 | <code>    return item</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `loan` অংশে |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 25 | <code>class ReminderRulesTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 26 | <code>    def test_three_day_message_has_book_deadline_and_daily_rate(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 27 | <code>        result = messages.reminder_for(loan(), date(2026, 10, 7))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_three_day_message_has_book_deadline_and_daily_rate` অংশে |
| 28 | <code>        self.assertEqual(result[&quot;channel&quot;], &quot;SMS&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 29 | <code>        for text in (&quot;Clean Code&quot;, &quot;Copy #3&quot;, &quot;2026-10-10&quot;, &quot;Tk 10/day&quot;, &quot;2026-10-11&quot;, &quot;PSTU-0002&quot;):</code> | একাধিক fields/records/tokens অথবা retry/startup condition নিয়ে iteration করে। `test_three_day_message_has_book_deadline_and_daily_rate` অংশে |
| 30 | <code>            self.assertIn(text, result[&quot;body&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 31 | <code>        self.assertIsNone(messages.reminder_for(loan(), date(2026, 10, 6)))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 32 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 33 | <code>    def test_pre_due_catchup_keeps_one_event_key(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 34 | <code>        early = messages.reminder_for(loan(), date(2026, 10, 7))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_pre_due_catchup_keeps_one_event_key` অংশে |
| 35 | <code>        later = messages.reminder_for(loan(), date(2026, 10, 9))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_pre_due_catchup_keeps_one_event_key` অংশে |
| 36 | <code>        self.assertEqual(early[&quot;key&quot;], later[&quot;key&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 37 | <code>        self.assertIn(&quot;1 day(s) left&quot;, later[&quot;body&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 38 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 39 | <code>    def test_first_day_and_ten_day_milestones_use_todays_amount(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 40 | <code>        first = messages.reminder_for(loan(), date(2026, 10, 11))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_first_day_and_ten_day_milestones_use_todays_amount` অংশে |
| 41 | <code>        between = messages.reminder_for(loan(), date(2026, 10, 20))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_first_day_and_ten_day_milestones_use_todays_amount` অংশে |
| 42 | <code>        next_reminder = messages.reminder_for(loan(), date(2026, 10, 21))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_first_day_and_ten_day_milestones_use_todays_amount` অংশে |
| 43 | <code>        self.assertEqual(first[&quot;key&quot;], between[&quot;key&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 44 | <code>        self.assertNotEqual(first[&quot;key&quot;], next_reminder[&quot;key&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 45 | <code>        self.assertIn(&quot;Tk 10&quot;, first[&quot;body&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 46 | <code>        self.assertIn(&quot;Tk 110&quot;, next_reminder[&quot;body&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 47 | <code>        self.assertEqual(next_reminder[&quot;channel&quot;], &quot;EMAIL&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 48 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 49 | <code>    def test_return_freezes_fine_and_payment_stops_reminders(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 50 | <code>        result = messages.reminder_for(loan(status=&quot;RETURNED&quot;, balance=80), date(2026, 11, 1))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_return_freezes_fine_and_payment_stops_reminders` অংশে |
| 51 | <code>        self.assertIn(&quot;Tk 80&quot;, result[&quot;body&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 52 | <code>        self.assertIn(&quot;no longer increases&quot;, result[&quot;body&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 53 | <code>        self.assertIsNone(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 54 | <code>            messages.reminder_for(loan(status=&quot;RETURNED&quot;, balance=0), date(2026, 11, 1))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_return_freezes_fine_and_payment_stops_reminders` অংশে |
| 55 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_return_freezes_fine_and_payment_stops_reminders` অংশে |
| 56 | <code>        self.assertIsNone(</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 57 | <code>            messages.reminder_for(loan(status=&quot;RETURNED&quot;, balance=0), date(2026, 10, 7))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_return_freezes_fine_and_payment_stops_reminders` অংশে |
| 58 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_return_freezes_fine_and_payment_stops_reminders` অংশে |
| 59 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 60 | <code>    def test_due_email_fallback_uses_registered_email(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 61 | <code>        result = worker.prepare_message(</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_due_email_fallback_uses_registered_email` অংশে |
| 62 | <code>            loan(), date(2026, 10, 7), {&quot;DUE_REMINDER_CHANNEL&quot;: &quot;email&quot;}</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_due_email_fallback_uses_registered_email` অংশে |
| 63 | <code>        )</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_due_email_fallback_uses_registered_email` অংশে |
| 64 | <code>        self.assertEqual(result[&quot;channel&quot;], &quot;EMAIL&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 65 | <code>        self.assertEqual(result[&quot;recipient&quot;], &quot;member@example.test&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 66 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 67 | <code>    def test_disabled_channels_never_report_ready(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 68 | <code>        self.assertFalse(providers.ready(&quot;EMAIL&quot;, {}))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 69 | <code>        self.assertFalse(providers.ready(&quot;SMS&quot;, {&quot;SMS_REMINDERS_ENABLED&quot;: &quot;true&quot;}))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 70 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 71 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 72 | <code>class DeliveryTests(unittest.TestCase):</code> | Class definition; related test/helper behavior একত্র করে। |
| 73 | <code>    def dispatch(self, error=None, claimed=True, current=None):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 74 | <code>        settings = {&quot;REMINDERS_ENABLED&quot;: &quot;true&quot;, &quot;DUE_REMINDER_CHANNEL&quot;: &quot;email&quot;}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 75 | <code>        item = loan()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 76 | <code>        with (</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 77 | <code>            patch.object(worker, &quot;datetime&quot;) as clock,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 78 | <code>            patch.object(providers, &quot;ready&quot;, return_value=True),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 79 | <code>            patch.object(store, &quot;recover_abandoned&quot;),</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 80 | <code>            patch.object(store, &quot;loans&quot;, side_effect=[[item], [current or item]]),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 81 | <code>            patch.object(store, &quot;claim&quot;, return_value=claimed),</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 82 | <code>            patch.object(store, &quot;finish&quot;) as finish,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 83 | <code>            patch.object(</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 84 | <code>                providers, &quot;send_email&quot;, return_value=&quot;accepted&quot;, side_effect=error</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 85 | <code>            ) as send,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 86 | <code>        ):</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 87 | <code>            clock.now.return_value = datetime(2026, 10, 7, 10)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `dispatch` অংশে |
| 88 | <code>            worker.run_once(settings)</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `dispatch` অংশে |
| 89 | <code>        return send, finish</code> | Function-এর result caller-কে ফেরায় ও বর্তমান execution শেষ করে। `dispatch` অংশে |
| 90 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 91 | <code>    def test_provider_acceptance_is_recorded(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 92 | <code>        send, finish = self.dispatch()</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_provider_acceptance_is_recorded` অংশে |
| 93 | <code>        send.assert_called_once()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 94 | <code>        self.assertEqual(finish.call_args.args[1:], (&quot;ACCEPTED&quot;, &quot;accepted&quot;))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 95 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 96 | <code>    def test_existing_claim_prevents_duplicate_sending(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 97 | <code>        send, finish = self.dispatch(claimed=False)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_existing_claim_prevents_duplicate_sending` অংশে |
| 98 | <code>        send.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 99 | <code>        finish.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 100 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 101 | <code>    def test_returned_book_is_rechecked_before_sending(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 102 | <code>        send, finish = self.dispatch(current=loan(status=&quot;RETURNED&quot;))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_returned_book_is_rechecked_before_sending` অংশে |
| 103 | <code>        send.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 104 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 105 | <code>    def test_timeout_is_unknown_and_not_marked_retryable(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 106 | <code>        send, finish = self.dispatch(error=TimeoutError())</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_timeout_is_unknown_and_not_marked_retryable` অংশে |
| 107 | <code>        self.assertEqual(finish.call_args.args[1], &quot;UNKNOWN&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 108 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 109 | <code>    def test_explicit_rejection_is_retryable(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 110 | <code>        send, finish = self.dispatch(error=providers.DeliveryRejected())</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_explicit_rejection_is_retryable` অংশে |
| 111 | <code>        self.assertEqual(finish.call_args.args[1], &quot;FAILED&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 112 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 113 | <code>    def test_global_disable_does_not_touch_database(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 114 | <code>        with patch.object(store, &quot;loans&quot;) as read:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_global_disable_does_not_touch_database` অংশে |
| 115 | <code>            worker.run_once({&quot;REMINDERS_ENABLED&quot;: &quot;false&quot;})</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_global_disable_does_not_touch_database` অংশে |
| 116 | <code>        read.assert_not_called()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 117 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 118 | <code>    def test_oracle_claim_guards_retries_and_commits_before_send(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 119 | <code>        with patch.object(store, &quot;run_sql&quot;, return_value=&quot;CLAIMED&quot;) as sql:</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_oracle_claim_guards_retries_and_commits_before_send` অংশে |
| 120 | <code>            self.assertTrue(store.claim({&quot;key&quot;: &quot;test:7&quot;, &quot;issue_id&quot;: 7, &quot;channel&quot;: &quot;EMAIL&quot;}))</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 121 | <code>        statement = sql.call_args.args[0]</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_oracle_claim_guards_retries_and_commits_before_send` অংশে |
| 122 | <code>        self.assertIn(&quot;DUP_VAL_ON_INDEX&quot;, statement)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 123 | <code>        self.assertIn(&quot;attempts&lt;3&quot;, statement)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 124 | <code>        self.assertIn(&quot;next_attempt&lt;=SYSDATE&quot;, statement)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 125 | <code>        self.assertIn(&quot;COMMIT&quot;, statement)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 126 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 127 | <code>    def test_smtp_uses_tls_and_only_registered_recipient(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 128 | <code>        settings = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 129 | <code>            &quot;SMTP_HOST&quot;: &quot;smtp.example.test&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 130 | <code>            &quot;SMTP_USERNAME&quot;: &quot;test&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 131 | <code>            &quot;SMTP_PASSWORD&quot;: &quot;fake&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 132 | <code>            &quot;SMTP_FROM&quot;: &quot;library@example.test&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 133 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 134 | <code>        message = messages.reminder_for(loan(), date(2026, 10, 11))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 135 | <code>        with patch.object(providers.smtplib, &quot;SMTP&quot;) as smtp:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 136 | <code>            connection = smtp.return_value.__enter__.return_value</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 137 | <code>            connection.send_message.return_value = {}</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_smtp_uses_tls_and_only_registered_recipient` অংশে |
| 138 | <code>            self.assertEqual(providers.send_email(message, settings), &quot;smtp-accepted&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 139 | <code>        connection.starttls.assert_called_once()</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 140 | <code>        self.assertEqual(connection.send_message.call_args.args[0][&quot;To&quot;], &quot;member@example.test&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 141 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 142 | <code>    def test_sms_uses_registered_bangladeshi_number_and_provider_acceptance(self):</code> | Function definition; arguments গ্রহণ করে reusable logic শুরু করে। Async হলে await ব্যবহার করা যায়। |
| 143 | <code>        from io import BytesIO</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 144 | <code>        from urllib.parse import parse_qs</code> | Module/helper import; নিচের code-এ dependency ব্যবহার করার নাম যুক্ত করে। |
| 145 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 146 | <code>        settings = {</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 147 | <code>            &quot;TWILIO_ACCOUNT_SID&quot;: &quot;AC&quot; + &quot;1&quot; * 32,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 148 | <code>            &quot;TWILIO_AUTH_TOKEN&quot;: &quot;fake&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 149 | <code>            &quot;TWILIO_FROM_NUMBER&quot;: &quot;+12025550123&quot;,</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 150 | <code>        }</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 151 | <code>        message = messages.reminder_for(loan(), date(2026, 10, 7))</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 152 | <code>        with patch.object(providers, &quot;urlopen&quot;) as request:</code> | চলমান function expression, SQL string বা multi-line call-এর অংশ; উপরের function purpose ও পূর্ণ block একসঙ্গে পড়ো। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 153 | <code>            request.return_value.__enter__.return_value = BytesIO(b&#x27;{&quot;sid&quot;:&quot;SM-test&quot;}&#x27;)</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 154 | <code>            self.assertEqual(providers.send_sms(message, settings), &quot;SM-test&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 155 | <code>        body = parse_qs(request.call_args.args[0].data.decode())</code> | Value/configuration/query/result কোনো variable অথবা object field-এ assign করে। `test_sms_uses_registered_bangladeshi_number_and_provider_acceptance` অংশে |
| 156 | <code>        self.assertEqual(body[&quot;To&quot;], [&quot;+8801700000001&quot;])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 157 | <code>        self.assertIn(&quot;2026-10-10&quot;, body[&quot;Body&quot;][0])</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
| 158 | <code>        self.assertEqual(request.call_args.args[0].method, &quot;POST&quot;)</code> | Expected behavior/values পরীক্ষা করে; mismatch test failure করে। |
