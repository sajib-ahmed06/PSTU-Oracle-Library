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
